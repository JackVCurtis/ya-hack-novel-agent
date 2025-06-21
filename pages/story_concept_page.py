"""
Story Concept page for the YA Novel Generator.
"""
import streamlit as st
from .abstract_page import AbstractPage


class StoryConceptPage(AbstractPage):
    """Page for entering basic story concept and setting"""
    
    def render(self):
        """Render the story concept page"""
        st.header("📝 Story Concept & Setting")
        st.markdown("Start by defining your story's core concept and initial setting description.")
        
        with st.form("story_concept_form"):
            st.subheader("Story Concept")
            story_concept = st.text_area(
                "Describe your story concept:",
                placeholder="A seemingly powerless student at a magical academy discovers they have a rare and dangerous ability that could either save or destroy both the academy and the world below.",
                height=100,
                help="Describe the main plot, conflict, or theme of your story"
            )
            
            st.subheader("Initial Setting Description")
            setting_description = st.text_area(
                "Describe your story's setting:",
                placeholder="A prestigious boarding academy built on a floating island above a post-apocalyptic wasteland. The academy trains gifted teenagers in elemental magic, but students are ranked in a strict hierarchy based on their magical abilities.",
                height=100,
                help="Describe the world, time period, and environment where your story takes place"
            )
            
            st.subheader("Character Roles")
            col1, col2 = st.columns(2)
            
            with col1:
                protagonist_desc = st.text_area(
                    "Protagonist Description:",
                    placeholder="A 16-year-old student who appears powerless but has hidden abilities...",
                    height=80,
                    help="Brief description of your main character"
                )
            
            with col2:
                antagonist_desc = st.text_area(
                    "Antagonist Description:",
                    placeholder="The academy's top student who views the protagonist as a threat...",
                    height=80,
                    help="Brief description of your main opposing character"
                )
            
            submitted = st.form_submit_button("Save Story Elements", type="primary")
            
            if submitted:
                if story_concept and setting_description and protagonist_desc and antagonist_desc:
                    # Store in session state
                    st.session_state.story_concept = story_concept
                    st.session_state.initial_setting = setting_description
                    st.session_state.protagonist_desc = protagonist_desc
                    st.session_state.antagonist_desc = antagonist_desc

                    # Auto-save to database
                    self.save_current_story()

                    st.success("✅ Story elements saved! Move to 'World Building' to generate your detailed setting.")
                    st.info("💾 Story automatically saved to database.")
                else:
                    st.error("Please fill in all fields before proceeding.")
        
        # Display saved elements if they exist
        if hasattr(st.session_state, 'story_concept'):
            st.subheader("📋 Saved Story Elements")
            with st.expander("View Saved Elements"):
                st.write("**Story Concept:**", st.session_state.story_concept)
                st.write("**Setting:**", st.session_state.initial_setting)
                st.write("**Protagonist:**", st.session_state.protagonist_desc)
                st.write("**Antagonist:**", st.session_state.antagonist_desc)
