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
        /* Make text and buttons larger */
        .big-text {
            font-size: 24px !important;
            margin: 15px 0;
        }
        
        .stButton > button {
            font-size: 24px !important;
            padding: 15px !important;
            width: 100%;
        }
        
        /* Make camera button more prominent */
        .stCamera > button {
            font-size: 24px !important;
            padding: 15px !important;
            background-color: #0088ff !important;
            color: white !important;
            width: 100% !important;
        }
        
        /* Center camera preview */
        .stCamera > video {
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 auto;
            display: block;
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

    st.title("Text Scanner")

    # Simple instructions
    st.markdown('<div class="big-text">Point camera at text and take a photo</div>', 
                unsafe_allow_html=True)

    # Camera input
    picture = st.camera_input(
        label="",
        key="camera",
        help="Click to take photo",
        disabled=False,
        label_visibility="collapsed"
    )

    if picture:
        image = Image.open(picture)
        
        with st.spinner('Reading text...'):
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
                
                st.download_button(
                    label="💾 SAVE TEXT",
                    data=combined_text,
                    file_name="scanned_text.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            if st.button("📸 SCAN ANOTHER", use_container_width=True):
                st.rerun()

if __name__ == "__main__":
    main()
