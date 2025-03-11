import streamlit as st
from urllib.parse import parse_qs

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

def main():
    st.title("Reading App")

    # Get query parameters
    query_params = st.query_params()
    
    # Handle story ID from URL
    story_id = query_params.get('story', [None])[0]
    reading_level = query_params.get('level', [None])[0]

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    
    # Display content based on URL parameters
    if story_id and story_id in content_mapping:
        story = content_mapping[story_id]
        
        # Display story content
        st.header(story["title"])
        
        # Show reading level if specified in URL
        if reading_level:
            st.info(f"Reading Level: {reading_level}")
        
        # Display story text
        st.write(story["text"])
        
        # Additional features
        st.markdown("---")
        if st.button("Mark as Complete"):
            st.success("Progress saved!")
            
    else:
        st.warning("Please select a story or provide a valid story ID in the URL")
        
        # Show available stories
        st.subheader("Available Stories")
        for id, story in content_mapping.items():
            if st.button(story["title"]):
                # Update URL with selected story
                new_params = {"story": id}
                st.experimental_set_query_params(**new_params)
                st.rerun()

    # Show current URL parameters (for debugging)
    st.sidebar.subheader("Current URL Parameters")
    st.sidebar.write(query_params)

if __name__ == "__main__":
    main()
