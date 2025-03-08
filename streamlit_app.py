import streamlit as st
from PIL import Image
import easyocr
import numpy as np

st.set_page_config(page_title="Text Scanner", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .big-text {
        font-size: 28px !important;
        line-height: 1.5;
        margin: 20px 0;
        text-align: center;
    }
    
    /* Style the file uploader */
    .stFileUploader > label {
        font-size: 28px !important;
        width: 90% !important;
        margin: 20px auto !important;
        padding: 20px !important;
        border: 3px dashed #0088ff !important;
        border-radius: 15px !important;
        text-align: center !important;
    }
    
    /* Style the download button */
    .stDownloadButton > button {
        font-size: 28px !important;
        padding: 20px !important;
        width: 90% !important;
        margin: 20px auto !important;
        display: block !important;
        border-radius: 15px !important;
        background-color: #0088ff !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("Text Scanner")

# File uploader
uploaded_file = st.file_uploader(
    "📸 TAP HERE TO TAKE PHOTO OR BROWSE",
    type=['jpg', 'jpeg', 'png', 'pdf'],
)

# Initialize EasyOCR with GPU
@st.cache_resource
def get_ocr_reader():
    return easyocr.Reader(['en'], gpu=True)  # Changed to GPU=True

if uploaded_file:
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
            if confidence > 0.2:
                all_text.append(text)
                st.write(text)
        
        if all_text:
            combined_text = "\n".join(all_text)
            st.download_button(
                "💾 SAVE TEXT",
                data=combined_text,
                file_name="text.txt",
                mime="text/plain",
                use_container_width=True
            )
else:
    st.markdown("""
        <div class="big-text">
        Tap above to:<br>
        📸 Take a new photo<br>
        or<br>
        📄 Choose a saved photo
        </div>
    """, unsafe_allow_html=True)
