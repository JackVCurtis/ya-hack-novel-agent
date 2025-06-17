from openai import OpenAI
from typing import Optional, Dict, Any


class CharacterAgent:
    """
    A specialized agent for creating compelling young adult fiction character descriptions.
    
    This agent takes a novel concept, setting description, and character role to produce
    detailed character profiles including physical appearance, personality, goals, and flaws.
    """
    
    def __init__(self, model: str = "gpt-4o-mini", api_key: str = None):
        """
        Initialize the CharacterAgent.

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
        """Get the specialized instructions for the character creation agent."""
        return """You are a creative character development assistant specializing in young adult fiction.
        Your task is to create compelling, three-dimensional characters that fit seamlessly into the 
        provided setting and serve their narrative role effectively.
        
        For each character, provide detailed information in these categories:
        
        PHYSICAL APPEARANCE:
        - Age-appropriate descriptions for YA audience
        - Distinctive features that make them memorable
        - How their appearance reflects their personality or role
        - Clothing style and personal presentation
        
        PERSONAL TASTES & INTERESTS:
        - Hobbies, interests, and passions
        - Favorite things (music, food, activities, etc.)
        - Dislikes and pet peeves
        - Cultural preferences that fit the setting
        
        GOALS & MOTIVATIONS:
        - Primary driving goal related to the main plot
        - Secondary personal goals
        - Internal motivations and desires
        - What they're trying to achieve or avoid
        
        STRENGTHS:
        - Natural talents and abilities
        - Learned skills and competencies
        - Positive personality traits
        - How these strengths serve their role in the story
        
        FLAWS & WEAKNESSES:
        - Character flaws that create internal conflict
        - Weaknesses that can be exploited
        - Bad habits or negative traits
        - How these flaws drive character growth
        
        Focus on creating characters that:
        - Feel authentic and relatable to YA readers
        - Have clear connections to the setting and world
        - Serve their narrative function while being complex individuals
        - Have potential for growth and change throughout the story
        - Balance strengths and flaws to avoid Mary Sue/Gary Stu characters"""
    
    def generate_character(self, novel_concept: str, setting_description: str,
                          character_role: str, character_description: Optional[str] = None,
                          verbose: bool = True) -> str:
        """
        Generate a comprehensive character description for a YA novel.

        Args:
            novel_concept: The overall concept/theme of the novel
            setting_description: Description of the novel's setting/world
            character_role: The character's role (protagonist, antagonist, ally, etc.)
            character_description: Optional initial character description to build upon
            verbose: Whether to print progress messages

        Returns:
            A detailed character description with all requested elements
        """
        prompt = self._create_prompt(novel_concept, setting_description, character_role, character_description)
        
        if verbose:
            print("CharacterAgent> Creating character for role:", character_role)
            print("CharacterAgent> Novel concept:", novel_concept[:50] + "...")
            print("CharacterAgent> Setting:", setting_description[:50] + "...")
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_instructions},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=3000
        )

        return response.choices[0].message.content.strip()
    
    def _create_prompt(self, novel_concept: str, setting_description: str,
                      character_role: str, character_description: Optional[str] = None) -> str:
        """Create the prompt for the character creation task."""

        # Base prompt
        prompt = f"""Create a detailed character description for a young adult novel with the following parameters:

NOVEL CONCEPT: {novel_concept}

SETTING DESCRIPTION: {setting_description}

CHARACTER ROLE: {character_role}"""

        # Add initial character description if provided
        if character_description:
            prompt += f"""

INITIAL CHARACTER DESCRIPTION: {character_description}

Please expand upon this initial description to create a comprehensive character profile."""

        prompt += """

Please create a comprehensive character profile that includes:

1. PHYSICAL APPEARANCE - Detailed description of how they look, dress, and present themselves
2. PERSONAL TASTES & INTERESTS - What they like, dislike, hobbies, and preferences
3. GOALS & MOTIVATIONS - What drives them, what they want to achieve
4. STRENGTHS - Their talents, skills, and positive traits
5. FLAWS & WEAKNESSES - Their shortcomings, bad habits, and areas for growth

Make sure the character fits naturally into the provided setting and serves their narrative role effectively while being a complex, three-dimensional individual that YA readers can connect with."""

        if character_description:
            prompt += """

If an initial character description was provided, use it as a foundation but expand significantly with rich details, ensuring consistency while adding depth and complexity."""

        return prompt
    
    def generate_character_ensemble(self, novel_concept: str, setting_description: str,
                                   character_roles: list[str], character_descriptions: Optional[Dict[str, str]] = None,
                                   verbose: bool = True) -> Dict[str, str]:
        """
        Generate multiple characters for different roles in the story.

        Args:
            novel_concept: The overall concept/theme of the novel
            setting_description: Description of the novel's setting/world
            character_roles: List of character roles to create
            character_descriptions: Optional dict mapping roles to initial descriptions
            verbose: Whether to print progress messages

        Returns:
            Dictionary mapping character roles to their descriptions
        """
        characters = {}

        for role in character_roles:
            if verbose:
                print(f"Generating {role}...")

            # Get initial description if provided
            initial_desc = character_descriptions.get(role) if character_descriptions else None

            character_desc = self.generate_character(
                novel_concept, setting_description, role,
                character_description=initial_desc, verbose=False
            )
            characters[role] = character_desc

        return characters
    

    def update_instructions(self, custom_instructions: str):
        """
        Update the agent's instructions for specialized character creation tasks.

        Args:
            custom_instructions: New instructions for the agent
        """
        self.system_instructions = custom_instructions
