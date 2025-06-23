import streamlit as st
import sqlite3
import json
import uuid
from datetime import datetime

# Import page classes
from pages.story_concept_page import StoryConceptPage
from pages.world_building_page import WorldBuildingPage
from pages.character_creation_page import CharacterCreationPage
from pages.plot_summary_page import PlotSummaryPage
from pages.story_outline_page import StoryOutlinePage
from pages.chapter_writing_page import ChapterWritingPage
from pages.reader_page import ReaderPage
from pages.edit_content_page import EditContentPage


def init_database():
    """Initialize the SQLite database for persisting story data"""
    conn = sqlite3.connect('ya_novel_generator.db')
    cursor = conn.cursor()

    # Create stories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stories (
            id TEXT PRIMARY KEY,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            story_concept TEXT,
            initial_setting TEXT,
            protagonist_desc TEXT,
            antagonist_desc TEXT,
            generated_setting TEXT,
            generated_characters TEXT,
            generated_plot_summary TEXT,
            generated_outline TEXT,
            generated_chapters TEXT,
            worldbuilder_style_guide TEXT,
            character_style_guide TEXT,
            plot_summary_style_guide TEXT,
            outliner_style_guide TEXT,
            chapter_style_guide TEXT
        )
    ''')

    # Add new columns to existing tables if they don't exist
    try:
        cursor.execute('ALTER TABLE stories ADD COLUMN worldbuilder_style_guide TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists

    try:
        cursor.execute('ALTER TABLE stories ADD COLUMN character_style_guide TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists

    try:
        cursor.execute('ALTER TABLE stories ADD COLUMN outliner_style_guide TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists

    try:
        cursor.execute('ALTER TABLE stories ADD COLUMN chapter_style_guide TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists

    try:
        cursor.execute('ALTER TABLE stories ADD COLUMN generated_plot_summary TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists

    try:
        cursor.execute('ALTER TABLE stories ADD COLUMN plot_summary_style_guide TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists

    conn.commit()
    conn.close()


def save_story_to_db(story_id, data):
    """Save story data to database"""
    conn = sqlite3.connect('ya_novel_generator.db')
    cursor = conn.cursor()

    # Convert complex data to JSON strings
    characters_json = json.dumps(data.get('generated_characters')) if data.get('generated_characters') else None
    chapters_json = json.dumps(data.get('generated_chapters')) if data.get('generated_chapters') else None

    cursor.execute('''
        INSERT OR REPLACE INTO stories
        (id, title, updated_at, story_concept, initial_setting, protagonist_desc,
         antagonist_desc, generated_setting, generated_characters, generated_plot_summary, generated_outline, generated_chapters,
         worldbuilder_style_guide, character_style_guide, plot_summary_style_guide, outliner_style_guide, chapter_style_guide)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        story_id,
        data.get('title', 'Untitled Story'),
        datetime.now(),
        data.get('story_concept'),
        data.get('initial_setting'),
        data.get('protagonist_desc'),
        data.get('antagonist_desc'),
        data.get('generated_setting'),
        characters_json,
        data.get('generated_plot_summary'),
        data.get('generated_outline'),
        chapters_json,
        data.get('worldbuilder_style_guide'),
        data.get('character_style_guide'),
        data.get('plot_summary_style_guide'),
        data.get('outliner_style_guide'),
        data.get('chapter_style_guide')
    ))

    conn.commit()
    conn.close()


