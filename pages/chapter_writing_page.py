"""
Chapter Writing page for the YA Novel Generator.
"""
import streamlit as st
import time
from .abstract_page import AbstractPage
from chapter_agent import ChapterAgent


class ChapterWritingPage(AbstractPage):
    """Page for writing individual chapters"""
    
    def render(self):
        """Render the chapter writing page"""
        st.header("✍️ Chapter Writing")
        st.markdown("Write individual chapters based on your story outline.")

        if not self.check_prerequisites(['story_concept', 'generated_setting', 'generated_characters', 'generated_outline']):
            self.show_prerequisites_warning(['Story Concept', 'World Building', 'Character Creation', 'Story Outline'])
            return

        # Chapter Style Guide Section
        self.create_style_guide_section(
            ChapterAgent,
            'chapter_style_guide',
            'Chapter Writing Style Guide',
            'Guidelines for chapter writing and narrative style'
        )

        col1, col2 = st.columns([1, 2])
        
        with col1:
            self._render_chapter_selection_section()
            st.markdown("---")
            self._render_generate_all_chapters_section()
        
        with col2:
            self._render_generated_chapters_section()
    
    def _render_chapter_selection_section(self):
        """Render the chapter selection section"""
        st.subheader("Chapter Selection")
        
        chapter_number = st.selectbox(
            "Select chapter to write:",
            options=list(range(1, 18)),
            format_func=lambda x: f"Chapter {x}"
        )
        
        # Show outline for selected chapter if available
        if st.session_state.generated_outline:
            st.subheader("Chapter Outline")
            # This is a simplified approach - in a real app you'd parse the outline
            st.info("📝 Use the full outline below to extract the specific chapter details")
        
        if st.button(f"✍️ Write Chapter {chapter_number}", type="primary"):
            with st.spinner(f"Writing Chapter {chapter_number}..."):
                try:
                    # Use custom style guide if available
                    custom_style = st.session_state.get('chapter_style_guide')
                    chapter_writer = ChapterAgent(
                        model="gpt-4o-mini",
                        writing_style_guide=custom_style
                    )

                    # Get previous chapter if it exists
                    previous_chapter = None
                    if chapter_number > 1 and (chapter_number - 1) in st.session_state.generated_chapters:
                        previous_chapter = st.session_state.generated_chapters[chapter_number - 1]

                    # Using the full outline for now - in a real app, you'd extract the specific chapter outline
                    chapter = chapter_writer.write_chapter(
                        chapter_outline=st.session_state.generated_outline,
                        characters=st.session_state.generated_characters,
                        setting_description=st.session_state.generated_setting,
                        chapter_number=chapter_number,
                        previous_chapter=previous_chapter,
                        plot_summary=st.session_state.get('generated_plot_summary'),
                        verbose=False
                    )

                    st.session_state.generated_chapters[chapter_number] = chapter
                    self.save_current_story()  # Auto-save
                    st.success(f"✅ Chapter {chapter_number} complete!")
                    st.info("💾 Story automatically saved to database.")
                except Exception as e:
                    st.error(f"Error writing chapter: {str(e)}")
    
    def _render_generate_all_chapters_section(self):
        """Render the generate all chapters section"""
        st.subheader("📚 Generate All Chapters")

        # Show progress information
        completed_chapters = set(st.session_state.generated_chapters.keys()) if st.session_state.generated_chapters else set()
        remaining_chapters = set(range(1, 18)) - completed_chapters

        if completed_chapters:
            st.write(f"**Completed:** {len(completed_chapters)}/17 chapters")
            st.write(f"**Completed chapters:** {', '.join(map(str, sorted(completed_chapters)))}")

        if remaining_chapters:
            st.write(f"**Remaining:** {len(remaining_chapters)} chapters")
            st.write(f"**Remaining chapters:** {', '.join(map(str, sorted(remaining_chapters)))}")

            # Options for generation
            col_a, col_b = st.columns(2)

            with col_a:
                if st.button("📖 Generate All Remaining Chapters", type="primary", help="Generate all remaining chapters sequentially"):
                    self._generate_all_chapters(remaining_chapters)

            with col_b:
                self._render_regenerate_all_confirmation(remaining_chapters)
        else:
            st.success("🎉 All 17 chapters have been generated!")
            self._render_regenerate_complete_confirmation()
    
    def _render_regenerate_all_confirmation(self, remaining_chapters):
        """Render regenerate all chapters confirmation"""
        # Use session state to handle confirmation
        if 'confirm_regenerate_all' not in st.session_state:
            st.session_state.confirm_regenerate_all = False

        if not st.session_state.confirm_regenerate_all:
            if st.button("🔄 Regenerate All 17 Chapters", type="secondary", help="Regenerate all chapters from scratch"):
                if st.session_state.generated_chapters:
                    st.session_state.confirm_regenerate_all = True
                    st.rerun()
                else:
                    self._generate_all_chapters(set(range(1, 18)))
        else:
            st.warning("⚠️ This will overwrite all existing chapters!")
            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button("✅ Confirm Regenerate", type="secondary"):
                    st.session_state.confirm_regenerate_all = False
                    self._generate_all_chapters(set(range(1, 18)))
            with col_cancel:
                if st.button("❌ Cancel", type="secondary"):
                    st.session_state.confirm_regenerate_all = False
                    st.rerun()
    
    def _render_regenerate_complete_confirmation(self):
        """Render regenerate confirmation when all chapters are complete"""
        # Use session state to handle confirmation for regenerating all when complete
        if 'confirm_regenerate_complete' not in st.session_state:
            st.session_state.confirm_regenerate_complete = False

        if not st.session_state.confirm_regenerate_complete:
            if st.button("🔄 Regenerate All 17 Chapters", type="secondary", help="Regenerate all chapters from scratch"):
                st.session_state.confirm_regenerate_complete = True
                st.rerun()
        else:
            st.warning("⚠️ This will overwrite all existing chapters!")
            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button("✅ Confirm Regenerate All", type="secondary"):
                    st.session_state.confirm_regenerate_complete = False
                    self._generate_all_chapters(set(range(1, 18)))
            with col_cancel:
                if st.button("❌ Cancel Regenerate", type="secondary"):
                    st.session_state.confirm_regenerate_complete = False
                    st.rerun()

    def _render_generated_chapters_section(self):
        """Render the generated chapters section"""
        st.subheader("Generated Chapters")

        if st.session_state.generated_chapters:
            # Show list of completed chapters
            completed_chapters = sorted(map(int, st.session_state.generated_chapters.keys()))
            st.write(f"**Completed Chapters:** {', '.join(map(str, completed_chapters))}")

            # Chapter viewer and editor
            if completed_chapters:
                view_chapter = st.selectbox(
                    "View/Edit chapter:",
                    options=completed_chapters,
                    format_func=lambda x: f"Chapter {x}",
                    key="chapter_selector"
                )

                if view_chapter in st.session_state.generated_chapters:
                    st.subheader(f"📖 Chapter {view_chapter}")

                    # Editable text area for the chapter
                    edited_chapter = st.text_area(
                        f"Edit Chapter {view_chapter}:",
                        value=st.session_state.generated_chapters[view_chapter],
                        height=500,
                        help=f"You can edit Chapter {view_chapter} directly here",
                        key=f"chapter_editor_{view_chapter}"
                    )

                    # Update session state if content was edited
                    if edited_chapter != st.session_state.generated_chapters[view_chapter]:
                        st.session_state.generated_chapters[view_chapter] = edited_chapter
                        self.save_current_story()  # Auto-save changes
                        st.success(f"✅ Chapter {view_chapter} updated and saved!")

                    # Option to delete chapter
                    if st.button(f"🗑️ Delete Chapter {view_chapter}", type="secondary"):
                        del st.session_state.generated_chapters[view_chapter]
                        self.save_current_story()  # Auto-save changes
                        st.success(f"✅ Chapter {view_chapter} deleted!")
                        st.rerun()
        else:
            st.info("No chapters written yet. Select a chapter number and click 'Write Chapter' to begin.")

    def _generate_all_chapters(self, chapters_to_generate):
        """Generate multiple chapters sequentially"""
        if not chapters_to_generate:
            return

        # Sort chapters to generate them in order
        sorted_chapters = sorted(chapters_to_generate)
        total_chapters = len(sorted_chapters)

        # Create a progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # Use custom style guide if available
            custom_style = st.session_state.get('chapter_style_guide')
            chapter_writer = ChapterAgent(
                model="gpt-4o-mini",
                writing_style_guide=custom_style
            )

            for i, chapter_number in enumerate(sorted_chapters):
                # Update progress
                progress = (i) / total_chapters
                progress_bar.progress(progress)
                status_text.text(f"Writing Chapter {chapter_number}... ({i + 1}/{total_chapters})")

                # Get previous chapter if it exists
                previous_chapter = None
                if chapter_number > 1 and (chapter_number - 1) in st.session_state.generated_chapters:
                    previous_chapter = st.session_state.generated_chapters[chapter_number - 1]

                # Generate the chapter
                chapter = chapter_writer.write_chapter(
                    chapter_outline=st.session_state.generated_outline,
                    characters=st.session_state.generated_characters,
                    setting_description=st.session_state.generated_setting,
                    chapter_number=chapter_number,
                    previous_chapter=previous_chapter,
                    plot_summary=st.session_state.get('generated_plot_summary'),
                    verbose=False
                )

                # Store the chapter
                st.session_state.generated_chapters[chapter_number] = chapter

                # Save progress after each chapter
                self.save_current_story()

                # Update progress
                progress = (i + 1) / total_chapters
                progress_bar.progress(progress)

            # Final status update
            status_text.text(f"✅ Successfully generated {total_chapters} chapters!")
            st.success(f"🎉 All {total_chapters} chapters have been generated successfully!")
            st.info("💾 Story automatically saved to database.")

            # Clear progress indicators after a moment
            time.sleep(2)
            progress_bar.empty()
            status_text.empty()

            # Refresh the page to show updated content
            st.rerun()

        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Error generating chapters: {str(e)}")
            st.info("💾 Progress has been saved up to the point of failure.")
