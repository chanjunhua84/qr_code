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

# Custom CSS to maximize camera view and style buttons
st.markdown("""
    <style>
        /* Full screen camera styling */
        .stCamera {
            position: fixed !important;
            top: 0;
            left: 0;
            width: 100vw !important;
            height: 100vh !important;
            max-width: none !important;
            max-height: none !important;
            z-index: 1000;
            background: black;
        }
        
        .stCamera > video {
            width: 100vw !important;
            height: 100vh !important;
            object-fit: cover !important;
        }
        
        .stCamera > button {
            position: fixed !important;
            bottom: 20px !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
            z-index: 1001 !important;
            width: 80px !important;
            height: 80px !important;
            border-radius: 50% !important;
            background-color: white !important;
            border: 3px solid #FF4B4B !important;
        }
        
        /* Hide camera when not active */
        .camera-hidden {
            display: none !important;
        }
        
        /* Custom button styling */
        .custom-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.5rem 1rem;
            background-color: #FF4B4B;
            color: white;
            border: none;
            border-radius: 0.5rem;
            font-size: 1.2rem;
            cursor: pointer;
            margin: 1rem 0;
            width: 100%;
            height: 3rem;
            text-decoration: none;
        }
        
        .custom-button:hover {
            background-color: #FF3333;
        }
        
        /* Result card styling */
        .result-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Hide Streamlit elements when camera is active */
        .camera-active .main {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# JavaScript to handle camera visibility
st.markdown("""
    <script>
        // Function to toggle camera visibility
        function toggleCamera() {
            const camera = document.querySelector('.stCamera');
            if (camera) {
                camera.classList.toggle('camera-hidden');
            }
        }
    </script>
""", unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def load_ocr():
    try:
        return easyocr.Reader(['en'], gpu=False)
    except Exception as e:
        st.error(f"Error loading OCR model: {str(e)}")
        return None

def draw_boxes(image, bounds, color=(0, 255, 0), width=3):
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

def process_image(image):
    try:
        # Convert and process image
        image_np = np.array(image)
        results = st.session_state.ocr_reader.readtext(image_np)
        
        # Show results in a clean layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Original Photo")
            st.image(image, use_container_width=True)
        
        with col2:
            st.markdown("### Detected Text Regions")
            annotated_image = draw_boxes(image, results)
            st.image(annotated_image, use_container_width=True)
        
        # Show extracted text in a clean format
        st.markdown("### 📝 Extracted Text")
        if not results:
            st.warning("No text was detected. Please try again with a clearer photo.")
        else:
            extracted_text = ""
            for result in results:
                text, confidence = result[1], result[2]
                extracted_text += f"{text}\n"
                st.markdown(f"""
                    <div class="result-card">
                        <p style='font-size: 1.2rem; margin: 0;'>{text}</p>
                        <p style='color: #666; margin: 0;'>Confidence: {confidence:.2f}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Download button
            st.download_button(
                "💾 Download Extracted Text",
                extracted_text,
                file_name="extracted_text.txt",
                mime="text/plain",
                use_container_width=True
            )
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")

def main():
    st.title("📸 Smart Text Scanner")
    
    # Initialize OCR
    if 'ocr_reader' not in st.session_state:
        with st.spinner("Loading OCR model..."):
            st.session_state.ocr_reader = load_ocr()

    # Initialize session state for camera control
    if 'show_camera' not in st.session_state:
        st.session_state.show_camera = False

    # Create two tabs
    tab1, tab2 = st.tabs([
        "📸 Take Photo",
        "📁 Upload Image"
    ])

    with tab1:
        st.markdown("### Take a Photo of Text")
        
        # Custom button to launch camera
        if st.button("📸 Launch Camera", use_container_width=True):
            st.session_state.show_camera = True
            st.experimental_rerun()
        
        # Show camera only when button is clicked
        if st.session_state.show_camera:
            camera_image = st.camera_input("", key="camera")
            
            if camera_image is not None:
                try:
                    image = Image.open(camera_image)
                    st.session_state.show_camera = False  # Hide camera after capture
                    process_image(image)
                except Exception as e:
                    st.error(f"Error processing camera image: {str(e)}")

    with tab2:
        st.markdown("### Upload an Image")
        uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            try:
                image = Image.open(uploaded_file)
                process_image(image)
            except Exception as e:
                st.error(f"Error processing uploaded image: {str(e)}")

    # Helpful tips in expandable section
    with st.expander("📌 Tips for Better Results"):
        st.markdown("""
            ### For Best Results:
            - Ensure good lighting
            - Hold the camera steady
            - Keep text horizontal
            - Avoid glare and shadows
            - Position text within frame
            - Make sure text is in focus
        """)

if __name__ == "__main__":
    main()
