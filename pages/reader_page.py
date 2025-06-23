"""
Reader page for the YA Novel Generator.
"""
import streamlit as st
from .abstract_page import AbstractPage


class ReaderPage(AbstractPage):
    """Dedicated page for reading the complete story in a distraction-free environment"""
    
    def render(self):
        """Render the reader page"""
        # Initialize fullscreen state if not exists
        if 'reader_fullscreen' not in st.session_state:
            st.session_state.reader_fullscreen = False
        
        # Check if story is complete (has chapters)
        story_complete = bool(st.session_state.get('generated_chapters'))
        
        if not story_complete:
            st.header("📖 Story Reader")
            st.warning("⚠️ Story is not complete yet. Please finish writing chapters to access the reader.")
            return
        
        # Fullscreen toggle button
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔲 Toggle Fullscreen" if not st.session_state.reader_fullscreen else "🔳 Exit Fullscreen"):
                st.session_state.reader_fullscreen = not st.session_state.reader_fullscreen
                st.rerun()
        
        # Apply fullscreen styling if enabled
        if st.session_state.reader_fullscreen:
            st.markdown("""
                <style>
                .main > div {
                    padding-top: 1rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
                .stApp > header {
                    display: none;
                }
                .stApp [data-testid="stSidebar"] {
                    display: none;
                }
                .reader-content {
                    max-width: 800px;
                    margin: 0 auto;
                    font-family: 'Georgia', serif;
                    line-height: 1.6;
                    font-size: 18px;
                }
                .reader-title {
                    text-align: center;
                    font-size: 2.5em;
                    margin-bottom: 1em;
                    color: #2c3e50;
                }
                .reader-chapter-title {
                    font-size: 1.5em;
                    margin-top: 2em;
                    margin-bottom: 1em;
                    color: #34495e;
                    border-bottom: 2px solid #ecf0f1;
                    padding-bottom: 0.5em;
                }
                .reader-chapter-content {
                    text-align: justify;
                    margin-bottom: 2em;
                }
                </style>
            """, unsafe_allow_html=True)
        else:
            st.header("📖 Story Reader")
            st.markdown("*Read your complete story in a clean, distraction-free format*")
        
        # Story content container
        if st.session_state.reader_fullscreen:
            content_container = st.container()
        else:
            content_container = st.container()
        
        with content_container:
            if st.session_state.reader_fullscreen:
                st.markdown('<div class="reader-content">', unsafe_allow_html=True)
            
            # Story title
            story_title = st.session_state.get('story_title', 'Untitled Story')
            if st.session_state.reader_fullscreen:
                st.markdown(f'<h1 class="reader-title">{story_title}</h1>', unsafe_allow_html=True)
            else:
                st.markdown(f"# {story_title}")
            
            # Story metadata
            if not st.session_state.reader_fullscreen:
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                with col1:
                    chapter_count = len(st.session_state.generated_chapters) if st.session_state.get('generated_chapters') else 0
                    st.metric("Chapters", chapter_count)
                with col2:
                    # Estimate word count
                    total_words = 0
                    if st.session_state.get('generated_chapters'):
                        for chapter_content in st.session_state.generated_chapters.values():
                            total_words += len(chapter_content.split())
                    st.metric("Est. Words", f"{total_words:,}")
                with col3:
                    # Estimate reading time (average 200 words per minute)
                    reading_time = max(1, total_words // 200)
                    st.metric("Est. Reading Time", f"{reading_time} min")
                st.markdown("---")
            
            # Table of contents (only in normal mode)
            if not st.session_state.reader_fullscreen and st.session_state.get('generated_chapters'):
                with st.expander("📋 Table of Contents", expanded=False):
                    completed_chapters = sorted(st.session_state.generated_chapters.keys(), key=lambda x: int(x))
                    for chapter_num in completed_chapters:
                        st.markdown(f"- Chapter {chapter_num}")
            
            # Render chapters
            if st.session_state.get('generated_chapters'):
                completed_chapters = sorted(st.session_state.generated_chapters.keys(), key=lambda x: int(x))
                
                for i, chapter_num in enumerate(completed_chapters):
                    chapter_content = st.session_state.generated_chapters[chapter_num]
                    
                    if st.session_state.reader_fullscreen:
                        st.markdown(f'<h2 class="reader-chapter-title">Chapter {chapter_num}</h2>', unsafe_allow_html=True)
                        st.markdown(f'<div class="reader-chapter-content">{chapter_content}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f"## Chapter {chapter_num}")
                        st.markdown(chapter_content)
                        
                        # Add separator between chapters (except for last chapter)
                        if i < len(completed_chapters) - 1:
                            st.markdown("---")
            
            if st.session_state.reader_fullscreen:
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Reading controls (only in normal mode)
        if not st.session_state.reader_fullscreen:
            st.markdown("---")
            st.subheader("📚 Reading Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📖 Export as PDF", help="Export story as PDF for offline reading"):
                    st.info("PDF export feature coming soon!")
            
            with col2:
                if st.button("📱 Mobile View", help="Optimize layout for mobile reading"):
                    st.info("Mobile optimization feature coming soon!")
            
            with col3:
                if st.button("🔄 Refresh Story", help="Reload the latest story content"):
                    st.rerun()
    
    def _is_story_complete(self):
        """Check if the story has all required components for reading"""
        return bool(st.session_state.get('generated_chapters'))
