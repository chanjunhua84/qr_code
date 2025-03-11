import streamlit as st
import cv2
import numpy as np
import time
from urllib.parse import urlparse, parse_qs

# Dictionary of stories
stories = {
    "story1": """
    Title: The Little Red Hen

    Once upon a time, there was a little red hen who lived on a farm. 
    She was friends with a lazy dog, a sleepy cat, and a noisy duck.

    One day, she found some wheat seeds and asked her friends, 
    "Who will help me plant these wheat seeds?"

    "Not I," said the dog.
    "Not I," said the cat.
    "Not I," said the duck.
    """,
    
    "story2": """
    Title: The Three Little Pigs

    Once there were three little pigs who left home to seek their fortune.
    The first little pig built a house of straw.
    The second little pig built a house of sticks.
    The third little pig built a house of bricks.
    """,
}

def extract_story_id(url):
    """Extract story ID from the Streamlit app URL"""
    try:
        parsed_url = urlparse(url)
        # Check if it's our specific Streamlit app
        if "te5tqr.streamlit.app" in parsed_url.netloc:
            params = parse_qs(parsed_url.query)
            return params.get('story', [None])[0]
    except:
        return None

def main():
    st.title("Story Reader")

    # Initialize session state
    if 'camera_on' not in st.session_state:
        st.session_state.camera_on = False
    if 'current_story' not in st.session_state:
        st.session_state.current_story = None

    # Create columns for layout
    col1, col2 = st.columns([1, 2])

    with col1:
        # Camera controls
        if st.button("📷 Toggle Camera"):
            st.session_state.camera_on = not st.session_state.camera_on
        
        camera_placeholder = st.empty()

    with col2:
        # Story display
        story_placeholder = st.empty()

    # QR code scanning logic
    if st.session_state.camera_on:
        cap = cv2.VideoCapture(0)  # Use default camera
        qr_detector = cv2.QRCodeDetector()

        while st.session_state.camera_on:
            ret, frame = cap.read()
            if not ret:
                st.error("Cannot access camera")
                break

            # Convert frame for display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect QR code
            try:
                decoded_text, points, _ = qr_detector.detectAndDecode(frame)
                
                if decoded_text and points is not None:
                    # Draw green rectangle around QR code
                    points = points.astype(np.int32)
                    cv2.polylines(frame_rgb, [points], True, (0, 255, 0), 3)
                    
                    # Process URL if it's from our app
                    story_id = extract_story_id(decoded_text)
                    if story_id and story_id in stories:
                        st.session_state.current_story = stories[story_id]
                        st.success(f"Story loaded successfully!")
            except:
                pass

            # Show camera feed
            camera_placeholder.image(frame_rgb, channels="RGB")

            # Display current story
            if st.session_state.current_story:
                story_placeholder.markdown(st.session_state.current_story)
            else:
                story_placeholder.markdown("Scan a QR code to read a story...")

            time.sleep(0.1)

        cap.release()
    else:
        # Display current story when camera is off
        if st.session_state.current_story:
            story_placeholder.markdown(st.session_state.current_story)
        else:
            story_placeholder.markdown("Scan a QR code to read a story...")

if __name__ == "__main__":
    main()
