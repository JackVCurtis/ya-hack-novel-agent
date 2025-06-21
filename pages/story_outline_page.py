"""
Story Outline page for the YA Novel Generator.
"""
import streamlit as st
from .abstract_page import AbstractPage
from outliner_agent import OutlinerAgent


class StoryOutlinePage(AbstractPage):
    """Page for generating story outline"""
    
    def render(self):
        """Render the story outline page"""
        st.header("📋 Story Outline")
        st.markdown("Generate a 17-chapter outline following the Hero's Journey structure.")

        if not self.check_prerequisites(['story_concept', 'generated_setting', 'generated_characters', 'generated_plot_summary']):
            self.show_prerequisites_warning(['Story Concept', 'World Building', 'Character Creation', 'Plot Summary'])
            return

        # Outliner Style Guide Section
        self.create_style_guide_section(
            OutlinerAgent,
            'outliner_style_guide',
            'Outliner Writing Style Guide',
            'Guidelines for story structure and outlining'
        )

        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Story Elements Ready")
            st.write("✅ Story concept defined")
            st.write("✅ World building complete")
            st.write("✅ Characters created")
            st.write(f"✅ {len(st.session_state.generated_characters)} characters ready")
            st.write("✅ Plot summary created")
            
            if st.button("📚 Generate 17-Chapter Outline", type="primary"):
                with st.spinner("Creating your story outline..."):
                    try:
                        # Use custom style guide if available
                        custom_style = st.session_state.get('outliner_style_guide')
                        outliner = OutlinerAgent(
                            model="gpt-4o-mini",
                            writing_style_guide=custom_style
                        )
                        outline = outliner.generate_outline(
                            st.session_state.story_concept,
                            st.session_state.generated_setting,
                            st.session_state.generated_characters,
                            st.session_state.generated_plot_summary,
                            verbose=False
                        )
                        st.session_state.generated_outline = outline
                        self.save_current_story()  # Auto-save
                        st.success("✅ Story outline complete!")
                        st.info("💾 Story automatically saved to database.")
                    except Exception as e:
                        st.error(f"Error generating outline: {str(e)}")
        
        with col2:
            st.subheader("Generated Outline")
            if st.session_state.generated_outline:
                st.markdown("### 📋 Your Story Outline")

                # Editable text area for the outline
                edited_outline = st.text_area(
                    "Edit your story outline:",
                    value=st.session_state.generated_outline,
                    height=400,
                    help="You can edit the generated outline directly here",
                    key="outline_editor"
                )

                # Update session state if content was edited
                if edited_outline != st.session_state.generated_outline:
                    st.session_state.generated_outline = edited_outline
                    self.save_current_story()  # Auto-save changes
                    st.success("✅ Outline updated and saved!")

                # Option to regenerate
                if st.button("🔄 Regenerate Outline"):
                    with st.spinner("Regenerating outline..."):
                        try:
                            # Use custom style guide if available
                            custom_style = st.session_state.get('outliner_style_guide')
                            outliner = OutlinerAgent(
                                model="gpt-4o-mini",
                                writing_style_guide=custom_style
                            )
                            outline = outliner.generate_outline(
                                st.session_state.story_concept,
                                st.session_state.generated_setting,
                                st.session_state.generated_characters,
                                st.session_state.generated_plot_summary,
                                verbose=False
                            )
                            st.session_state.generated_outline = outline
                            self.save_current_story()  # Auto-save
                            st.success("✅ Outline regenerated!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error regenerating outline: {str(e)}")
            else:
                st.info("Click 'Generate 17-Chapter Outline' to create your story structure.")
