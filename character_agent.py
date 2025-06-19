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
                          existing_characters: Optional[Dict[str, str]] = None,
                          verbose: bool = True) -> str:
        """
        Generate a comprehensive character description for a YA novel using a two-step process:
        first generate a detailed prompt, then use that prompt to create the character.

        Args:
            novel_concept: The overall concept/theme of the novel
            setting_description: Description of the novel's setting/world
            character_role: The character's role (protagonist, antagonist, ally, etc.)
            character_description: Optional initial character description to build upon
            existing_characters: Optional dictionary of existing character descriptions for context
            verbose: Whether to print progress messages

        Returns:
            A detailed character description with all requested elements
        """

        if verbose:
            print(f"CharacterAgent> Creating character for role: {character_role}")
            print("CharacterAgent> Step 1: Generating detailed character prompt...")

        # Step 1: Generate a detailed prompt for character creation
        detailed_prompt = self._generate_character_prompt(
            novel_concept, setting_description, character_role,
            character_description, existing_characters, verbose
        )

        if verbose:
            print("CharacterAgent> Step 2: Creating character using generated prompt...")

        # Step 2: Use the detailed prompt to create the actual character
        character_content = self._create_character_from_prompt(
            detailed_prompt, character_role, verbose
        )

        return character_content

    def _generate_character_prompt(self, novel_concept: str, setting_description: str,
                                  character_role: str, character_description: Optional[str] = None,
                                  existing_characters: Optional[Dict[str, str]] = None,
                                  verbose: bool = True) -> str:
        """
        Generate a detailed prompt for creating a specific character.

        Args:
            novel_concept: The overall concept/theme of the novel
            setting_description: Description of the novel's setting/world
            character_role: The character's role (protagonist, antagonist, ally, etc.)
            character_description: Optional initial character description to build upon
            existing_characters: Optional dictionary of existing character descriptions for context
            verbose: Whether to print progress messages

        Returns:
            A detailed prompt for creating the character
        """
        # Format existing character information if provided
        existing_character_info = ""
        if existing_characters:
            existing_character_info = "\n".join([
                f"{role.upper()}:\n{description}\n"
                for role, description in existing_characters.items()
            ])
            existing_character_info = f"""
EXISTING CHARACTERS ALREADY CREATED:
{existing_character_info}

The new character should complement and interact well with these existing characters while being distinct and unique.
"""

        # Handle initial character description
        initial_description_context = ""
        if character_description:
            initial_description_context = f"""
INITIAL CHARACTER DESCRIPTION PROVIDED:
{character_description}

Please use this as a foundation but expand significantly with rich details, ensuring consistency while adding depth and complexity.
"""

        prompt_generation_request = f"""You are a professional character development coach specializing in young adult fiction. Your task is to create a detailed, comprehensive prompt that will guide an AI to develop a compelling {character_role} character for a YA novel.

NOVEL CONCEPT:
{novel_concept}

SETTING DESCRIPTION:
{setting_description}

CHARACTER ROLE: {character_role}
{existing_character_info}{initial_description_context}

Based on the above information, create a detailed character creation prompt that will result in a rich, three-dimensional {character_role} character. The prompt should include specific guidance for:

1. PHYSICAL APPEARANCE: Detailed visual description that fits the setting and role
2. PERSONALITY TRAITS: Complex personality with both strengths and flaws
3. BACKGROUND & HISTORY: Personal history that shapes who they are
4. GOALS & MOTIVATIONS: What drives them and what they want to achieve
5. RELATIONSHIPS: How they relate to others and existing characters
6. CHARACTER ARC POTENTIAL: How they can grow and change throughout the story
7. DIALOGUE VOICE: How they speak and express themselves
8. ROLE-SPECIFIC ELEMENTS: How they fulfill their narrative function
9. YA APPEAL: What makes them relatable and engaging to teenage readers

Create a comprehensive prompt that will result in a detailed character profile that feels authentic, serves the story, and resonates with YA readers."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert character development coach who creates detailed prompts for developing compelling young adult fiction characters."},
                {"role": "user", "content": prompt_generation_request}
            ],
            temperature=0.6,
            max_tokens=2000
        )

        return response.choices[0].message.content.strip()

    def _create_character_from_prompt(self, detailed_prompt: str, character_role: str,
                                     verbose: bool = True) -> str:
        """
        Create a character using a detailed prompt.

        Args:
            detailed_prompt: The detailed prompt for creating the character
            character_role: The character's role (for reference)
            verbose: Whether to print progress messages

        Returns:
            The complete character description
        """
        character_creation_instructions = """You are a professional character developer specializing in young adult fiction. Your task is to create a comprehensive, engaging character based on the detailed prompt provided.

CHARACTER PROFILE REQUIREMENTS:
- Create a three-dimensional character that feels authentic and relatable to YA readers
- Include detailed physical appearance, personality, background, and motivations
- Balance strengths and flaws to avoid Mary Sue/Gary Stu characters
- Ensure the character fits naturally into the provided setting
- Make them serve their narrative role while being a complex individual
- Include specific details that make them memorable and unique

CHARACTER PROFILE STRUCTURE:
1. PHYSICAL APPEARANCE: Detailed visual description including age, build, distinctive features, style
2. PERSONALITY: Core traits, quirks, how they interact with others, emotional patterns
3. BACKGROUND & HISTORY: Personal history, family, formative experiences
4. GOALS & MOTIVATIONS: Primary and secondary goals, internal drives, fears
5. STRENGTHS: Natural talents, learned skills, positive traits
6. FLAWS & WEAKNESSES: Character flaws, bad habits, areas for growth
7. RELATIONSHIPS: How they relate to others, social dynamics
8. VOICE & MANNERISMS: How they speak, distinctive behaviors, expressions

Focus on creating a character that YA readers will connect with emotionally while serving the story effectively."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": character_creation_instructions},
                {"role": "user", "content": detailed_prompt}
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
        Each character is created with awareness of previously created characters.

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

            # Pass existing characters as context for new character creation
            character_desc = self.generate_character(
                novel_concept, setting_description, role,
                character_description=initial_desc,
                existing_characters=characters,  # Pass existing characters for context
                verbose=False
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
