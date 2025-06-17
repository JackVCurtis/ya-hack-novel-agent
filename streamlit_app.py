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

    # Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a step:",
        ["Story Concept", "World Building", "Character Creation", "Story Outline", "Chapter Writing"]
    )
    
    if page == "Story Concept":
        story_concept_page()
    elif page == "World Building":
        world_building_page()
    elif page == "Character Creation":
        character_creation_page()
    elif page == "Story Outline":
        story_outline_page()
    elif page == "Chapter Writing":
        chapter_writing_page()


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
                    worldbuilder = WorldbuilderAgent()
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
            st.write(st.session_state.generated_setting)
            
            # Option to regenerate
            if st.button("🔄 Regenerate Setting"):
                with st.spinner("Regenerating world..."):
                    try:
                        worldbuilder = WorldbuilderAgent()
                        detailed_setting = worldbuilder.generate_setting(
                            st.session_state.initial_setting,
                            st.session_state.story_concept,
                            verbose=False
                        )
                        print(detailed_setting)
                        st.session_state.generated_setting = detailed_setting
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
                        character_agent = CharacterAgent()

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
            for role, description in st.session_state.generated_characters.items():
                with st.expander(f"📖 {role.title()}"):
                    st.write(description)
            
            # Option to regenerate specific characters
            st.subheader("Regenerate Individual Characters")
            role_to_regen = st.selectbox(
                "Select character to regenerate:",
                options=list(st.session_state.generated_characters.keys())
            )
            
            if st.button(f"🔄 Regenerate {role_to_regen.title()}"):
                with st.spinner(f"Regenerating {role_to_regen}..."):
                    try:
                        character_agent = CharacterAgent()

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
                    outliner = OutlinerAgent()
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
            st.write(st.session_state.generated_outline)
            
            # Option to regenerate
            if st.button("🔄 Regenerate Outline"):
                with st.spinner("Regenerating outline..."):
                    try:
                        outliner = OutlinerAgent()
                        outline = outliner.generate_outline(
                            st.session_state.story_concept,
                            st.session_state.generated_setting,
                            st.session_state.generated_characters,
                            verbose=False
                        )
                        st.session_state.generated_outline = outline
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error regenerating outline: {str(e)}")
        else:
            st.info("Click 'Generate 17-Chapter Outline' to create your story structure.")


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
                    chapter_writer = ChapterAgent()
                    
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
    
    with col2:
        st.subheader("Generated Chapters")
        
        if st.session_state.generated_chapters:
            # Show list of completed chapters
            completed_chapters = sorted(st.session_state.generated_chapters.keys())
            st.write(f"**Completed Chapters:** {', '.join(map(str, completed_chapters))}")
            
            # Chapter viewer
            if completed_chapters:
                view_chapter = st.selectbox(
                    "View chapter:",
                    options=completed_chapters,
                    format_func=lambda x: f"Chapter {x}"
                )
                
                if view_chapter in st.session_state.generated_chapters:
                    st.subheader(f"Chapter {view_chapter}")
                    st.write(st.session_state.generated_chapters[view_chapter])
        else:
            st.info("No chapters written yet. Select a chapter number and click 'Write Chapter' to begin.")


if __name__ == "__main__":
    main()
