import streamlit as st
import torch
from transformers import pipeline

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
    
    # Initialize summarizer with caching
    @st.cache_resource
    def load_summarizer():
        return pipeline("summarization", 
                       model="facebook/bart-large-cnn", 
                       device=0 if torch.cuda.is_available() else -1)
    
    try:
        summarizer = load_summarizer()
    except Exception as e:
        st.error(f"Error loading summarizer: {e}")
        summarizer = None
    
    # Get query parameters
    query_params = st.experimental_get_query_params()
    
    # Get story ID from parameters
    story_id = None
    if 'story' in query_params:
        story_id = query_params['story'][0]

    # Display story based on ID
    if story_id and story_id in stories:
        story = stories[story_id]
        st.header(story["title"])
        st.markdown(story["content"])
        
        # Generate and display summary
        if summarizer:
            try:
                with st.spinner('Generating summary...'):
                    summary = summarizer(story["content"], 
                                       max_length=150, 
                                       min_length=50, 
                                       do_sample=False)[0]["summary_text"]
                    st.subheader("Summary")
                    st.markdown(summary)
            except Exception as e:
                st.error(f"Error generating summary: {e}")
    else:
        st.info("Please scan a valid story QR code")
        st.write("Available stories:", list(stories.keys()))

if __name__ == "__main__":
    main()
