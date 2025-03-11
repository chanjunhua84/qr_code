import streamlit as st

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
    
    # Get query parameters
    query_params = st.experimental_get_query_params()
    
    # Debug: Show current parameters
    st.write("Debug - URL Parameters:", query_params)
    
    # Get story ID from parameters
    story_id = None
    if 'story' in query_params:
        story_id = query_params['story'][0]
    
    # Debug: Show detected story ID
    st.write("Debug - Detected Story ID:", story_id)

    # Display story based on ID
    if story_id and story_id in stories:
        story = stories[story_id]
        st.header(story["title"])
        st.info(f"Reading Level: {story['level']}")
        st.markdown(story["content"])
    else:
        st.info("Please scan a valid story QR code")
        st.write("Available stories:", list(stories.keys()))

if __name__ == "__main__":
    main()
