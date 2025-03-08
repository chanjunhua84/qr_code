import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import cv2

def load_model():
    return easyocr.Reader(['en'])

def perform_ocr(image, reader):
    results = reader.readtext(np.array(image))
    return results

def inject_custom_css():
    st.markdown("""
        <style>
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Full screen button styling */
        .camera-button {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 80vw;
            height: 15vh;
            font-size: 24px !important;
            background-color: #0088ff;
            color: white;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            z-index: 1000;
        }
        
        /* Large text styling */
        .large-text {
            font-size: 24px;
            line-height: 1.6;
            margin: 20px 0;
        }
        
        /* Results container */
        .results-container {
            padding: 20px;
            margin-top: 20px;
            font-size: 24px;
        }
        
        /* Custom file uploader */
        .stFileUploader {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)

def create_camera_button():
    return st.markdown("""
        <input type="file" 
               id="camera" 
               accept="image/*" 
               capture="environment" 
               style="display: none;">
        <button class="camera-button" onclick="document.getElementById('camera').click()">
            📸 TAKE PHOTO
        </button>
        <script>
            document.getElementById('camera').onchange = function(e) {
                var form = new FormData();
                form.append('file', e.target.files[0]);
                fetch('/', {
                    method: 'POST',
                    body: form
                });
            }
        </script>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Text Scanner",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    inject_custom_css()
    
    # Initialize EasyOCR
    @st.cache_resource
    def get_ocr_reader():
        return load_model()
    
    reader = get_ocr_reader()

    # Session state
    if 'processed_image' not in st.session_state:
        st.session_state.processed_image = None

    # Main interface
    st.markdown('<h1 style="text-align: center; font-size: 36px;">Text Scanner</h1>', 
                unsafe_allow_html=True)

    # File uploader that triggers native camera
    uploaded_file = st.file_uploader(
        "",
        type=['jpg', 'jpeg', 'png'],
        key="uploader",
        accept_multiple_files=False,
        help="",
        on_change=None,
        args=None,
        kwargs=None,
    )

    # Custom camera button
    if not uploaded_file:
        st.markdown(
            '<div class="large-text" style="text-align: center;">Tap button to take photo:</div>',
            unsafe_allow_html=True
        )
        create_camera_button()
        
        # Instructions
        st.markdown("""
            <div class="large-text" style="text-align: center; margin-top: 40vh;">
            How to use:<br>
            1. Tap the TAKE PHOTO button<br>
            2. Allow camera access<br>
            3. Take picture of text<br>
            4. Wait for results
            </div>
        """, unsafe_allow_html=True)

    # Process image if uploaded
    if uploaded_file:
        image = Image.open(uploaded_file)
        
        with st.spinner('Reading text...'):
            results = perform_ocr(image, reader)
            
            # Display results
            st.markdown('<div class="results-container">', unsafe_allow_html=True)
            
            all_text = []
            for result in results:
                text = result[1]
                confidence = result[2]
                all_text.append(text)
                st.markdown(f'<div class="large-text">{text}</div>', 
                          unsafe_allow_html=True)
            
            if all_text:
                combined_text = "\n".join(all_text)
                
                # Download button
                st.download_button(
                    label="💾 SAVE TEXT",
                    data=combined_text,
                    file_name="scanned_text.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Scan again button
        if st.button("📸 SCAN ANOTHER", use_container_width=True):
            st.session_state.processed_image = None
            st.rerun()

if __name__ == "__main__":
    main()
