import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import easyocr
import os

# Force CPU usage
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Set page configuration
st.set_page_config(
    page_title="Camera OCR App",
    page_icon="📸",
    layout="wide"
)

@st.cache_resource(show_spinner=False)
def load_ocr():
    try:
        return easyocr.Reader(['en'], gpu=False)
    except Exception as e:
        st.error(f"Error loading OCR model: {str(e)}")
        return None

def process_image(image):
    try:
        image_np = np.array(image)
        results = st.session_state.ocr_reader.readtext(image_np)
        
        if not results:
            st.warning("No text was detected. Please try again with a clearer photo.")
            return
        
        # Display results
        extracted_text = ""
        for result in results:
            text, confidence = result[1], result[2]
            extracted_text += f"{text}\n"
            st.markdown(f"""
                <div style='
                    background-color: #f0f2f6;
                    padding: 1rem;
                    border-radius: 0.5rem;
                    margin: 0.5rem 0;
                '>
                    <p style='font-size: 1.2rem; margin: 0;'>{text}</p>
                    <p style='color: #666; margin: 0;'>Confidence: {confidence:.2f}</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Download button
        st.download_button(
            "💾 Download Extracted Text",
            extracted_text,
            file_name="extracted_text.txt",
            mime="text/plain"
        )
        
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")

def main():
    st.title("📸 Smart Text Scanner")
    
    # Initialize OCR
    if 'ocr_reader' not in st.session_state:
        with st.spinner("Loading OCR model..."):
            st.session_state.ocr_reader = load_ocr()

    # Simple camera input
    st.markdown("### Take a Photo or Upload an Image")
    image_source = st.camera_input("", key="camera")
    
    if image_source is not None:
        image = Image.open(image_source)
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Captured Image", use_container_width=True)
        
        with col2:
            st.markdown("### Extracted Text")
            process_image(image)

    # Alternative file upload
    st.markdown("### Or Upload an Image")
    uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        process_image(image)

    # Tips
    with st.expander("📌 Tips for Better Results"):
        st.markdown("""
            - Ensure good lighting
            - Hold the camera steady
            - Keep text horizontal
            - Avoid glare and shadows
            - Position text within frame
            - Make sure text is in focus
        """)

if __name__ == "__main__":
    main()
