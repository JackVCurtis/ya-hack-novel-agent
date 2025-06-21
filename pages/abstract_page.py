"""
Abstract base class for Streamlit pages in the YA Novel Generator.
"""
from abc import ABC, abstractmethod
import streamlit as st


class AbstractPage(ABC):
    """
    Abstract base class for all pages in the YA Novel Generator Streamlit app.
    
    Each page should inherit from this class and implement the render method.
    This provides a consistent interface and shared functionality across all pages.
    """
    
    def __init__(self):
        """Initialize the page."""
        pass
    
    @abstractmethod
    def render(self):
        """
        Render the page content.
        
        This method should contain all the Streamlit UI code for the page.
        It will be called by the main app to display the page content.
        """
        pass
    
    def save_current_story(self):
        """Save current session state to database"""
        from streamlit_app import save_current_story
        save_current_story()
    
    def check_prerequisites(self, required_fields):
        """
        Check if required session state fields exist and have values.
        
        Args:
            required_fields (list): List of session state field names that are required
            
        Returns:
            bool: True if all prerequisites are met, False otherwise
        """
        for field in required_fields:
            if not hasattr(st.session_state, field) or not st.session_state.get(field):
                return False
        return True
    
    def show_prerequisites_warning(self, missing_steps):
        """
        Show a warning message about missing prerequisites.
        
        Args:
            missing_steps (list): List of step names that need to be completed first
        """
        if len(missing_steps) == 1:
            st.warning(f"⚠️ Please complete the '{missing_steps[0]}' step first.")
        else:
            steps_text = "', '".join(missing_steps[:-1]) + f"' and '{missing_steps[-1]}"
            st.warning(f"⚠️ Please complete the '{steps_text}' steps first.")
    
    def create_style_guide_section(self, agent_class, style_guide_key, section_title, help_text):
        """
        Create a collapsible style guide section for an agent.
        
        Args:
            agent_class: The agent class to get default style guide from
            style_guide_key (str): Session state key for storing the style guide
            section_title (str): Title for the expandable section
            help_text (str): Help text for the text area
        """
        with st.expander(f"✍️ {section_title}", expanded=False):
            st.markdown(f"Customize how the AI {help_text.lower()}:")
            
            # Get default style guide
            agent = agent_class()
            default_guide = agent._get_default_style_guide()
            
            current_guide = st.session_state.get(style_guide_key) or default_guide
            guide = st.text_area(
                f"{section_title}:",
                value=current_guide,
                height=150,
                key=f"{style_guide_key}_input_main",
                help=help_text
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Style Guide", key=f"save_{style_guide_key}"):
                    st.session_state[style_guide_key] = guide
                    self.save_current_story()
                    st.success(f"✅ {section_title} saved!")
            
            with col2:
                if st.button("🔄 Reset to Default", key=f"reset_{style_guide_key}_main"):
                    st.session_state[style_guide_key] = None
                    self.save_current_story()
                    st.success("✅ Reset to default style guide!")
                    st.rerun()
