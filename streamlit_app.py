import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import cv2
import base64
from pathlib import Path

def load_model():
    return easyocr.Reader(['en'])

def perform_ocr(image, reader):
    results = reader.readtext(np.array(image))
    return results

def inject_custom_css():
    st.markdown("""
        <style>
        /* Full-width button styling */
        .big-button {
            width: 100%;
            padding: 20px;
            font-size: 24px !important;
            margin: 10px 0;
            border-radius: 10px;
            background-color: #0088ff;
            color: white;
        }
        
        /* Large text styling */
        .large-text {
            font-size: 20px;
            line-height: 1.5;
        }
        
        /* Camera input container - hide when not needed */
        .camera-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 1000;
            background: white;
        }
        
        /* Make the camera view full screen */
        .stCamera {
            width: 100vw;
            height: 100vh;
            position: fixed;
            top: 0;
            left: 0;
        }
        
        /* Style the camera button to be more visible */
        .stCamera > button {
            background-color: #0088ff !important;
            color: white !important;
            padding: 20px !important;
            font-size: 20px !important;
            border-radius: 10px !important;
            margin: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide")
    inject_custom_css()
    
    st.title("Easy Text Scanner", anchor=False)
    
    # Initialize EasyOCR
    @st.cache_resource
    def get_ocr_reader():
        return load_model()
    
    reader = get_ocr_reader()

    # Session state for controlling flow
    if 'show_camera' not in st.session_state:
        st.session_state.show_camera = False
    
    # Large, easy to see button
    if not st.session_state.show_camera:
        st.markdown('<div class="large-text">Click the button below to take a photo:</div>', 
                   unsafe_allow_html=True)
        if st.button("📸 TAKE PHOTO", key="take_photo", 
                    help="Click to open camera", 
                    use_container_width=True):
            st.session_state.show_camera = True
            st.experimental_rerun()

    # Show camera when button is clicked
    if st.session_state.show_camera:
        img_file = st.camera_input("", key="camera")
        
        if img_file is not None:
            st.session_state.show_camera = False
            image = Image.open(img_file)
            
            # Show processing message
            with st.spinner('Reading text from image...'):
                # Perform OCR
                results = perform_ocr(image, reader)
                
                # Display results
                st.markdown("### Found Text:", unsafe_allow_html=True)
                
                all_text = []
                for result in results:
                    text = result[1]
                    confidence = result[2]
                    all_text.append(text)
                    st.markdown(f'<div class="large-text">{text}</div>', 
                              unsafe_allow_html=True)
                
                # Combine all text
                if all_text:
                    combined_text = "\n".join(all_text)
                    
                    # Large download button
                    st.markdown('<div class="large-text">Save the text to your phone:</div>', 
                              unsafe_allow_html=True)
                    st.download_button(
                        label="💾 SAVE TEXT",
                        data=combined_text,
                        file_name="scanned_text.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                # Large button to scan again
                st.markdown('<div class="large-text">Want to scan another?</div>', 
                          unsafe_allow_html=True)
                if st.button("📸 SCAN AGAIN", 
                           use_container_width=True):
                    st.session_state.show_camera = True
                    st.experimental_rerun()

    # Simple instructions with large text
    if not st.session_state.show_camera:
        st.markdown("""
        <div class="large-text">
        <br>
        How to use:
        <br>
        1. Click 'TAKE PHOTO'
        <br>
        2. Point camera at text
        <br>
        3. Take picture
        <br>
        4. Wait for text to appear
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
