import streamlit as st
import cv2
import numpy as np
import time
from urllib.parse import urlparse, parse_qs

# Dictionary of stories with clear structure
stories = {
    "story1": {
        "title": "The Little Red Hen",
        "content": """
        Once upon a time, there was a little red hen who lived on a farm. 
        She was friends with a lazy dog, a sleepy cat, and a noisy duck.

        One day, she found some wheat seeds and asked her friends, 
        "Who will help me plant these wheat seeds?"

        "Not I," said the dog.
        "Not I," said the cat.
        "Not I," said the duck.
        """,
        "level": "Beginner"
    },
    "story2": {
        "title": "The Three Little Pigs",
        "content": """
        Once there were three little pigs who left home to seek their fortune.
        The first little pig built a house of straw.
        The second little pig built a house of sticks.
        The third little pig built a house of bricks.
        """,
        "level": "Intermediate"
    }
}

def main():
    st.title("Story Reader")

    # Get story ID directly from URL parameters
    query_params = st.experimental_get_query_params()
    story_id = query_params.get('story', [None])[0]

    # If story ID is in URL, display that story
    if story_id and story_id in stories:
        story = stories[story_id]
        st.header(story["title"])
        st.info(f"Reading Level: {story['level']}")
        st.markdown(story["content"])
    else:
        st.info("Scan a QR code to read a story")

if __name__ == "__main__":
    main()
