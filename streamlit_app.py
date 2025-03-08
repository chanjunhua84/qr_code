import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import easyocr
import os

# Force CPU usage
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Set page configuration for full screen
st.set_page_config(
    page_title="Camera OCR App",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for full screen mobile camera
st.markdown("""
    <style>
        /* Hide Streamlit elements when camera is active */
        [data-testid="stToolbar"] {
            display: none;
        }
        
        .stApp {
            margin: 0;
            padding: 0;
            max-width: 100vw !important;
        }
        
        /* Full screen camera styling */
        .stCamera {
            position: fixed !important;
            min-width: 100vw !important;
            min-height: 100vh !important;
            max-width: 100vw !important;
            max-height: 100vh !important;
            width: 100vw !important;
            height: 100vh !important;
            left: 0;
            top: 0;
            z-index: 9999;
            background: black;
            padding: 0 !important;
            margin: 0 !important;
            border: none !important;
        }
        
        .stCamera > video {
            width: 100vw !important;
            height: 100vh !important;
            object-fit: cover !important;
            position: fixed !important;
            left: 0;
            top: 0;
        }
        
        .stCamera > button {
            position: fixed !important;
            bottom: 40px !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
            z-index: 10000 !important;
            width: 80px !important;
            height: 80px !important;
            border-radius: 50% !important;
            background-color: white !important;
            border: 4px solid #FF4B4B !important;
            padding: 0 !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.3) !important;
        }
        
        .stCamera > button:hover {
            background-color: #f8f8f8 !important;
        }
        
        /* Hide camera when not active */
        .camera-hidden {
            display: none !important;
        }
        
        /* Custom button styling */
        .stButton > button {
            width: 100%;
            height: 3.5rem;
            font-size: 1.2rem;
            background-color: #FF4B4B;
            color: white;
            border: none;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        /* Result card styling */
        .result-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Mobile-friendly container */
        .mobile-container {
            padding: 1rem;
            max-width: 100vw;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 4rem;
        }
        
        /* Hide header when camera is active */
        .camera-active header {
            display: none !important;
        }
        
        /* Adjust main content padding */
        .main .block-container {
            padding: 1rem !important;
            max-width: 100vw !important;
        }
        
        /* Make images full width on mobile */
        .stImage > img {
            width: 100% !important;
            max-width: 100% !important;
        }
        
        /* Responsive text sizing */
        @media screen and (max-width: 640px) {
            .stMarkdown h1 {
                font-size: 1.5rem !important;
            }
            .stMarkdown h2 {
                font-size: 1.3rem !important;
            }
            .stMarkdown h3 {
                font-size: 1.1rem !important;
            }
        }
    </style>
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
        st.markdown("### Original Photo")
        st.image(image, use_container_width=True)
        
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
        if not st.session_state.show_camera:
            st.button("📸 Launch Camera", key="launch_camera", 
                     on_click=lambda: setattr(st.session_state, 'show_camera', True))
        
        if st.session_state.show_camera:
            camera_col = st.container()
            with camera_col:
                camera_image = st.camera_input("", key="camera")
                
                if camera_image is not None:
                    try:
                        image = Image.open(camera_image)
                        st.session_state.show_camera = False
                        process_image(image)
                    except Exception as e:
                        st.error(f"Error processing camera image: {str(e)}")

    with tab2:
        uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            try:
                image = Image.open(uploaded_file)
                process_image(image)
            except Exception as e:
                st.error(f"Error processing uploaded image: {str(e)}")

    # Tips in expandable section
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
