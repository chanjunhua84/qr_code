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
    </style>
""", unsafe_allow_html=True)

# Title
st.title("Text Scanner")

# Initialize EasyOCR with CPU only
@st.cache_resource
def get_ocr_reader():
    return easyocr.Reader(['en'], gpu=False)

# Two columns for buttons
col1, col2 = st.columns(2)

with col1:
    browse_btn = st.button("📄 BROWSE", use_container_width=True)
with col2:
    photo_btn = st.button("📸 PHOTO", use_container_width=True)

# File uploader
uploaded_file = st.file_uploader(
    "",
    type=['jpg', 'jpeg', 'png', 'pdf'],
    label_visibility="hidden"
)

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
        
        if st.button("📸 SCAN ANOTHER"):
            st.rerun()
else:
    st.markdown("""
        <div class="big-text">
        Choose an option:<br>
        📄 BROWSE - Select a saved photo<br>
        📸 PHOTO - Use your camera
        </div>
    """, unsafe_allow_html=True)
