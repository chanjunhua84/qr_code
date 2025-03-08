import streamlit as st
from paddleocr import PaddleOCR
import cv2
import numpy as np
from PIL import Image
import tempfile

st.set_page_config(page_title="PaddleOCR Demo", layout="wide")

def main():
    st.title("📑 PaddleOCR Text Recognition")
    
    # Language selection
    lang = st.sidebar.selectbox(
        "Select Language",
        ["ch", "en", "fr", "german", "korean", "japan"]
    )
    
    # Initialize OCR
    @st.cache_resource
    def load_ocr(lang):
        return PaddleOCR(use_angle_cls=True, lang=lang)
    
    ocr = load_ocr(lang)
    
    # File upload
    uploaded_file = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        # Read image
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Extract Text"):
            with st.spinner("Processing..."):
                # Convert to numpy array
                img_array = np.array(image)
                
                # OCR detection
                result = ocr.ocr(img_array)
                
                # Draw result
                result = result[0]
                image = Image.fromarray(img_array)
                if result:
                    boxes = [line[0] for line in result]
                    txts = [line[1][0] for line in result]
                    scores = [line[1][1] for line in result]
                    
                    # Draw boxes
                    img_draw = img_array.copy()
                    for box in boxes:
                        box = np.array(box).astype(np.int32).reshape((-1, 1, 2))
                        cv2.polylines(img_draw, [box], True, (255, 0, 0), 2)
                    
                    with col2:
                        st.image(img_draw, caption="Detected Text Regions", use_column_width=True)
                    
                    # Show results
                    st.subheader("Extracted Text")
                    extracted_text = ""
                    for txt, score in zip(txts, scores):
                        extracted_text += f"{txt}\n"
                        st.write(f"Text: {txt}")
                        st.write(f"Confidence: {score:.4f}")
                        st.write("---")
                    
                    # Download button
                    st.download_button(
                        label="Download extracted text",
                        data=extracted_text,
                        file_name="extracted_text.txt",
                        mime="text/plain"
                    )
                else:
                    st.write("No text detected")

if __name__ == "__main__":
    main()
