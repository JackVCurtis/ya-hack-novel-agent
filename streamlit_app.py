import streamlit as st
import sqlite3
import json
import uuid
from datetime import datetime
from worldbuilder_agent import WorldbuilderAgent
from character_agent import CharacterAgent
from outliner_agent import OutlinerAgent
from chapter_agent import ChapterAgent


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
            generated_outline TEXT,
            generated_chapters TEXT
        )
    ''')

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
         antagonist_desc, generated_setting, generated_characters, generated_outline, generated_chapters)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        data.get('generated_outline'),
        chapters_json
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
        # Convert row to dictionary
        columns = ['id', 'title', 'created_at', 'updated_at', 'story_concept',
                  'initial_setting', 'protagonist_desc', 'antagonist_desc',
                  'generated_setting', 'generated_characters', 'generated_outline', 'generated_chapters']
        data = dict(zip(columns, row))

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
        'generated_outline': st.session_state.get('generated_outline'),
        'generated_chapters': st.session_state.get('generated_chapters')
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
        st.session_state.generated_outline = data['generated_outline']
        st.session_state.generated_chapters = data['generated_chapters'] or {}


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
                       'generated_setting', 'generated_characters', 'generated_outline']:
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
                st.session_state.get('generated_characters'), st.session_state.get('generated_outline')]):
            save_current_story()

    # Export functionality
    st.sidebar.subheader("📤 Export Story")

    # Check if story has content to export
    has_exportable_content = any([
        st.session_state.get('story_concept'),
        st.session_state.get('generated_setting'),
        st.session_state.get('generated_characters'),
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

    # Render navigation header and route to appropriate page
    render_navigation_header()

    # Route to appropriate page based on current step
    current_step = st.session_state.current_step
    if current_step == "Story Concept":
        story_concept_page()
    elif current_step == "World Building":
        world_building_page()
    elif current_step == "Character Creation":
        character_creation_page()
    elif current_step == "Story Outline":
        story_outline_page()
    elif current_step == "Chapter Writing":
        chapter_writing_page()
    elif current_step == "Edit Content":
        edit_content_page()


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
            "name": "Story Outline",
            "icon": "📋",
            "description": "Plan your story",
            "required": "generated_characters",
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
            "name": "Edit Content",
            "icon": "✏️",
            "description": "Review and edit",
            "required": None,  # Always available if any content exists
            "completed": False  # Never marked as "completed"
        }
    ]

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
                # Story Concept is always available, Edit Content available if any content exists
                if step["name"] == "Story Concept":
                    is_available = True
                elif step["name"] == "Edit Content":
                    is_available = any([
                        st.session_state.get('story_concept'),
                        st.session_state.get('generated_setting'),
                        st.session_state.get('generated_characters'),
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
    completed_steps = sum(1 for step in steps[:-1] if step["completed"])  # Exclude "Edit Content"
    total_steps = len(steps) - 1  # Exclude "Edit Content" from count
    progress_percentage = (completed_steps / total_steps) * 100

    # Progress bar spanning full width
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(progress_percentage / 100)
    with col2:
        st.write(f"**{completed_steps}/{total_steps} completed**")

    st.markdown("---")


def story_concept_page():
    """Page for entering basic story concept and setting"""
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
                save_current_story()

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


def world_building_page():
    """Page for generating detailed world building"""
    st.header("🌍 World Building")
    st.markdown("Generate a detailed setting description based on your story concept.")
    
    if not hasattr(st.session_state, 'story_concept'):
        st.warning("⚠️ Please complete the 'Story Concept' step first.")
        return
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Your Story Elements")
        st.write("**Concept:**", st.session_state.story_concept[:100] + "...")
        st.write("**Initial Setting:**", st.session_state.initial_setting[:100] + "...")
        
        if st.button("🎯 Generate Detailed Setting", type="primary"):
            with st.spinner("Creating your world..."):
                try:
                    worldbuilder = WorldbuilderAgent(model="gpt-4o-mini")
                    detailed_setting = worldbuilder.generate_setting(
                        st.session_state.initial_setting,
                        st.session_state.story_concept,
                        verbose=False
                    )
                    st.session_state.generated_setting = detailed_setting
                    save_current_story()  # Auto-save
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
                save_current_story()  # Auto-save changes
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
                        save_current_story()  # Auto-save
                        st.success("✅ Setting regenerated!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error regenerating setting: {str(e)}")
        else:
            st.info("Click 'Generate Detailed Setting' to create your world description.")


def character_creation_page():
    """Page for generating detailed character descriptions"""
    st.header("👥 Character Creation")
    st.markdown("Generate detailed character profiles based on your story elements.")
    
    if not hasattr(st.session_state, 'story_concept') or not st.session_state.generated_setting:
        st.warning("⚠️ Please complete the 'Story Concept' and 'World Building' steps first.")
        return
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Character Roles")
        
        # Default character roles
        default_roles = ["protagonist", "antagonist", "mentor figure", "love interest"]
        
        # Allow users to customize roles
        character_roles = st.multiselect(
            "Select character roles to generate:",
            options=["protagonist", "antagonist", "mentor figure", "love interest", 
                    "best friend", "rival", "parent figure", "comic relief"],
            default=default_roles,
            help="Choose which character types you want detailed descriptions for"
        )
        
        if st.button("🎭 Generate Characters", type="primary"):
            if character_roles:
                with st.spinner("Creating your characters..."):
                    try:
                        character_agent = CharacterAgent(model="gpt-4o-mini")

                        # Prepare initial character descriptions from story concept page
                        initial_descriptions = {}
                        if "protagonist" in character_roles and st.session_state.get('protagonist_desc'):
                            initial_descriptions["protagonist"] = st.session_state.protagonist_desc
                        if "antagonist" in character_roles and st.session_state.get('antagonist_desc'):
                            initial_descriptions["antagonist"] = st.session_state.antagonist_desc

                        characters = character_agent.generate_character_ensemble(
                            st.session_state.story_concept,
                            st.session_state.generated_setting,
                            character_roles,
                            character_descriptions=initial_descriptions if initial_descriptions else None,
                            verbose=False
                        )
                        st.session_state.generated_characters = characters
                        save_current_story()  # Auto-save
                        st.success("✅ Characters created!")
                        if initial_descriptions:
                            st.info(f"💡 Used initial descriptions for: {', '.join(initial_descriptions.keys())}")
                        st.info("💾 Story automatically saved to database.")
                    except Exception as e:
                        st.error(f"Error generating characters: {str(e)}")
            else:
                st.error("Please select at least one character role.")
    
    with col2:
        st.subheader("Generated Characters")
        if st.session_state.generated_characters:
            # Display each character in an expandable section with editing capability
            for role, description in st.session_state.generated_characters.items():
                with st.expander(f"📖 {role.title().replace('_', ' ')}", expanded=True):
                    # Editable text area for each character
                    edited_character = st.text_area(
                        f"Edit {role.title().replace('_', ' ')} description:",
                        value=description,
                        height=200,
                        help=f"You can edit the {role} description directly here",
                        key=f"character_editor_{role}"
                    )

                    # Update session state if content was edited
                    if edited_character != description:
                        st.session_state.generated_characters[role] = edited_character
                        save_current_story()  # Auto-save changes
                        st.success(f"✅ {role.title().replace('_', ' ')} updated and saved!")
            
            # Option to regenerate specific characters
            st.subheader("Regenerate Individual Characters")
            role_to_regen = st.selectbox(
                "Select character to regenerate:",
                options=list(st.session_state.generated_characters.keys())
            )
            
            if st.button(f"🔄 Regenerate {role_to_regen.title()}"):
                with st.spinner(f"Regenerating {role_to_regen}..."):
                    try:
                        character_agent = CharacterAgent(model="gpt-4o-mini")

                        # Use initial description if available
                        initial_desc = None
                        if role_to_regen == "protagonist" and st.session_state.get('protagonist_desc'):
                            initial_desc = st.session_state.protagonist_desc
                        elif role_to_regen == "antagonist" and st.session_state.get('antagonist_desc'):
                            initial_desc = st.session_state.antagonist_desc

                        new_character = character_agent.generate_character(
                            st.session_state.story_concept,
                            st.session_state.generated_setting,
                            role_to_regen,
                            character_description=initial_desc,
                            verbose=False
                        )
                        st.session_state.generated_characters[role_to_regen] = new_character
                        save_current_story()  # Auto-save
                        st.success(f"✅ {role_to_regen.title()} regenerated!")
                        if initial_desc:
                            st.info("💡 Used initial description as foundation")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error regenerating character: {str(e)}")
        else:
            st.info("Click 'Generate Characters' to create detailed character profiles.")


def story_outline_page():
    """Page for generating story outline"""
    st.header("📋 Story Outline")
    st.markdown("Generate a 17-chapter outline following the Hero's Journey structure.")
    
    if not all([
        hasattr(st.session_state, 'story_concept'),
        st.session_state.generated_setting,
        st.session_state.generated_characters
    ]):
        st.warning("⚠️ Please complete all previous steps first.")
        return
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Story Elements Ready")
        st.write("✅ Story concept defined")
        st.write("✅ World building complete")
        st.write("✅ Characters created")
        st.write(f"✅ {len(st.session_state.generated_characters)} characters ready")
        
        if st.button("📚 Generate 17-Chapter Outline", type="primary"):
            with st.spinner("Creating your story outline..."):
                try:
                    outliner = OutlinerAgent(model="gpt-4o-mini")
                    outline = outliner.generate_outline(
                        st.session_state.story_concept,
                        st.session_state.generated_setting,
                        st.session_state.generated_characters,
                        verbose=False
                    )
                    st.session_state.generated_outline = outline
                    save_current_story()  # Auto-save
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
                save_current_story()  # Auto-save changes
                st.success("✅ Outline updated and saved!")

            # Option to regenerate
            if st.button("🔄 Regenerate Outline"):
                with st.spinner("Regenerating outline..."):
                    try:
                        outliner = OutlinerAgent(model="gpt-4o-mini")
                        outline = outliner.generate_outline(
                            st.session_state.story_concept,
                            st.session_state.generated_setting,
                            st.session_state.generated_characters,
                            verbose=False
                        )
                        st.session_state.generated_outline = outline
                        save_current_story()  # Auto-save
                        st.success("✅ Outline regenerated!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error regenerating outline: {str(e)}")
        else:
            st.info("Click 'Generate 17-Chapter Outline' to create your story structure.")


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
    if st.session_state.get('generated_outline'):
        toc_items.append("- [Story Outline](#story-outline)")

    # Add chapters to TOC
    if st.session_state.get('generated_chapters'):
        toc_items.append("- [Chapters](#chapters)")
        completed_chapters = sorted(st.session_state.generated_chapters.keys())
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

    # Characters
    if st.session_state.get('generated_characters'):
        markdown_content.append("## Characters\n")
        for role, description in st.session_state.generated_characters.items():
            role_title = role.title().replace('_', ' ')
            role_anchor = role.lower().replace(' ', '-').replace('_', '-')
            markdown_content.append(f"### {role_title} {{#{role_anchor}}}\n")
            markdown_content.append(f"{description}\n\n")

    # Story Outline
    if st.session_state.get('generated_outline'):
        markdown_content.append("## Story Outline\n")
        markdown_content.append(f"{st.session_state.generated_outline}\n\n")

    # Chapters
    if st.session_state.get('generated_chapters'):
        markdown_content.append("## Chapters\n")
        completed_chapters = sorted(st.session_state.generated_chapters.keys())
        for chapter_num in completed_chapters:
            chapter_content = st.session_state.generated_chapters[chapter_num]
            markdown_content.append(f"### Chapter {chapter_num} {{#chapter-{chapter_num}}}\n")
            markdown_content.append(f"{chapter_content}\n\n")
            markdown_content.append("---\n")  # Separator between chapters

    return "\n".join(markdown_content)


def generate_all_chapters(chapters_to_generate):
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
        chapter_writer = ChapterAgent(model="gpt-4o-mini")

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
                verbose=False
            )

            # Store the chapter
            st.session_state.generated_chapters[chapter_number] = chapter

            # Save progress after each chapter
            save_current_story()

            # Update progress
            progress = (i + 1) / total_chapters
            progress_bar.progress(progress)

        # Final status update
        status_text.text(f"✅ Successfully generated {total_chapters} chapters!")
        st.success(f"🎉 All {total_chapters} chapters have been generated successfully!")
        st.info("💾 Story automatically saved to database.")

        # Clear progress indicators after a moment
        import time
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


def chapter_writing_page():
    """Page for writing individual chapters"""
    st.header("✍️ Chapter Writing")
    st.markdown("Write individual chapters based on your story outline.")
    
    if not all([
        hasattr(st.session_state, 'story_concept'),
        st.session_state.generated_setting,
        st.session_state.generated_characters,
        st.session_state.generated_outline
    ]):
        st.warning("⚠️ Please complete all previous steps first.")
        return
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
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
                    chapter_writer = ChapterAgent(model="gpt-4o-mini")

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
                        verbose=False
                    )

                    st.session_state.generated_chapters[chapter_number] = chapter
                    save_current_story()  # Auto-save
                    st.success(f"✅ Chapter {chapter_number} complete!")
                    st.info("💾 Story automatically saved to database.")
                except Exception as e:
                    st.error(f"Error writing chapter: {str(e)}")

        # Add separator
        st.markdown("---")

        # Generate All Chapters button
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
                    generate_all_chapters(remaining_chapters)

            with col_b:
                # Use session state to handle confirmation
                if 'confirm_regenerate_all' not in st.session_state:
                    st.session_state.confirm_regenerate_all = False

                if not st.session_state.confirm_regenerate_all:
                    if st.button("🔄 Regenerate All 17 Chapters", type="secondary", help="Regenerate all chapters from scratch"):
                        if st.session_state.generated_chapters:
                            st.session_state.confirm_regenerate_all = True
                            st.rerun()
                        else:
                            generate_all_chapters(set(range(1, 18)))
                else:
                    st.warning("⚠️ This will overwrite all existing chapters!")
                    col_confirm, col_cancel = st.columns(2)
                    with col_confirm:
                        if st.button("✅ Confirm Regenerate", type="secondary"):
                            st.session_state.confirm_regenerate_all = False
                            generate_all_chapters(set(range(1, 18)))
                    with col_cancel:
                        if st.button("❌ Cancel", type="secondary"):
                            st.session_state.confirm_regenerate_all = False
                            st.rerun()
        else:
            st.success("🎉 All 17 chapters have been generated!")

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
                        generate_all_chapters(set(range(1, 18)))
                with col_cancel:
                    if st.button("❌ Cancel Regenerate", type="secondary"):
                        st.session_state.confirm_regenerate_complete = False
                        st.rerun()
    
    with col2:
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
                        save_current_story()  # Auto-save changes
                        st.success(f"✅ Chapter {view_chapter} updated and saved!")

                    # Option to delete chapter
                    if st.button(f"🗑️ Delete Chapter {view_chapter}", type="secondary"):
                        del st.session_state.generated_chapters[view_chapter]
                        save_current_story()  # Auto-save changes
                        st.success(f"✅ Chapter {view_chapter} deleted!")
                        st.rerun()
        else:
            st.info("No chapters written yet. Select a chapter number and click 'Write Chapter' to begin.")


def edit_content_page():
    """Dedicated page for editing all generated content"""
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
                save_current_story()
                st.success("✅ Setting updated!")
        else:
            st.info("No setting generated yet. Go to 'World Building' to create one.")

    # Characters Tab
    with tabs[1]:
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
                    save_current_story()
                    st.success(f"✅ {role.title().replace('_', ' ')} updated!")

                st.markdown("---")
        else:
            st.info("No characters generated yet. Go to 'Character Creation' to create them.")

    # Outline Tab
    with tabs[2]:
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
                save_current_story()
                st.success("✅ Outline updated!")
        else:
            st.info("No outline generated yet. Go to 'Story Outline' to create one.")

    # Chapters Tab
    with tabs[3]:
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
                        save_current_story()
                        st.success(f"✅ Chapter {selected_chapter} updated!")

                    # Delete chapter option
                    if st.button(f"🗑️ Delete Chapter {selected_chapter}", type="secondary", key=f"delete_chapter_{selected_chapter}"):
                        del st.session_state.generated_chapters[selected_chapter]
                        save_current_story()
                        st.success(f"✅ Chapter {selected_chapter} deleted!")
                        st.rerun()
            else:
                st.info("No chapters written yet.")
        else:
            st.info("No chapters written yet. Go to 'Chapter Writing' to create them.")

    # Export options
    st.markdown("---")
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


if __name__ == "__main__":
    main()
