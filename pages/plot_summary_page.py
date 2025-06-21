"""
Plot Summary page for the YA Novel Generator.
"""
import streamlit as st
from .abstract_page import AbstractPage
from plot_summary_agent import PlotSummaryAgent


class PlotSummaryPage(AbstractPage):
    """Page for generating and editing plot summaries"""
    
    def render(self):
        """Render the plot summary page"""
        st.header("📖 Plot Summary")
        st.markdown("Generate a compelling single paragraph plot summary that captures the essence of your story.")

        if not self.check_prerequisites(['story_concept', 'generated_setting', 'generated_characters']):
            self.show_prerequisites_warning(['Story Concept', 'World Building', 'Character Creation'])
            return

        # Plot Summary Style Guide Section
        self.create_style_guide_section(
            PlotSummaryAgent,
            'plot_summary_style_guide',
            'Plot Summary Writing Style Guide',
            'Guidelines for creating compelling plot summaries'
        )

        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Generate Plot Summary")
            
            st.markdown("""
            **What is a plot summary?**
            
            A plot summary is a single paragraph that captures:
            - The protagonist and their world
            - The main conflict or challenge
            - What's at stake
            - The journey ahead
            
            It serves as a guide for creating your detailed outline and chapters.
            """)
            
            if st.button("📝 Generate Plot Summary", type="primary"):
                with st.spinner("Creating your plot summary..."):
                    try:
                        # Use custom style guide if available
                        custom_style = st.session_state.get('plot_summary_style_guide')
                        plot_agent = PlotSummaryAgent(
                            model="gpt-4o-mini",
                            writing_style_guide=custom_style
                        )

                        plot_summary = plot_agent.generate_plot_summary(
                            st.session_state.story_concept,
                            st.session_state.generated_setting,
                            st.session_state.generated_characters,
                            verbose=False
                        )
                        st.session_state.generated_plot_summary = plot_summary
                        self.save_current_story()  # Auto-save
                        st.success("✅ Plot summary created!")
                        st.info("💾 Story automatically saved to database.")
                    except Exception as e:
                        st.error(f"Error generating plot summary: {str(e)}")
            
            # Regenerate button if plot summary exists
            if st.session_state.get('generated_plot_summary'):
                st.markdown("---")
                if st.button("🔄 Regenerate Plot Summary", type="secondary"):
                    with st.spinner("Regenerating plot summary..."):
                        try:
                            # Use custom style guide if available
                            custom_style = st.session_state.get('plot_summary_style_guide')
                            plot_agent = PlotSummaryAgent(
                                model="gpt-4o-mini",
                                writing_style_guide=custom_style
                            )

                            plot_summary = plot_agent.generate_plot_summary(
                                st.session_state.story_concept,
                                st.session_state.generated_setting,
                                st.session_state.generated_characters,
                                verbose=False
                            )
                            st.session_state.generated_plot_summary = plot_summary
                            self.save_current_story()  # Auto-save
                            st.success("✅ Plot summary regenerated!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error regenerating plot summary: {str(e)}")
        
        with col2:
            st.subheader("Your Plot Summary")
            if st.session_state.get('generated_plot_summary'):
                # Display current plot summary with editing capability
                with st.container():
                    st.markdown("**Current Plot Summary:**")
                    
                    # Editable text area for the plot summary
                    edited_summary = st.text_area(
                        "Edit your plot summary:",
                        value=st.session_state.generated_plot_summary,
                        height=200,
                        help="You can edit the plot summary directly here. This will guide your outline and chapter creation.",
                        key="plot_summary_editor"
                    )

                    # Update session state if content was edited
                    if edited_summary != st.session_state.generated_plot_summary:
                        st.session_state.generated_plot_summary = edited_summary
                        self.save_current_story()  # Auto-save changes
                        st.success("✅ Plot summary updated and saved!")
                
                # Show word count and analysis
                word_count = len(st.session_state.generated_plot_summary.split())
                st.info(f"📊 Word count: {word_count} words")
                
                if word_count < 50:
                    st.warning("⚠️ Your plot summary might be too short. Consider adding more detail about the conflict and stakes.")
                elif word_count > 200:
                    st.warning("⚠️ Your plot summary might be too long. Consider condensing to focus on the core story elements.")
                else:
                    st.success("✅ Good length for a plot summary!")
                
                # Show how this will be used
                st.markdown("---")
                st.markdown("**How this will be used:**")
                st.markdown("""
                - 📋 **Story Outline**: Your outline will expand on this summary
                - ✍️ **Chapter Writing**: Each chapter will serve this overall plot
                - 🎯 **Story Focus**: Keeps your narrative on track
                """)
                
            else:
                st.info("Click 'Generate Plot Summary' to create a compelling summary of your story.")
                
                # Show preview of what will be used
                st.markdown("**Preview of story elements:**")
                
                with st.expander("📝 Story Concept", expanded=False):
                    st.write(st.session_state.story_concept[:200] + "..." if len(st.session_state.story_concept) > 200 else st.session_state.story_concept)
                
                with st.expander("🌍 Setting", expanded=False):
                    st.write(st.session_state.generated_setting[:200] + "..." if len(st.session_state.generated_setting) > 200 else st.session_state.generated_setting)
                
                with st.expander("👥 Characters", expanded=False):
                    for role, description in st.session_state.generated_characters.items():
                        st.write(f"**{role.title()}**: {description[:100]}...")
