"""
World Building page for the YA Novel Generator.
"""
import streamlit as st
from .abstract_page import AbstractPage
from worldbuilder_agent import WorldbuilderAgent


class WorldBuildingPage(AbstractPage):
    """Page for generating detailed world building"""
    
    def render(self):
        """Render the world building page"""
        st.header("🌍 World Building")
        st.markdown("Generate a detailed setting description based on your story concept.")

        if not self.check_prerequisites(['story_concept']):
            self.show_prerequisites_warning(['Story Concept'])
            return

        # Worldbuilder Style Guide Section
        self.create_style_guide_section(
            WorldbuilderAgent,
            'worldbuilder_style_guide',
            'Worldbuilder Writing Style Guide',
            'Guidelines for world and setting descriptions'
        )

        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("Your Story Elements")
            st.write("**Concept:**", st.session_state.story_concept[:100] + "...")
            st.write("**Initial Setting:**", st.session_state.initial_setting[:100] + "...")

            if st.button("🎯 Generate Detailed Setting", type="primary"):
                with st.spinner("Creating your world..."):
                    try:
                        # Use custom style guide if available
                        custom_style = st.session_state.get('worldbuilder_style_guide')
                        worldbuilder = WorldbuilderAgent(
                            model="gpt-4o-mini",
                            writing_style_guide=custom_style
                        )
                        detailed_setting = worldbuilder.generate_setting(
                            st.session_state.initial_setting,
                            st.session_state.story_concept,
                            verbose=False
                        )
                        st.session_state.generated_setting = detailed_setting
                        self.save_current_story()  # Auto-save
                        st.success("✅ World building complete!")
                        st.info("💾 Story automatically saved to database.")
                    except Exception as e:
                        st.error(f"Error generating setting: {str(e)}")
        
        with col2:
            st.subheader("Generated Setting")
            if st.session_state.generated_setting:
                st.markdown("### 🌍 Your Generated World")

                # Editable text area for the setting
                edited_setting = st.text_area(
                    "Edit your setting description:",
                    value=st.session_state.generated_setting,
                    height=300,
                    help="You can edit the generated setting description directly here",
                    key="setting_editor"
                )

                # Update session state if content was edited
                if edited_setting != st.session_state.generated_setting:
                    st.session_state.generated_setting = edited_setting
                    self.save_current_story()  # Auto-save changes
                    st.success("✅ Setting updated and saved!")

                # Option to regenerate
                if st.button("🔄 Regenerate Setting"):
                    with st.spinner("Regenerating world..."):
                        try:
                            worldbuilder = WorldbuilderAgent(model="gpt-4o-mini")
                            detailed_setting = worldbuilder.generate_setting(
                                st.session_state.initial_setting,
                                st.session_state.story_concept,
                                verbose=False
                            )
                            st.session_state.generated_setting = detailed_setting
                            self.save_current_story()  # Auto-save
                            st.success("✅ Setting regenerated!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error regenerating setting: {str(e)}")
            else:
                st.info("Click 'Generate Detailed Setting' to create your world description.")
