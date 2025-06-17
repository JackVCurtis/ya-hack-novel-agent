from openai import OpenAI
from typing import Dict, Optional


class ChapterAgent:
    """
    A specialized agent for writing complete chapters of young adult fiction.
    
    This agent takes a chapter outline, character descriptions, setting, and optional
    previous chapter to write a full chapter with proper structure including sensory
    opening, rising action, and falling action.
    """
    
    def __init__(self, model: str = "gpt-4o-mini", api_key: str = None):
        """
        Initialize the ChapterAgent.

        Args:
            model: The OpenAI model to use (default: gpt-4o-mini)
            api_key: OpenAI API key (if None, will use environment variable)
        """
        self.model = model
        self.client = OpenAI(api_key=api_key)
        self.system_instructions = self._get_instructions()

    def _initialize_client(self):
        """Initialize the OpenAI client - kept for compatibility."""
        pass  # No longer needed with OpenAI client
    
    def _get_instructions(self) -> str:
        """Get the specialized instructions for the chapter writing agent."""
        return """You are a professional young adult fiction writer specializing in creating compelling, 
        well-structured chapters that engage teenage readers.
        
        CHAPTER STRUCTURE REQUIREMENTS:
        
        1. SENSORY OPENING (1-2 paragraphs):
        - Begin with vivid sensory details that immediately establish mood and atmosphere
        - Use sight, sound, smell, touch, or taste to ground the reader in the scene
        - Set the emotional tone for the chapter
        - Avoid starting with dialogue or action - lead with atmosphere
        
        2. RISING ACTION (majority of chapter):
        - Build tension and conflict progressively
        - Develop character relationships and growth
        - Advance the plot according to the outline
        - Include meaningful dialogue that reveals character
        - Show don't tell - use action and dialogue to convey information
        - Maintain appropriate pacing for YA readers
        
        3. FALLING ACTION & CHAPTER END (1-2 paragraphs):
        - Resolve the immediate chapter conflict or tension
        - Provide a sense of completion for this chapter's arc
        - Set up intrigue or questions for the next chapter
        - End with impact - either emotional resonance or compelling hook
        
        WRITING STYLE GUIDELINES:
        - Write in third person limited POV (unless specified otherwise)
        - Use age-appropriate language for 13-18 year old readers
        - Balance action, dialogue, and internal thoughts
        - Create authentic teenage voices and concerns
        - Include emotional depth and relatability
        - Maintain consistent character voices
        - Show character growth and development
        - Integrate setting details naturally throughout
        
        TECHNICAL REQUIREMENTS:
        - Aim for 2,000-3,500 words per chapter
        - Use proper paragraph breaks and pacing
        - Ensure smooth transitions between scenes
        - Maintain continuity with previous chapters
        - Follow the provided outline while adding creative details
        
        Focus on creating chapters that:
        - Hook readers from the first sentence
        - Maintain engagement throughout
        - Feel authentic to the YA experience
        - Advance both plot and character development
        - Leave readers wanting to continue"""
    
    def write_chapter(self, chapter_outline: str, characters: Dict[str, str], 
                     setting_description: str, chapter_number: int,
                     previous_chapter: Optional[str] = None, verbose: bool = True) -> str:
        """
        Write a complete chapter based on the provided outline and story elements.
        
        Args:
            chapter_outline: Detailed outline for this specific chapter
            characters: Dictionary of character roles and their descriptions
            setting_description: Description of the novel's setting/world
            chapter_number: The chapter number being written
            previous_chapter: The text of the previous chapter (if exists)
            verbose: Whether to print progress messages
            
        Returns:
            A complete chapter with proper structure and pacing
        """
        
        prompt = self._create_prompt(
            chapter_outline, characters, setting_description, 
            chapter_number, previous_chapter
        )
        
        if verbose:
            print(f"ChapterAgent> Writing Chapter {chapter_number}...")
            print("ChapterAgent> Processing outline and character details...")
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_instructions},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000  # Chapters need more tokens
        )

        return response.choices[0].message.content.strip()
    
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
1. Begin with 1-2 paragraphs of sensory description that sets the mood and atmosphere
2. Build rising action that follows the outline while developing characters and advancing plot
3. Include meaningful dialogue and character interactions
4. End with falling action that resolves the chapter's immediate conflict while setting up future intrigue

WRITING GUIDELINES:
- Write 2,000-3,500 words
- Use third person limited POV
- Create authentic YA voices and concerns
- Balance action, dialogue, and internal thoughts
- Show character growth and development
- Integrate setting details naturally
- Maintain appropriate pacing for teenage readers
- End with impact (emotional resonance or compelling hook)

Please write the complete chapter now."""
    
    def write_chapter_with_specific_pov(self, chapter_outline: str, characters: Dict[str, str],
                                       setting_description: str, chapter_number: int,
                                       pov_character: str, previous_chapter: Optional[str] = None,
                                       verbose: bool = True) -> str:
        """
        Write a chapter from a specific character's point of view.
        
        Args:
            chapter_outline: Detailed outline for this specific chapter
            characters: Dictionary of character roles and their descriptions
            setting_description: Description of the novel's setting/world
            chapter_number: The chapter number being written
            pov_character: The character whose POV to write from
            previous_chapter: The text of the previous chapter (if exists)
            verbose: Whether to print progress messages
            
        Returns:
            A complete chapter written from the specified character's POV
        """
        if pov_character not in characters:
            raise ValueError(f"POV character '{pov_character}' not found in character descriptions")
        
        # Create modified prompt with POV specification
        character_info = "\n".join([
            f"{role.upper()}:\n{description[:400]}...\n" 
            for role, description in characters.items()
        ])
        
        previous_context = ""
        if previous_chapter:
            previous_context = f"""
PREVIOUS CHAPTER ENDING:
{previous_chapter[-500:]}

Please ensure smooth continuity from the previous chapter.
"""
        
        pov_prompt = f"""Write Chapter {chapter_number} of a young adult novel from {pov_character.upper()}'S POINT OF VIEW.

CHAPTER OUTLINE:
{chapter_outline}

SETTING DESCRIPTION:
{setting_description}

CHARACTERS:
{character_info}

POV CHARACTER FOCUS:
Write this chapter entirely from {pov_character}'s perspective. Show their thoughts, feelings, and observations. 
Filter all events through their unique viewpoint and personality.
{previous_context}

Follow the same structure and writing guidelines as specified in the instructions, but ensure everything 
is experienced through {pov_character}'s eyes and consciousness.

Please write the complete chapter now."""
        
        if verbose:
            print(f"ChapterAgent> Writing Chapter {chapter_number} from {pov_character}'s POV...")
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_instructions},
                {"role": "user", "content": pov_prompt}
            ],
            temperature=0.7,
            max_tokens=4000  # Chapters need more tokens
        )

        return response.choices[0].message.content.strip()
    
    def update_instructions(self, custom_instructions: str):
        """
        Update the agent's instructions for specialized chapter writing tasks.

        Args:
            custom_instructions: New instructions for the agent
        """
        self.system_instructions = custom_instructions
