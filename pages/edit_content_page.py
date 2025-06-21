"""
Edit Content page for the YA Novel Generator.
"""
import streamlit as st
from .abstract_page import AbstractPage


class EditContentPage(AbstractPage):
    """Dedicated page for editing all generated content"""
    
    def render(self):
        """Render the edit content page"""
        st.header("✏️ Edit Content")
        st.markdown("Edit all your generated story content in one place.")

        # Check if any content exists
        has_content = any([
            st.session_state.get('generated_setting'),
            st.session_state.get('generated_characters'),
            st.session_state.get('generated_outline'),
            st.session_state.get('generated_chapters')
        ])

        if not has_content:
            st.warning("⚠️ No generated content found. Please generate content in the other sections first.")
            return

        # Create tabs for different content types
        tabs = st.tabs(["🌍 Setting", "👥 Characters", "📋 Outline", "📖 Chapters"])

        # Setting Tab
        with tabs[0]:
            self._render_setting_tab()

        # Characters Tab
        with tabs[1]:
            self._render_characters_tab()

        # Outline Tab
        with tabs[2]:
            self._render_outline_tab()

        # Chapters Tab
        with tabs[3]:
            self._render_chapters_tab()

        # Export options
        st.markdown("---")
        self._render_export_options()
    
    def _render_setting_tab(self):
        """Render the setting editing tab"""
        if st.session_state.get('generated_setting'):
            st.subheader("World Setting")
            edited_setting = st.text_area(
                "Edit your world setting:",
                value=st.session_state.generated_setting,
                height=400,
                help="Edit your world description here",
                key="edit_page_setting"
            )

            if edited_setting != st.session_state.generated_setting:
                st.session_state.generated_setting = edited_setting
                self.save_current_story()
                st.success("✅ Setting updated!")
        else:
            st.info("No setting generated yet. Go to 'World Building' to create one.")
    
    def _render_characters_tab(self):
        """Render the characters editing tab"""
        if st.session_state.get('generated_characters'):
            st.subheader("Character Profiles")
            for role, description in st.session_state.generated_characters.items():
                st.markdown(f"### {role.title().replace('_', ' ')}")
                edited_character = st.text_area(
                    f"Edit {role.title().replace('_', ' ')}:",
                    value=description,
                    height=250,
                    help=f"Edit the {role} description here",
                    key=f"edit_page_character_{role}"
                )

                if edited_character != description:
                    st.session_state.generated_characters[role] = edited_character
                    self.save_current_story()
                    st.success(f"✅ {role.title().replace('_', ' ')} updated!")

                st.markdown("---")
        else:
            st.info("No characters generated yet. Go to 'Character Creation' to create them.")
    
    def _render_outline_tab(self):
        """Render the outline editing tab"""
        if st.session_state.get('generated_outline'):
            st.subheader("Story Outline")
            edited_outline = st.text_area(
                "Edit your story outline:",
                value=st.session_state.generated_outline,
                height=500,
                help="Edit your 17-chapter outline here",
                key="edit_page_outline"
            )

            if edited_outline != st.session_state.generated_outline:
                st.session_state.generated_outline = edited_outline
                self.save_current_story()
                st.success("✅ Outline updated!")
        else:
            st.info("No outline generated yet. Go to 'Story Outline' to create one.")
    
    def _render_chapters_tab(self):
        """Render the chapters editing tab"""
        if st.session_state.get('generated_chapters'):
            st.subheader("Chapters")
            completed_chapters = sorted(st.session_state.generated_chapters.keys())

            if completed_chapters:
                selected_chapter = st.selectbox(
                    "Select chapter to edit:",
                    options=completed_chapters,
                    format_func=lambda x: f"Chapter {x}",
                    key="edit_page_chapter_selector"
                )

                if selected_chapter:
                    st.markdown(f"### Chapter {selected_chapter}")
                    edited_chapter = st.text_area(
                        f"Edit Chapter {selected_chapter}:",
                        value=st.session_state.generated_chapters[selected_chapter],
                        height=600,
                        help=f"Edit Chapter {selected_chapter} content here",
                        key=f"edit_page_chapter_{selected_chapter}"
                    )

                    if edited_chapter != st.session_state.generated_chapters[selected_chapter]:
                        st.session_state.generated_chapters[selected_chapter] = edited_chapter
                        self.save_current_story()
                        st.success(f"✅ Chapter {selected_chapter} updated!")

                    # Delete chapter option
                    if st.button(f"🗑️ Delete Chapter {selected_chapter}", type="secondary", key=f"delete_chapter_{selected_chapter}"):
                        del st.session_state.generated_chapters[selected_chapter]
                        self.save_current_story()
                        st.success(f"✅ Chapter {selected_chapter} deleted!")
                        st.rerun()
            else:
                st.info("No chapters written yet.")
        else:
            st.info("No chapters written yet. Go to 'Chapter Writing' to create them.")
    
    def _render_export_options(self):
        """Render the export options section"""
        st.subheader("📤 Export Options")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📋 Copy All Content"):
                all_content = []
                if st.session_state.get('story_concept'):
                    all_content.append(f"**STORY CONCEPT:**\n{st.session_state.story_concept}\n")
                if st.session_state.get('generated_setting'):
                    all_content.append(f"**SETTING:**\n{st.session_state.generated_setting}\n")
                if st.session_state.get('generated_characters'):
                    all_content.append("**CHARACTERS:**")
                    for role, desc in st.session_state.generated_characters.items():
                        all_content.append(f"\n{role.title().replace('_', ' ')}:\n{desc}\n")
                if st.session_state.get('generated_outline'):
                    all_content.append(f"**OUTLINE:**\n{st.session_state.generated_outline}\n")
                if st.session_state.get('generated_chapters'):
                    all_content.append("**CHAPTERS:**")
                    for chapter_num in sorted(st.session_state.generated_chapters.keys()):
                        all_content.append(f"\nChapter {chapter_num}:\n{st.session_state.generated_chapters[chapter_num]}\n")

                full_text = "\n".join(all_content)
                st.text_area("Copy this content:", value=full_text, height=200)

        with col2:
            if st.button("💾 Download as Text"):
                all_content = []
                if st.session_state.get('story_concept'):
                    all_content.append(f"STORY CONCEPT:\n{st.session_state.story_concept}\n\n")
                if st.session_state.get('generated_setting'):
                    all_content.append(f"SETTING:\n{st.session_state.generated_setting}\n\n")
                if st.session_state.get('generated_characters'):
                    all_content.append("CHARACTERS:\n")
                    for role, desc in st.session_state.generated_characters.items():
                        all_content.append(f"{role.title().replace('_', ' ')}:\n{desc}\n\n")
                if st.session_state.get('generated_outline'):
                    all_content.append(f"OUTLINE:\n{st.session_state.generated_outline}\n\n")
                if st.session_state.get('generated_chapters'):
                    all_content.append("CHAPTERS:\n\n")
                    for chapter_num in sorted(st.session_state.generated_chapters.keys()):
                        all_content.append(f"Chapter {chapter_num}:\n{st.session_state.generated_chapters[chapter_num]}\n\n")

                full_text = "".join(all_content)
                st.download_button(
                    label="📥 Download Story",
                    data=full_text,
                    file_name=f"{st.session_state.get('story_title', 'story')}.txt",
                    mime="text/plain"
                )

        with col3:
            if st.button("🔄 Refresh All"):
                st.rerun()
