"""
Character Creation page for the YA Novel Generator.
"""
import streamlit as st
from .abstract_page import AbstractPage
from character_agent import CharacterAgent


class CharacterCreationPage(AbstractPage):
    """Page for generating detailed character descriptions"""
    
    def render(self):
        """Render the character creation page"""
        st.header("👥 Character Creation")
        st.markdown("Generate detailed character profiles based on your story elements.")

        if not self.check_prerequisites(['story_concept', 'generated_setting']):
            self.show_prerequisites_warning(['Story Concept', 'World Building'])
            return

        # Character Style Guide Section
        self.create_style_guide_section(
            CharacterAgent,
            'character_style_guide',
            'Character Writing Style Guide',
            'Guidelines for character development and descriptions'
        )

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
                            # Use custom style guide if available
                            custom_style = st.session_state.get('character_style_guide')
                            character_agent = CharacterAgent(
                                model="gpt-4o-mini",
                                writing_style_guide=custom_style
                            )

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
                            self.save_current_story()  # Auto-save
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
                            self.save_current_story()  # Auto-save changes
                            st.success(f"✅ {role.title().replace('_', ' ')} updated and saved!")
                
                self._render_character_regeneration_section()
            else:
                st.info("Click 'Generate Characters' to create detailed character profiles.")
    
    def _render_character_regeneration_section(self):
        """Render the character regeneration section"""
        # Option to regenerate specific characters
        st.subheader("Regenerate Individual Characters")
        role_to_regen = st.selectbox(
            "Select character to regenerate:",
            options=list(st.session_state.generated_characters.keys())
        )
        
        if st.button(f"🔄 Regenerate {role_to_regen.title()}"):
            with st.spinner(f"Regenerating {role_to_regen}..."):
                try:
                    # Use custom style guide if available
                    custom_style = st.session_state.get('character_style_guide')
                    character_agent = CharacterAgent(
                        model="gpt-4o-mini",
                        writing_style_guide=custom_style
                    )

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
                    self.save_current_story()  # Auto-save
                    st.success(f"✅ {role_to_regen.title()} regenerated!")
                    if initial_desc:
                        st.info("💡 Used initial description as foundation")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error regenerating character: {str(e)}")
