import streamlit as st
import cv2
import numpy as np
import time
from urllib.parse import urlparse, parse_qs

# Dictionary of content based on parameters
content_mapping = {
    "story1": {
        "title": "The Little Red Hen",
        "text": "Once upon a time...",
        "level": "beginner"
    },
    "story2": {
        "title": "Three Little Pigs",
        "text": "Once there were three pigs...",
        "level": "intermediate"
    }
}

def extract_story_id_from_url(url):
    """Extract story ID from URL parameters"""
    try:
        # Check if the URL is from te5tqr.streamlit.app
        parsed_url = urlparse(url)
        if "te5tqr.streamlit.app" in parsed_url.netloc:
            params = parse_qs(parsed_url.query)
            return params.get('story', [None])[0]
    except:
        return None

def main():
    st.title("QR Code Story Reader")
    
    # Initialize QR detector
    qr_detector = cv2.QRCodeDetector()
    
    # Initialize session states
    if 'camera_on' not in st.session_state:
        st.session_state.camera_on = False
    if 'current_story' not in st.session_state:
        st.session_state.current_story = None
    if 'last_scan' not in st.session_state:
        st.session_state.last_scan = None

    # Create two columns
    col1, col2 = st.columns([1, 1])

    with col1:
        # Camera toggle button
        if st.button("Toggle Camera"):
            st.session_state.camera_on = not st.session_state.camera_on
        
        # Camera placeholder
        camera_placeholder = st.empty()

    with col2:
        # Story display area
        story_container = st.container()

    if st.session_state.camera_on:
        cap = cv2.VideoCapture(0)
        
        while st.session_state.camera_on:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to access camera")
                break

            # Convert frame for display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect and decode QR code
            try:
                decoded_text, points, _ = qr_detector.detectAndDecode(frame)
                
                if decoded_text and points is not None:
                    # Draw outline
                    points = points.astype(np.int32)
                    cv2.polylines(frame_rgb, [points], True, (0, 255, 0), 2)
                    
                    # Process QR code data if it's a new scan
                    if decoded_text != st.session_state.last_scan:
                        story_id = extract_story_id_from_url(decoded_text)
                        
                        if story_id in content_mapping:
                            st.session_state.current_story = content_mapping[story_id]
                            st.session_state.last_scan = decoded_text
                            st.success(f"Loaded: {st.session_state.current_story['title']}")
            except:
                pass

            # Display camera feed
            camera_placeholder.image(frame_rgb)
            
            # Display story content
            with story_container:
                if st.session_state.current_story:
                    st.header(st.session_state.current_story["title"])
                    st.info(f"Reading Level: {st.session_state.current_story['level']}")
                    st.write(st.session_state.current_story["text"])
                else:
                    st.write("Scan a QR code to see the story")
            
            time.sleep(0.1)

        cap.release()
    else:
        # Display story when camera is off
        with story_container:
            if st.session_state.current_story:
                st.header(st.session_state.current_story["title"])
                st.info(f"Reading Level: {st.session_state.current_story['level']}")
                st.write(st.session_state.current_story["text"])
            else:
                st.write("Scan a QR code to see the story")

if __name__ == "__main__":
    main()
