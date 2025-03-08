import streamlit as st
import easyocr
from PIL import Image
import numpy as np

def load_model():
    return easyocr.Reader(['en'])

def perform_ocr(image, reader):
    results = reader.readtext(np.array(image))
    return results

def inject_custom_css():
    st.markdown("""
        <style>
        /* Large, clear text */
        .big-text {
            font-size: 28px !important;
            line-height: 1.5;
            margin: 20px 0;
            text-align: center;
        }
        
        /* Make buttons very prominent */
        .stButton > button {
            font-size: 28px !important;
            padding: 20px !important;
            width: 90% !important;
            margin: 20px auto !important;
            display: block !important;
            border-radius: 15px !important;
            background-color: #0088ff !important;
            color: white !important;
        }
        
        /* Hide the default file uploader */
        .stFileUploader > label {
            font-size: 28px !important;
            width: 90% !important;
            margin: 20px auto !important;
            padding: 20px !important;
            border: 3px dashed #0088ff !important;
            border-radius: 15px !important;
            text-align: center !important;
        }
        
        /* Center all content */
        .block-container {
            max-width: 100%;
            padding: 20px;
        }
        </style>
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

    st.markdown('<h1 style="text-align: center; font-size: 36px;">Text Scanner</h1>', 
                unsafe_allow_html=True)

    # Clear instructions
    if 'processed_image' not in st.session_state:
        st.markdown("""
            <div class="big-text">
            1. Tap the button below<br>
            2. Take photo using your camera<br>
            3. Wait for the text to appear
            </div>
        """, unsafe_allow_html=True)

    # File uploader styled as a big button
    uploaded_file = st.file_uploader(
        "📸 TAP HERE TO TAKE PHOTO",
        type=['jpg', 'jpeg', 'png'],
        accept_multiple_files=False,
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        
        with st.spinner('Reading the text from your photo...'):
            results = perform_ocr(image, reader)
            
            st.markdown('<div class="big-text">Found Text:</div>', 
                       unsafe_allow_html=True)
            
            all_text = []
            for result in results:
                text = result[1]
                confidence = result[2]
                if confidence > 0.2:
                    all_text.append(text)
                    st.markdown(f'<div class="big-text">{text}</div>', 
                              unsafe_allow_html=True)
            
            if all_text:
                combined_text = "\n".join(all_text)
                
                st.markdown('<div class="big-text">Save the text:</div>', 
                           unsafe_allow_html=True)
                
                st.download_button(
                    label="💾 SAVE TEXT",
                    data=combined_text,
                    file_name="scanned_text.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            st.markdown('<div class="big-text">Want to scan another?</div>', 
                       unsafe_allow_html=True)
            
            if st.button("📸 SCAN ANOTHER", use_container_width=True):
                st.rerun()

if __name__ == "__main__":
    main()
