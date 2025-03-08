import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import easyocr
import os
import io

# Force CPU usage
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Set page configuration
st.set_page_config(
    page_title="Camera OCR App",
    page_icon="📸",
    layout="wide"
)

# Cache the EasyOCR reader
@st.cache_resource(show_spinner=False)
def load_ocr():
    try:
        return easyocr.Reader(['en'], gpu=False)
    except Exception as e:
        st.error(f"Error loading OCR model: {str(e)}")
        return None

def draw_boxes(image, bounds, color=(0, 255, 0), width=2):
    """Draw bounding boxes on the image using PIL"""
    try:
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        elif not isinstance(image, Image.Image):
            raise ValueError("Unsupported image type")

        draw_image = image.copy()
        draw = ImageDraw.Draw(draw_image)

        for bound in bounds:
            p0, p1, p2, p3 = bound[0]
            draw.line([tuple(p0), tuple(p1), tuple(p2), tuple(p3), tuple(p0)],
                     fill=color, width=width)

        return draw_image
    except Exception as e:
        st.error(f"Error drawing boxes: {str(e)}")
        return image

def main():
    st.title("📸 Camera OCR App")
    st.write("Take a photo or upload an image to extract text")

    # Initialize session state if not exists
    if 'ocr_reader' not in st.session_state:
        with st.spinner("Loading OCR model..."):
            st.session_state.ocr_reader = load_ocr()

    # Create tabs for camera and file upload
    tab1, tab2 = st.tabs(["📸 Camera", "📁 File Upload"])

    with tab1:
        # Camera input
        camera_image = st.camera_input("Take a picture")
        
        if camera_image is not None:
            try:
                # Display original and processed images side by side
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Captured Image")
                    image = Image.open(camera_image)
                    st.image(image, use_container_width=True)

                if st.button("Extract Text from Photo", key="camera_extract"):
                    if st.session_state.ocr_reader is None:
                        st.error("OCR model failed to load. Please refresh the page.")
                        return

                    with st.spinner("Processing image..."):
                        try:
                            # Convert image to numpy array
                            image_np = np.array(image)
                            
                            # Perform OCR
                            results = st.session_state.ocr_reader.readtext(image_np)
                            
                            # Draw boxes on image
                            annotated_image = draw_boxes(image, results)
                            
                            with col2:
                                st.subheader("Detected Text Regions")
                                st.image(annotated_image, use_container_width=True)

                            # Display results
                            st.subheader("Extracted Text")
                            
                            if not results:
                                st.warning("No text was detected in the image.")
                            else:
                                extracted_text = ""
                                for result in results:
                                    text = result[1]
                                    confidence = result[2]
                                    extracted_text += f"{text}\n"
                                    st.write(f"📝 **Text:** {text}")
                                    st.write(f"🎯 **Confidence:** {confidence:.2f}")
                                    st.write("---")

                                # Download button
                                if extracted_text.strip():
                                    st.download_button(
                                        label="Download extracted text",
                                        data=extracted_text,
                                        file_name="extracted_text.txt",
                                        mime="text/plain"
                                    )

                        except Exception as e:
                            st.error(f"Error processing image: {str(e)}")

            except Exception as e:
                st.error(f"Error loading camera image: {str(e)}")

    with tab2:
        # File upload option
        uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file is not None:
            try:
                # Display original and processed images side by side
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Uploaded Image")
                    image = Image.open(uploaded_file)
                    st.image(image, use_container_width=True)

                if st.button("Extract Text from File", key="file_extract"):
                    if st.session_state.ocr_reader is None:
                        st.error("OCR model failed to load. Please refresh the page.")
                        return

                    with st.spinner("Processing image..."):
                        try:
                            # Convert image to numpy array
                            image_np = np.array(image)
                            
                            # Perform OCR
                            results = st.session_state.ocr_reader.readtext(image_np)
                            
                            # Draw boxes on image
                            annotated_image = draw_boxes(image, results)
                            
                            with col2:
                                st.subheader("Detected Text Regions")
                                st.image(annotated_image, use_container_width=True)

                            # Display results
                            st.subheader("Extracted Text")
                            
                            if not results:
                                st.warning("No text was detected in the image.")
                            else:
                                extracted_text = ""
                                for result in results:
                                    text = result[1]
                                    confidence = result[2]
                                    extracted_text += f"{text}\n"
                                    st.write(f"📝 **Text:** {text}")
                                    st.write(f"🎯 **Confidence:** {confidence:.2f}")
                                    st.write("---")

                                # Download button
                                if extracted_text.strip():
                                    st.download_button(
                                        label="Download extracted text",
                                        data=extracted_text,
                                        file_name="extracted_text.txt",
                                        mime="text/plain"
                                    )

                        except Exception as e:
                            st.error(f"Error processing image: {str(e)}")

            except Exception as e:
                st.error(f"Error loading uploaded file: {str(e)}")

    # Add information sidebar
    st.sidebar.title("ℹ️ Information")
    st.sidebar.write("""
    ### How to Use
    1. Choose either Camera or File Upload tab
    2. Take a photo or upload an image
    3. Click 'Extract Text' button
    4. View results and download text if needed
    
    ### Tips for Better Results
    - Ensure good lighting
    - Hold the camera steady
    - Keep text in focus
    - Avoid glare and shadows
    - Position text horizontally
    """)

if __name__ == "__main__":
    main()