def load_story_from_db(story_id):
    """Load story data from database"""
    conn = sqlite3.connect('ya_novel_generator.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM stories WHERE id = ?', (story_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        # Convert row to dictionary - handle both old and new schema
        columns = ['id', 'title', 'created_at', 'updated_at', 'story_concept',
                  'initial_setting', 'protagonist_desc', 'antagonist_desc',
                  'generated_setting', 'generated_characters', 'generated_plot_summary', 'generated_outline', 'generated_chapters']

        # Add style guide columns if they exist in the row
        if len(row) > 13:
            columns.extend(['worldbuilder_style_guide', 'character_style_guide', 'plot_summary_style_guide',
                           'outliner_style_guide', 'chapter_style_guide'])

        data = dict(zip(columns, row[:len(columns)]))

        # Parse JSON fields back to objects
        if data['generated_characters']:
            data['generated_characters'] = json.loads(data['generated_characters'])
        if data['generated_chapters']:
            data['generated_chapters'] = json.loads(data['generated_chapters'])

        return data
    return None


def get_all_stories():
    """Get list of all stories"""
    conn = sqlite3.connect('ya_novel_generator.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, title, created_at, updated_at FROM stories ORDER BY updated_at DESC')
    rows = cursor.fetchall()
    conn.close()

    return [{'id': row[0], 'title': row[1], 'created_at': row[2], 'updated_at': row[3]} for row in rows]


def delete_story_from_db(story_id):
    """Delete a story from database"""
    conn = sqlite3.connect('ya_novel_generator.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM stories WHERE id = ?', (story_id,))
    conn.commit()
    conn.close()


def initialize_session_state():
    """Initialize session state variables"""
    if 'current_story_id' not in st.session_state:
        st.session_state.current_story_id = str(uuid.uuid4())
    if 'story_title' not in st.session_state:
        st.session_state.story_title = "Untitled Story"
    if 'generated_setting' not in st.session_state:
        st.session_state.generated_setting = None
    if 'generated_characters' not in st.session_state:
        st.session_state.generated_characters = None
    if 'generated_plot_summary' not in st.session_state:
        st.session_state.generated_plot_summary = None
    if 'generated_outline' not in st.session_state:
        st.session_state.generated_outline = None
    if 'generated_chapters' not in st.session_state:
        st.session_state.generated_chapters = {}
    if 'story_concept' not in st.session_state:
        st.session_state.story_concept = None
    if 'initial_setting' not in st.session_state:
        st.session_state.initial_setting = None
    if 'protagonist_desc' not in st.session_state:
        st.session_state.protagonist_desc = None
    if 'antagonist_desc' not in st.session_state:
        st.session_state.antagonist_desc = None

    # Initialize writing style guides
    if 'worldbuilder_style_guide' not in st.session_state:
        st.session_state.worldbuilder_style_guide = None
    if 'character_style_guide' not in st.session_state:
        st.session_state.character_style_guide = None
    if 'plot_summary_style_guide' not in st.session_state:
        st.session_state.plot_summary_style_guide = None
    if 'outliner_style_guide' not in st.session_state:
        st.session_state.outliner_style_guide = None
    if 'chapter_style_guide' not in st.session_state:
        st.session_state.chapter_style_guide = None


def save_current_story():
    """Save current session state to database"""
    data = {
        'title': st.session_state.get('story_title', 'Untitled Story'),
        'story_concept': st.session_state.get('story_concept'),
        'initial_setting': st.session_state.get('initial_setting'),
        'protagonist_desc': st.session_state.get('protagonist_desc'),
        'antagonist_desc': st.session_state.get('antagonist_desc'),
        'generated_setting': st.session_state.get('generated_setting'),
        'generated_characters': st.session_state.get('generated_characters'),
        'generated_plot_summary': st.session_state.get('generated_plot_summary'),
        'generated_outline': st.session_state.get('generated_outline'),
        'generated_chapters': st.session_state.get('generated_chapters'),
        'worldbuilder_style_guide': st.session_state.get('worldbuilder_style_guide'),
        'character_style_guide': st.session_state.get('character_style_guide'),
        'plot_summary_style_guide': st.session_state.get('plot_summary_style_guide'),
        'outliner_style_guide': st.session_state.get('outliner_style_guide'),
        'chapter_style_guide': st.session_state.get('chapter_style_guide')
    }
    save_story_to_db(st.session_state.current_story_id, data)


def load_story_into_session(story_id):
    """Load a story from database into session state"""
    data = load_story_from_db(story_id)
    if data:
        st.session_state.current_story_id = data['id']
        st.session_state.story_title = data['title'] or 'Untitled Story'
        st.session_state.story_concept = data['story_concept']
        st.session_state.initial_setting = data['initial_setting']
        st.session_state.protagonist_desc = data['protagonist_desc']
        st.session_state.antagonist_desc = data['antagonist_desc']
        st.session_state.generated_setting = data['generated_setting']
        st.session_state.generated_characters = data['generated_characters']
        st.session_state.generated_plot_summary = data.get('generated_plot_summary')
        st.session_state.generated_outline = data['generated_outline']
        st.session_state.generated_chapters = data['generated_chapters'] or {}

        # Load style guides if they exist
        st.session_state.worldbuilder_style_guide = data.get('worldbuilder_style_guide')
        st.session_state.character_style_guide = data.get('character_style_guide')
        st.session_state.plot_summary_style_guide = data.get('plot_summary_style_guide')
        st.session_state.outliner_style_guide = data.get('outliner_style_guide')
        st.session_state.chapter_style_guide = data.get('chapter_style_guide')








def main():
    st.set_page_config(
        page_title="YA Novel Generator",
        page_icon="📚",
        layout="wide"
    )

    # Initialize database
    init_database()
    initialize_session_state()

    st.title("📚 Young Adult Novel Generator")
    st.markdown("Create compelling YA fiction with AI-powered story development tools")

    # Story Management in Sidebar
    st.sidebar.title("📖 Story Management")

    # Current story info
    st.sidebar.write(f"**Current Story:** {st.session_state.story_title}")
    st.sidebar.write(f"**Story ID:** {st.session_state.current_story_id[:8]}...")

    # Story title editor
    new_title = st.sidebar.text_input("Story Title:", value=st.session_state.story_title)
    if new_title != st.session_state.story_title:
        st.session_state.story_title = new_title

    # Save/Load buttons
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("💾 Save Story"):
            save_current_story()
            st.sidebar.success("Story saved!")

    with col2:
        if st.button("🆕 New Story"):
            st.session_state.current_story_id = str(uuid.uuid4())
            st.session_state.story_title = "Untitled Story"
            # Clear all story data
            for key in ['story_concept', 'initial_setting', 'protagonist_desc', 'antagonist_desc',
                       'generated_setting', 'generated_characters', 'generated_plot_summary', 'generated_outline',
                       'worldbuilder_style_guide', 'character_style_guide', 'plot_summary_style_guide', 'outliner_style_guide', 'chapter_style_guide']:
                st.session_state[key] = None
            st.session_state.generated_chapters = {}
            st.rerun()

    # Load existing stories
    st.sidebar.subheader("📚 Load Existing Story")
    stories = get_all_stories()
    if stories:
        story_options = {f"{story['title']} ({story['id'][:8]}...)": story['id'] for story in stories}
        selected_story = st.sidebar.selectbox("Select story to load:", options=list(story_options.keys()))

        if st.sidebar.button("📂 Load Selected Story"):
            story_id = story_options[selected_story]
            load_story_into_session(story_id)
            st.sidebar.success("Story loaded!")
            st.rerun()

        # Delete story option
        if st.sidebar.button("🗑️ Delete Selected Story", type="secondary"):
            story_id = story_options[selected_story]
            delete_story_from_db(story_id)
            st.sidebar.success("Story deleted!")
            st.rerun()
    else:
        st.sidebar.info("No saved stories found.")



    # Auto-save functionality
    st.sidebar.write("---")
    if st.sidebar.checkbox("🔄 Auto-save", value=True):
        # Auto-save every time something changes
        if any([st.session_state.get('story_concept'), st.session_state.get('generated_setting'),
                st.session_state.get('generated_characters'), st.session_state.get('generated_plot_summary'), st.session_state.get('generated_outline')]):
            save_current_story()

    # Export functionality
    st.sidebar.subheader("📤 Export Story")

    # Check if story has content to export
    has_exportable_content = any([
        st.session_state.get('story_concept'),
        st.session_state.get('generated_setting'),
        st.session_state.get('generated_characters'),
        st.session_state.get('generated_plot_summary'),
        st.session_state.get('generated_outline'),
        st.session_state.get('generated_chapters')
    ])

    if has_exportable_content:
        # Show story completion status
        completion_items = []
        if st.session_state.get('story_concept'):
            completion_items.append("✅ Story Concept")
        if st.session_state.get('generated_setting'):
            completion_items.append("✅ Setting")
        if st.session_state.get('generated_characters'):
            completion_items.append("✅ Characters")
        if st.session_state.get('generated_plot_summary'):
            completion_items.append("✅ Plot Summary")
        if st.session_state.get('generated_outline'):
            completion_items.append("✅ Outline")
        if st.session_state.get('generated_chapters'):
            chapter_count = len(st.session_state.generated_chapters)
            completion_items.append(f"✅ Chapters ({chapter_count}/17)")

        # Show completion status in a compact format
        with st.sidebar.expander("📋 Story Status", expanded=False):
            for item in completion_items:
                st.sidebar.write(item)

        # Export button
        if st.sidebar.button("📖 Export as Markdown", type="primary", help="Export complete story as a markdown document with table of contents"):
            with st.spinner("Generating markdown document..."):
                try:
                    markdown_content = generate_markdown_export()
                    if markdown_content:
                        # Create filename
                        safe_title = "".join(c for c in st.session_state.get('story_title', 'story') if c.isalnum() or c in (' ', '-', '_')).rstrip()
                        filename = f"{safe_title.replace(' ', '_')}.md"

                        # Provide download button
                        st.sidebar.download_button(
                            label="💾 Download Markdown",
                            data=markdown_content,
                            file_name=filename,
                            mime="text/markdown",
                            help="Click to download your story as a markdown file"
                        )
                        st.sidebar.success("✅ Markdown generated! Click download button above.")
                    else:
                        st.sidebar.error("❌ Failed to generate markdown content.")
                except Exception as e:
                    st.sidebar.error(f"❌ Export error: {str(e)}")
    else:
        st.sidebar.info("📝 Create story content to enable export.")

    # Initialize current step in session state if not exists
    if 'current_step' not in st.session_state:
        st.session_state.current_step = "Story Concept"

    # Initialize completion tracking
    if 'completion_states' not in st.session_state:
        st.session_state.completion_states = {}

    # Track completion state changes
    track_completion_changes()

    # Render navigation header and route to appropriate page
    render_navigation_header()

    # Route to appropriate page based on current step
    current_step = st.session_state.current_step
    if current_step == "Story Concept":
        page = StoryConceptPage()
        page.render()
    elif current_step == "World Building":
        page = WorldBuildingPage()
        page.render()
    elif current_step == "Character Creation":
        page = CharacterCreationPage()
        page.render()
    elif current_step == "Plot Summary":
        page = PlotSummaryPage()
        page.render()
    elif current_step == "Story Outline":
        page = StoryOutlinePage()
        page.render()
    elif current_step == "Chapter Writing":
        page = ChapterWritingPage()
        page.render()
    elif current_step == "Reader":
        page = ReaderPage()
        page.render()
    elif current_step == "Edit Content":
        page = EditContentPage()
        page.render()


def track_completion_changes():
    """Track when steps are completed and trigger navigation updates"""

    # Define current completion states
    current_states = {
        "Story Concept": bool(st.session_state.get('story_concept')),
        "World Building": bool(st.session_state.get('generated_setting')),
        "Character Creation": bool(st.session_state.get('generated_characters')),
        "Plot Summary": bool(st.session_state.get('generated_plot_summary')),
        "Story Outline": bool(st.session_state.get('generated_outline')),
        "Chapter Writing": bool(st.session_state.get('generated_chapters'))
    }

    # Check for newly completed steps
    for step_name, is_completed in current_states.items():
        previous_state = st.session_state.completion_states.get(step_name, False)

        # If step was just completed (changed from False to True)
        if is_completed and not previous_state:
            # Mark as just completed for potential auto-advance
            st.session_state.step_just_completed = step_name

    # Update stored completion states
    st.session_state.completion_states = current_states


def render_navigation_header():
    """Render the horizontal navigation header in the main content area"""

    # Define steps and their requirements
    steps = [
        {
            "name": "Story Concept",
            "icon": "📝",
            "description": "Define your story",
            "required": None,
            "completed": bool(st.session_state.get('story_concept'))
        },
        {
            "name": "World Building",
            "icon": "🌍",
            "description": "Create your world",
            "required": "story_concept",
            "completed": bool(st.session_state.get('generated_setting'))
        },
        {
            "name": "Character Creation",
            "icon": "👥",
            "description": "Develop characters",
            "required": "generated_setting",
            "completed": bool(st.session_state.get('generated_characters'))
        },
        {
            "name": "Plot Summary",
            "icon": "📖",
            "description": "Create plot summary",
            "required": "generated_characters",
            "completed": bool(st.session_state.get('generated_plot_summary'))
        },
        {
            "name": "Story Outline",
            "icon": "📋",
            "description": "Plan your story",
            "required": "generated_plot_summary",
            "completed": bool(st.session_state.get('generated_outline'))
        },
        {
            "name": "Chapter Writing",
            "icon": "✍️",
            "description": "Write your chapters",
            "required": "generated_outline",
            "completed": bool(st.session_state.get('generated_chapters'))
        },
        {
            "name": "Reader",
            "icon": "📖",
            "description": "Read your story",
            "required": None,  # Available when story is complete
            "completed": False  # Never marked as "completed"
        },
        {
            "name": "Edit Content",
            "icon": "✏️",
            "description": "Review and edit",
            "required": None,  # Always available if any content exists
            "completed": False  # Never marked as "completed"
        }
    ]

    # Check if current step was just completed and auto-advance
    current_step_index = next((i for i, step in enumerate(steps) if step["name"] == st.session_state.current_step), 0)
    current_step = steps[current_step_index]

    # Auto-advance logic: if a step was just completed and it's the current step, move to next available step
    just_completed_step = st.session_state.get('step_just_completed')
    if (just_completed_step == current_step["name"] and
        current_step["completed"] and
        current_step_index < len(steps) - 1):
        # Find the next available step
        for i in range(current_step_index + 1, len(steps)):
            next_step = steps[i]

            # Check if next step is available
            if next_step["required"]:
                is_available = bool(st.session_state.get(next_step["required"]))
            else:
                # Story Concept is always available, Reader available when story complete, Edit Content available if any content exists
                if next_step["name"] == "Story Concept":
                    is_available = True
                elif next_step["name"] == "Reader":
                    is_available = bool(st.session_state.get('generated_chapters'))
                elif next_step["name"] == "Edit Content":
                    is_available = any([
                        st.session_state.get('story_concept'),
                        st.session_state.get('generated_setting'),
                        st.session_state.get('generated_characters'),
                        st.session_state.get('generated_plot_summary'),
                        st.session_state.get('generated_outline'),
                        st.session_state.get('generated_chapters')
                    ])
                else:
                    is_available = True

            # If next step is available, auto-advance to it
            if is_available:
                # Store the previous step for notification
                st.session_state.previous_completed_step = current_step["name"]
                st.session_state.current_step = next_step["name"]
                # Clear the completion flag
                if 'step_just_completed' in st.session_state:
                    del st.session_state.step_just_completed
                st.rerun()
                break

        # Clear the completion flag even if we don't auto-advance
        if 'step_just_completed' in st.session_state:
            del st.session_state.step_just_completed

    # Show completion notification if we just auto-advanced
    if st.session_state.get('previous_completed_step'):
        st.success(f"✅ {st.session_state.previous_completed_step} completed! Automatically moved to {st.session_state.current_step}.")
        # Clear the notification flag
        del st.session_state.previous_completed_step

    # Create navigation header
    st.markdown("### 📋 Story Development Steps")

    # Create columns for horizontal layout
    nav_cols = st.columns(len(steps))

    # Render each step as a column
    for i, step in enumerate(steps):
        with nav_cols[i]:
            step_number = i + 1

            # Check if step is available
            if step["required"]:
                is_available = bool(st.session_state.get(step["required"]))
            else:
                # Story Concept is always available, Reader available when story complete, Edit Content available if any content exists
                if step["name"] == "Story Concept":
                    is_available = True
                elif step["name"] == "Reader":
                    is_available = bool(st.session_state.get('generated_chapters'))
                elif step["name"] == "Edit Content":
                    is_available = any([
                        st.session_state.get('story_concept'),
                        st.session_state.get('generated_setting'),
                        st.session_state.get('generated_characters'),
                        st.session_state.get('generated_plot_summary'),
                        st.session_state.get('generated_outline'),
                        st.session_state.get('generated_chapters')
                    ])
                else:
                    is_available = True

            # Create button styling based on state
            if step["completed"]:
                status_icon = "✅"
                button_type = "secondary"
            elif st.session_state.current_step == step["name"]:
                status_icon = "🔄"
                button_type = "primary"
            elif is_available:
                status_icon = "⭕"
                button_type = "secondary"
            else:
                status_icon = "⏸️"
                button_type = "secondary"

            # Create compact button label for horizontal layout
            button_label = f"{step_number}. {status_icon}"

            # Create button with appropriate state
            if is_available:
                if st.button(
                    button_label,
                    type=button_type,
                    help=f"{step['icon']} {step['name']}: {step['description']}",
                    key=f"nav_step_{step['name']}",
                    use_container_width=True
                ):
                    st.session_state.current_step = step["name"]
                    st.rerun()
            else:
                # Disabled button (show but don't make clickable)
                st.button(
                    button_label,
                    type=button_type,
                    help=f"{step['icon']} {step['name']}: Complete previous steps first",
                    key=f"nav_step_disabled_{step['name']}",
                    disabled=True,
                    use_container_width=True
                )

            # Add step name and icon below button
            if st.session_state.current_step == step["name"]:
                st.markdown(f"**{step['icon']} {step['name']}**")
            else:
                st.markdown(f"{step['icon']} {step['name']}")

    # Add progress indicator
    completed_steps = sum(1 for step in steps[:-2] if step["completed"])  # Exclude "Reader" and "Edit Content"
    total_steps = len(steps) - 2  # Exclude "Reader" and "Edit Content" from count
    progress_percentage = (completed_steps / total_steps) * 100

    # Progress bar spanning full width
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(progress_percentage / 100)
    with col2:
        st.write(f"**{completed_steps}/{total_steps} completed**")

    st.markdown("---")














def generate_markdown_export():
    """Generate a complete markdown document with table of contents"""
    if not st.session_state.get('story_title'):
        return None

    markdown_content = []

    # Title
    title = st.session_state.get('story_title', 'Untitled Story')
    markdown_content.append(f"# {title}\n")

    # Add metadata if available
    if st.session_state.get('story_concept'):
        markdown_content.append("*A Young Adult Novel*\n")

    markdown_content.append("---\n")

    # Table of Contents
    markdown_content.append("## Table of Contents\n")

    # Add story elements to TOC
    toc_items = []
    if st.session_state.get('story_concept'):
        toc_items.append("- [Story Concept](#story-concept)")
    if st.session_state.get('generated_setting'):
        toc_items.append("- [Setting](#setting)")
    if st.session_state.get('generated_characters'):
        toc_items.append("- [Characters](#characters)")
        for role in st.session_state.generated_characters.keys():
            role_title = role.title().replace('_', ' ')
            role_anchor = role.lower().replace(' ', '-').replace('_', '-')
            toc_items.append(f"  - [{role_title}](#{role_anchor})")
    if st.session_state.get('generated_plot_summary'):
        toc_items.append("- [Plot Summary](#plot-summary)")
    if st.session_state.get('generated_outline'):
        toc_items.append("- [Story Outline](#story-outline)")

    # Add chapters to TOC - fix sorting to handle numeric values properly
    if st.session_state.get('generated_chapters'):
        toc_items.append("- [Chapters](#chapters)")
        # Convert to integers for proper numeric sorting, then back to original type
        completed_chapters = sorted(st.session_state.generated_chapters.keys(), key=lambda x: int(x))
        for chapter_num in completed_chapters:
            toc_items.append(f"  - [Chapter {chapter_num}](#chapter-{chapter_num})")

    markdown_content.extend(toc_items)
    markdown_content.append("\n---\n")

    # Story Concept
    if st.session_state.get('story_concept'):
        markdown_content.append("## Story Concept\n")
        markdown_content.append(f"{st.session_state.story_concept}\n\n")

    # Setting
    if st.session_state.get('generated_setting'):
        markdown_content.append("## Setting\n")
        markdown_content.append(f"{st.session_state.generated_setting}\n\n")

    # Characters - fix anchor syntax (remove curly braces)
    if st.session_state.get('generated_characters'):
        markdown_content.append("## Characters\n")
        for role, description in st.session_state.generated_characters.items():
            role_title = role.title().replace('_', ' ')
            # Remove the incorrect {#anchor} syntax - markdown auto-generates anchors
            markdown_content.append(f"### {role_title}\n")
            markdown_content.append(f"{description}\n\n")

    # Plot Summary
    if st.session_state.get('generated_plot_summary'):
        markdown_content.append("## Plot Summary\n")
        markdown_content.append(f"{st.session_state.generated_plot_summary}\n\n")

    # Story Outline
    if st.session_state.get('generated_outline'):
        markdown_content.append("## Story Outline\n")
        markdown_content.append(f"{st.session_state.generated_outline}\n\n")

    # Chapters - fix anchor syntax and sorting
    if st.session_state.get('generated_chapters'):
        markdown_content.append("## Chapters\n")
        # Convert to integers for proper numeric sorting, then back to original type
        completed_chapters = sorted(st.session_state.generated_chapters.keys(), key=lambda x: int(x))
        for chapter_num in completed_chapters:
            chapter_content = st.session_state.generated_chapters[chapter_num]
            # Remove the incorrect {#anchor} syntax - markdown auto-generates anchors
            markdown_content.append(f"### Chapter {chapter_num}\n")
            markdown_content.append(f"{chapter_content}\n\n")
            markdown_content.append("---\n")  # Separator between chapters

    return "\n".join(markdown_content)











if __name__ == "__main__":
    main()
