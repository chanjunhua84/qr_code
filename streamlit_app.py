import streamlit as st
from PIL import Image
import easyocr
import numpy as np

def inject_custom_css():
    st.markdown("""
        <style>
        /* Large text */
        .big-text {
            font-size: 28px !important;
            line-height: 1.5;
            margin: 20px 0;
            text-align: center;
        }
        
        /* Big buttons */
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
        
        /* Center content */
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

    st.markdown('<h1 style="text-align: center; font-size: 36px;">Text Scanner</h1>', 
                unsafe_allow_html=True)

    # Initialize EasyOCR with CPU only
    @st.cache_resource
    def get_ocr_reader():
        return easyocr.Reader(['en'], gpu=False)
    
    # Two buttons side by side
    col1, col2 = st.columns(2)
    
    with col1:
        st.button("📄 BROWSE DOCUMENT", key="browse", use_container_width=True)
    with col2:
        st.button("📸 TAKE PHOTO", key="photo", use_container_width=True)

    # File uploader (hidden but functional)
    uploaded_file = st.file_uploader(
        "",
        type=['jpg', 'jpeg', 'png', 'pdf'],
        key="uploader",
        label_visibility="hidden"
    )

    if uploaded_file is not None:
        # Load and process image
        image = Image.open(uploaded_file)
        
        with st.spinner('Reading text... Please wait...'):
            # Get OCR reader
            reader = get_ocr_reader()
            
            # Perform OCR
            results = reader.readtext(np.array(image))
            
            # Display results
            st.markdown('<div class="big-text">Found Text:</div>', 
                       unsafe_allow_html=True)
            
            all_text = []
            for result in results:
                text = result[1]
                confidence = result[2]
                if confidence > 0.2:  # Filter low confidence results
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
            else:
                st.markdown('<div class="big-text">No text found. Please try again.</div>', 
                           unsafe_allow_html=True)
            
            st.markdown('<div class="big-text">Want to scan another?</div>', 
                       unsafe_allow_html=True)
            
            if st.button("📸 SCAN ANOTHER", key="scan_again", use_container_width=True):
                st.rerun()
    else:
        # Instructions
        st.markdown("""
            <div class="big-text">
            Choose an option:<br><br>
            📄 BROWSE DOCUMENT - Select a saved photo<br><br>
            📸 TAKE PHOTO - Use your camera
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
