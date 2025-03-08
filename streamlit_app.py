import streamlit as st
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np

# Initialize OCR
ocr = PaddleOCR(use_angle_cls=True, lang="en")

st.title("Better OCR with PaddleOCR")

uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Convert to numpy array
    img_np = np.array(image)

    # Perform OCR
    result = ocr.ocr(img_np, cls=True)
    
    # Display results
    for line in result:
        for word in line:
            st.write("Detected Text:", word[1][0])
