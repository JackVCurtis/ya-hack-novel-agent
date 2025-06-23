from abstract_writer_agent import AbstractWriterAgent
from typing import Dict, Optional


class ChapterAgent(AbstractWriterAgent):
    """
    A specialized agent for writing complete chapters of young adult fiction.
    
    This agent takes a chapter outline, character descriptions, setting, and optional
    previous chapter to write a full chapter with proper structure including
    opening, rising action, and falling action.
    """
    
    def __init__(self, model: str = "gpt-4o-mini", api_key: str = None,
                 writing_style_guide: Optional[str] = None):
        """
        Initialize the ChapterAgent.

        Args:
            model: The OpenAI model to use (default: gpt-4o-mini)
            api_key: OpenAI API key (if None, will use environment variable)
            writing_style_guide: Optional text containing writing style guidelines.
                                If None, uses the default chapter writing style guide
        """
        super().__init__(model, api_key, writing_style_guide)
    
    def _get_instructions(self) -> str:
        """Get the specialized instructions for the chapter writing agent."""
        return """You are a professional young adult fiction writer specializing in creating compelling, 
        well-structured chapters that engage teenage readers.
        
        CHAPTER STRUCTURE REQUIREMENTS:
        
        1. EVOCATIVE OPENING (1-2 paragraphs):
        - Begin with vivid details that immediately establish mood and atmosphere
        - Use sight, sound, smell, touch, or taste to ground the reader in the scene
        - Set the emotional tone for the chapter
        - Avoid starting with dialogue or action - lead with atmosphere
        
        2. RISING ACTION (majority of chapter):
        - Build tension and conflict progressively
        - Develop character relationships and growth
        - Advance the plot according to the outline
        - Include meaningful dialogue that reveals character
        - Show don't tell - use action and dialogue to convey information
        
        3. CLIMAX (1-2 paragraphs):
        - A significant moment of conflict, revelation, or change
        - The turning point of the chapter
        - Should be emotionally impactful
        - Should advance the plot and character arcs
        - Should set up the falling action
        
        4. FALLING ACTION & CHAPTER END (1-2 paragraphs):
        - Resolve the immediate chapter conflict or tension
        - Provide a sense of completion for this chapter's arc
        - Set up intrigue or questions for the next chapter
        - End with impact - either emotional resonance or compelling hook
        
        ENSURE THAT THE STORY BEATS OF THE CHAPTER SPECIFIED IN THE OUTLINE ARE ACCOMPLISHED

        WRITING STYLE GUIDELINES:
        - Write in third person limited POV from a SINGLE character's perspective throughout the entire chapter
        - NEVER switch POV or create multiple sections - maintain one consistent viewpoint
        - Use age-appropriate language for 13-18 year old readers
        - Balance action, dialogue, and internal thoughts
        - Create authentic teenage voices and concerns
        - Include emotional depth and relatability
        - Maintain consistent character voices
        - Show character growth and development
        - Integrate setting details naturally throughout
        - Write as one continuous narrative without scene breaks or section divisions
        
        TECHNICAL REQUIREMENTS:
        - Aim for 2,000-3,500 words per chapter
        - Use proper paragraph breaks and pacing
        - Ensure smooth transitions between scenes
        - Maintain continuity with previous chapters
        - Follow the provided outline while adding creative details
        
        Focus on creating chapters that:
        - Hook readers from the first sentence
        - Maintain engagement throughout
        - Advance both plot and character development
        - Leave readers wanting to continue"""

    def _get_default_style_guide(self) -> str:
        """Get the default writing style guide for chapter writing."""
        return """CHAPTER WRITING STYLE GUIDE:
AVOID RUN-ON SENTENCES

NARRATIVE STRUCTURE:
- Begin each chapter with details that establish mood and atmosphere
- Build rising action progressively with clear story beats
- Include a climactic moment or turning point within the chapter
- End with falling action that resolves immediate tension while creating intrigue

WRITING STYLE:
- Use third person limited POV from ONE character's perspective for the entire chapter
- NEVER switch POV or create multiple viewpoint sections within a chapter
- Write 3,000-4,500 words per chapter for substantial content
- Balance action, dialogue, and internal thoughts effectively
- Create authentic teenage voices and concerns
- Write as one continuous narrative without section breaks

CHARACTER DEVELOPMENT:
- Show character growth through actions and decisions from the single POV character's perspective
- Include meaningful dialogue that reveals personality
- Demonstrate relationships and character dynamics as seen by the POV character
- Allow the POV character to drive the plot through their choices and observations

PACING AND FLOW:
- Vary sentence structure and paragraph length for rhythm
- Create smooth transitions between events without scene breaks or section divisions
- Maintain a fast and exciting pace through continuous narrative flow
- Create compelling hooks and chapter endings

EVOCATIVE AND ATMOSPHERIC DETAILS:
- Include details that ground readers in the scene
- DO NOT USE SIMILIES, in the form of "like" or "as"
- use metaphor sparingly to emphasize important details
- Balance description with action and dialogue
"""

    def write_chapter(self, chapter_outline: str, characters: Dict[str, str],
                     setting_description: str, chapter_number: int,
                     previous_chapter: Optional[str] = None, plot_summary: Optional[str] = None,
                     verbose: bool = True) -> str:
        """
        Write a complete chapter using a two-step process: first generate a detailed prompt,
        then use that prompt to write a comprehensive chapter.

        Args:
            chapter_outline: The complete book outline (all 17 chapters)
            characters: Dictionary of character roles and their descriptions
            setting_description: Description of the novel's setting/world
            chapter_number: The chapter number being written
            previous_chapter: The text of the previous chapter (if exists)
            plot_summary: Optional single paragraph plot summary for additional context
            verbose: Whether to print progress messages

        Returns:
            A complete chapter with proper structure and pacing
        """

        if verbose:
            print(f"ChapterAgent> Writing Chapter {chapter_number}...")
            if plot_summary:
                print("ChapterAgent> Using plot summary for additional context")

        # Use the parent class's two-step generation method
        return self._execute_two_step_generation(
            step1_args=(chapter_outline, characters, setting_description, chapter_number),
            step1_kwargs={'previous_chapter': previous_chapter, 'plot_summary': plot_summary, 'verbose': verbose},
            step2_args=(),
            step2_kwargs={'chapter_number': chapter_number, 'verbose': verbose},
            verbose=verbose,
            agent_name="ChapterAgent"
        )

    def _generate_detailed_prompt(self, chapter_outline: str, characters: Dict[str, str],
                                 setting_description: str, chapter_number: int,
                                 previous_chapter: Optional[str] = None, plot_summary: Optional[str] = None,
                                 verbose: bool = True) -> str:
        """
        Implementation of abstract method for generating detailed prompts.
        """
        return self._generate_chapter_prompt(
            chapter_outline, characters, setting_description, chapter_number, previous_chapter, plot_summary, verbose
        )

    def _create_content_from_prompt(self, detailed_prompt: str, chapter_number: int = None,
                                   verbose: bool = True) -> str:
        """
        Implementation of abstract method for creating content from prompts.
        """
        return self._write_chapter_from_prompt(detailed_prompt, chapter_number, verbose)

    def _generate_chapter_prompt(self, chapter_outline: str, characters: Dict[str, str],
                                setting_description: str, chapter_number: int,
                                previous_chapter: Optional[str] = None, plot_summary: Optional[str] = None,
                                verbose: bool = True) -> str:
        """
        Generate a detailed prompt for writing a specific chapter.

        Args:
            chapter_outline: The complete book outline (all 17 chapters)
            characters: Dictionary of character roles and their descriptions
            setting_description: Description of the novel's setting/world
            chapter_number: The chapter number being written
            previous_chapter: The text of the previous chapter (if exists)
            plot_summary: Optional single paragraph plot summary for additional context
            verbose: Whether to print progress messages

        Returns:
            A detailed prompt for writing the chapter
        """
        # Format character information
        character_info = self._format_character_info(characters)

        # Handle previous chapter context
        previous_context = ""
        if previous_chapter:
            previous_context = f"""
PREVIOUS CHAPTER SUMMARY:
{previous_chapter[-1000:]}

The new chapter should continue seamlessly from this point.
"""

        # Format plot summary section if provided
        plot_summary_section = ""
        if plot_summary:
            plot_summary_section = self._create_context_section("PLOT SUMMARY", plot_summary)

        prompt_generation_request = f"""You are a professional writing coach specializing in young adult fiction. Your task is to create a detailed, comprehensive prompt that will guide an AI to write an engaging Chapter {chapter_number} of a YA novel.

{self._create_context_section("COMPLETE BOOK OUTLINE", chapter_outline, max_length=2000)}

{self._create_context_section("SETTING DESCRIPTION", setting_description, max_length=500)}

{self._create_context_section("CHARACTER PROFILES", character_info)}

{plot_summary_section}
{previous_context}

Based on the above information, create a detailed writing prompt that will result in a rich, engaging Chapter {chapter_number} that is 3,000-4,500 words long written as ONE CONTINUOUS NARRATIVE from a single character's POV. The prompt should include:

1. NARRATIVE FLOW: What happens in this chapter as a continuous story from one character's perspective
2. POV CHARACTER FOCUS: Which character's viewpoint should be used throughout the entire chapter
3. CHARACTER DEVELOPMENT: How the POV character should grow or change
4. DIALOGUE GUIDANCE: Key conversations that need to happen as experienced by the POV character
5. EVOCATIVE DETAILS: Specific atmospheric elements the POV character notices and experiences
6. PACING INSTRUCTIONS: How to structure the rising and falling action through the POV character's experience
7. EMOTIONAL BEATS: What emotions should be evoked and when from the POV character's perspective
8. PLOT ADVANCEMENT: How this chapter moves the overall story forward through the POV character's actions and observations
9. {"PLOT SUMMARY ALIGNMENT: How to ensure the chapter aligns with and serves the overall plot summary" if plot_summary else "STORY COHERENCE: How to maintain consistency with the overall narrative"}
10. CHAPTER ENDING: Specific guidance on how to end with impact from the POV character's perspective

CRITICAL: Ensure the chapter is written as ONE CONTINUOUS NARRATIVE without scene breaks, section divisions, or POV switches. Everything should be experienced through a single character's perspective.

{"Ensure the chapter stays true to the plot summary while providing detailed continuous narrative development from one character's viewpoint." if plot_summary else ""}

Create a comprehensive prompt that will result in a substantial, well-developed chapter that feels authentic to the YA genre and advances both character and plot development significantly through a single, unbroken narrative perspective."""

        return self._make_api_call(
            system_content="You are an expert writing coach who creates detailed prompts for writing compelling young adult fiction chapters.",
            user_content=prompt_generation_request,
            temperature=0.6,
            max_tokens=2000
        )

    def _write_chapter_from_prompt(self, detailed_prompt: str, chapter_number: int,
                                  verbose: bool = True) -> str:
        """
        Write a chapter using a detailed prompt.

        Args:
            detailed_prompt: The detailed prompt for writing the chapter
            chapter_number: The chapter number being written
            verbose: Whether to print progress messages

        Returns:
            The complete chapter content
        """
        chapter_writing_instructions = """You are a professional young adult fiction writer. Your task is to write a complete, engaging chapter based on the detailed prompt provided.

CRITICAL REQUIREMENTS:
- Write exactly ONE CONTINUOUS CHAPTER from a SINGLE character's point of view
- NEVER switch POV or create multiple sections within the chapter
- NEVER use scene breaks, section dividers, or subsection headers
- Write as one unbroken narrative flow from beginning to end

WRITING REQUIREMENTS:
- Write 3,000-4,500 words as one continuous narrative
- Use third person limited POV from ONE character's perspective throughout
- Create authentic teenage voices and concerns
- Include rich details and atmospheric descriptions as seen by the POV character
- Balance action, dialogue, and internal thoughts from the POV character's experience
- Show character growth and development through the POV character's journey
- Maintain appropriate pacing for YA readers
- End with emotional impact or compelling hook

CHAPTER STRUCTURE (as one continuous narrative):
1. EVOCATIVE OPENING (2-3 paragraphs): Begin with vivid details that immediately establish mood and atmosphere from the POV character's perspective
2. RISING ACTION (majority of chapter): Build tension progressively with character development and plot advancement through the POV character's experience
3. CLIMAX/TURNING POINT: A significant moment of conflict, revelation, or change as experienced by the POV character
4. FALLING ACTION & RESOLUTION: Resolve immediate chapter tension while setting up future intrigue, all from the POV character's perspective

ABSOLUTELY AVOID:
- Multiple POV characters within the same chapter
- Scene breaks or section divisions (like "***" or "---")
- Subsection headers or chapter subdivisions
- Switching between different characters' perspectives
- Any formatting that breaks the narrative flow

Focus on creating a chapter that feels substantial, emotionally resonant, and advances both character and plot in meaningful ways through ONE character's continuous experience."""

        return self._make_api_call(
            system_content=chapter_writing_instructions,
            user_content=detailed_prompt,
            temperature=0.7,
            max_tokens=6000  # Increased for longer chapters
        )

    def _create_prompt(self, chapter_outline: str, characters: Dict[str, str],
                      setting_description: str, chapter_number: int,
                      previous_chapter: Optional[str] = None) -> str:
        """Create the prompt for the chapter writing task."""
        
        # Format character information
        character_info = "\n".join([
            f"{role.upper()}:\n{description[:400]}...\n" 
            for role, description in characters.items()
        ])
        
        # Handle previous chapter context
        previous_context = ""
        if previous_chapter:
            # Use last 500 characters to provide context without overwhelming
            previous_context = f"""
PREVIOUS CHAPTER ENDING:
{previous_chapter[-500:]}

Please ensure smooth continuity from the previous chapter.
"""
        
        return f"""Write Chapter {chapter_number} of a young adult novel based on the following information:

CHAPTER OUTLINE:
{chapter_outline}

SETTING DESCRIPTION:
{setting_description}

CHARACTERS:
{character_info}
{previous_context}

CHAPTER STRUCTURE REQUIREMENTS:
1. Begin with 1-2 paragraphs of description that sets the mood and atmosphere from ONE character's perspective
2. Build rising action that follows the outline while developing characters and advancing plot through ONE character's experience
3. Include meaningful dialogue and character interactions as experienced by the POV character
4. End with falling action that resolves the chapter's immediate conflict while setting up future intrigue, all from the same character's perspective

CRITICAL WRITING GUIDELINES:
- Write 2,000-3,500 words as ONE CONTINUOUS NARRATIVE
- Use third person limited POV from a SINGLE character throughout the entire chapter
- NEVER switch POV or create multiple sections within the chapter
- NEVER use scene breaks, section dividers, or subsection headers
- Create authentic YA voices and concerns
- Balance action, dialogue, and internal thoughts from the POV character's perspective
- Show character growth and development through the POV character's journey
- Integrate setting details naturally as noticed by the POV character
- Maintain appropriate pacing for teenage readers
- End with impact (emotional resonance or compelling hook)

Write the complete chapter as one unbroken narrative from a single character's point of view."""
    
    def write_chapter_with_specific_pov(self, chapter_outline: str, characters: Dict[str, str],
                                       setting_description: str, chapter_number: int,
                                       pov_character: str, previous_chapter: Optional[str] = None,
                                       plot_summary: Optional[str] = None, verbose: bool = True) -> str:
        """
        Write a chapter from a specific character's point of view using the two-step process.

        Args:
            chapter_outline: The complete book outline (all 17 chapters)
            characters: Dictionary of character roles and their descriptions
            setting_description: Description of the novel's setting/world
            chapter_number: The chapter number being written
            pov_character: The character whose POV to write from
            previous_chapter: The text of the previous chapter (if exists)
            plot_summary: Optional single paragraph plot summary for additional context
            verbose: Whether to print progress messages

        Returns:
            A complete chapter written from the specified character's POV
        """
        if pov_character not in characters:
            raise ValueError(f"POV character '{pov_character}' not found in character descriptions")

        if verbose:
            print(f"ChapterAgent> Writing Chapter {chapter_number} from {pov_character}'s POV...")
            if plot_summary:
                print("ChapterAgent> Using plot summary for additional context")
            print("ChapterAgent> Step 1: Generating POV-specific writing prompt...")

        # Step 1: Generate a detailed POV-specific prompt
        detailed_prompt = self._generate_pov_chapter_prompt(
            chapter_outline, characters, setting_description,
            chapter_number, pov_character, previous_chapter, plot_summary
        )

        if verbose:
            print("ChapterAgent> Step 2: Writing chapter from POV using generated prompt...")

        # Step 2: Write the chapter using the POV-specific prompt
        chapter_content = self._write_chapter_from_prompt(
            detailed_prompt, chapter_number, verbose
        )

        return chapter_content

    def _generate_pov_chapter_prompt(self, chapter_outline: str, characters: Dict[str, str],
                                    setting_description: str, chapter_number: int,
                                    pov_character: str, previous_chapter: Optional[str] = None,
                                    plot_summary: Optional[str] = None) -> str:
        """Generate a detailed prompt for writing a POV-specific chapter."""

        # Format character information
        character_info = self._format_character_info(characters)

        # Handle previous chapter context
        previous_context = ""
        if previous_chapter:
            previous_context = f"""
PREVIOUS CHAPTER SUMMARY:
{previous_chapter[-1000:]}

The new chapter should continue seamlessly from this point.
"""

        # Format plot summary section if provided
        plot_summary_section = ""
        if plot_summary:
            plot_summary_section = self._create_context_section("PLOT SUMMARY", plot_summary)

        pov_prompt_request = f"""You are a professional writing coach specializing in young adult fiction. Create a detailed, comprehensive prompt for writing Chapter {chapter_number} from {pov_character.upper()}'S POINT OF VIEW.

{self._create_context_section("COMPLETE BOOK OUTLINE", chapter_outline, max_length=2000)}

{self._create_context_section("SETTING DESCRIPTION", setting_description, max_length=500)}

{self._create_context_section("CHARACTER PROFILES", character_info)}

{plot_summary_section}

POV CHARACTER: {pov_character.upper()}
{previous_context}

Create a detailed writing prompt that will result in a rich, engaging Chapter {chapter_number} (3,000-4,500 words) written as ONE CONTINUOUS NARRATIVE entirely from {pov_character}'s perspective without any POV switches or section breaks. The prompt should include:

1. CONTINUOUS NARRATIVE FLOW: How {pov_character} experiences the entire chapter as one unbroken story
2. POV-SPECIFIC EXPERIENCE: What {pov_character} experiences, sees, thinks, and feels throughout the chapter
3. INTERNAL MONOLOGUE GUIDANCE: {pov_character}'s thoughts, reactions, and emotional journey
4. DIALOGUE FROM POV: How {pov_character} speaks and interprets others' words
5. EVOCATIVE EXPERIENCE: What {pov_character} specifically notices through their senses
6. CHARACTER VOICE: How to capture {pov_character}'s unique personality and speech patterns consistently
7. EMOTIONAL BEATS: {pov_character}'s emotional arc throughout the chapter
8. RELATIONSHIP DYNAMICS: How {pov_character} views and interacts with other characters
9. PLOT ADVANCEMENT: How events unfold from {pov_character}'s limited perspective

CRITICAL: Ensure the prompt emphasizes that the chapter must be written as ONE CONTINUOUS NARRATIVE from {pov_character}'s perspective only, with NO scene breaks, section divisions, or POV switches. Everything should flow as one unbroken story from {pov_character}'s viewpoint.

Ensure the prompt will create a chapter that feels authentic to {pov_character}'s voice while advancing the overall story through their singular perspective."""

        return self._make_api_call(
            system_content="You are an expert writing coach who creates detailed prompts for POV-specific young adult fiction chapters.",
            user_content=pov_prompt_request,
            temperature=0.6,
            max_tokens=2000
        )
    
    def update_instructions(self, custom_instructions: str):
        """
        Update the agent's instructions for specialized chapter writing tasks.

        Args:
            custom_instructions: New instructions for the agent
        """
        self.system_instructions = custom_instructions
