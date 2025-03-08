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
        /* Hide default elements */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Large text styling */
        .large-text {
            font-size: 24px;
            line-height: 1.6;
            margin: 20px 0;
            text-align: center;
        }
        
        /* Results container */
        .results-container {
            padding: 20px;
            margin-top: 20px;
            font-size: 24px;
        }
        
        /* Hide default file uploader */
        .stFileUploader {
            display: none;
        }
        
        /* Custom button styling */
        .stButton > button {
            width: 80%;
            height: 100px;
            margin: 10% 10%;
            font-size: 24px !important;
            background-color: #0088ff;
            color: white;
            border-radius: 15px;
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

    # Create two columns for centering
    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        # Custom file input that forces back camera
        st.markdown("""
            <div class="large-text">
                <input type="file" 
                    id="camera" 
                    accept="image/*" 
                    capture="environment"
                    style="display: none;"
                    onchange="handleFileSelect(event)">
            </div>
            """, unsafe_allow_html=True)

        # JavaScript to handle file selection
        st.markdown("""
            <script>
            function handleFileSelect(event) {
                const file = event.target.files[0];
                const formData = new FormData();
                formData.append('file', file);
                
                // Submit the form
                document.getElementsByTagName('form')[0].submit();
            }
            </script>
            """, unsafe_allow_html=True)

        # Button that triggers the hidden file input
        if st.button("📸 TAKE PHOTO", key="camera_button"):
            st.markdown("""
                <script>
                document.getElementById('camera').click();
                </script>
                """, unsafe_allow_html=True)

    # File uploader (hidden but functional)
    uploaded_file = st.file_uploader(
        "",
        type=['jpg', 'jpeg', 'png'],
        key="uploader",
        label_visibility="hidden"
    )

    # Process image if uploaded
    if uploaded_file:
        image = Image.open(uploaded_file)
        
        with st.spinner('Reading text...'):
            results = perform_ocr(image, reader)
            
            st.markdown('<div class="results-container">', unsafe_allow_html=True)
            
            all_text = []
            for result in results:
                text = result[1]
                confidence = result[2]
                if confidence > 0.2:  # Filter low confidence results
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
            st.rerun()
    else:
        # Instructions
        st.markdown("""
            <div class="large-text" style="margin-top: 40px;">
            How to use:<br>
            1. Tap TAKE PHOTO button<br>
            2. Allow camera access<br>
            3. Take picture of text<br>
            4. Wait for results
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
