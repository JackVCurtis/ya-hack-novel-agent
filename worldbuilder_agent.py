from openai import OpenAI
from typing import Optional


class WorldbuilderAgent:
    """
    A specialized agent for creating compelling young adult fiction setting descriptions.
    
    This agent takes a setting description and novel concept to produce engaging,
    atmospheric worldbuilding content tailored for YA audiences.
    """
    
    def __init__(self, model: str = "gpt-4o-mini", api_key: str = None):
        """
        Initialize the WorldbuilderAgent.

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
        """Get the specialized instructions for the worldbuilding agent."""
        return """You are a creative worldbuilding assistant specializing in young adult fiction. 
        Your task is to take a setting description and novel concept and craft a compelling, 
        atmospheric setting description that would appeal to YA readers.
        
        Focus on:
        - Creating vivid, immersive details
        - Establishing mood and atmosphere
        - Highlighting unique or intriguing elements
        - Using language that resonates with young adult audiences
        - Keeping descriptions concise but evocative (2-3 paragraphs max)
        - Incorporating elements that suggest conflict, mystery, or adventure
        
        Avoid overly complex world-building details - focus on what makes the setting 
        feel alive and compelling for the story."""
    
    def generate_setting(self, setting_description: str, novel_concept: str,
                        verbose: bool = True) -> str:
        """
        Generate a compelling setting description for a YA novel using a two-step process:
        first generate a detailed prompt, then use that prompt to create the setting.

        Args:
            setting_description: Description of the young adult novel setting
            novel_concept: General concept/theme of the novel
            verbose: Whether to print progress messages

        Returns:
            A short, polished description of the setting
        """

        if verbose:
            print("WorldbuilderAgent> Processing setting:", setting_description[:50] + "...")
            print("WorldbuilderAgent> Novel concept:", novel_concept[:50] + "...")
            print("WorldbuilderAgent> Step 1: Generating detailed worldbuilding prompt...")

        # Step 1: Generate a detailed prompt for worldbuilding
        detailed_prompt = self._generate_worldbuilding_prompt(
            setting_description, novel_concept, verbose
        )

        if verbose:
            print("WorldbuilderAgent> Step 2: Creating setting using generated prompt...")

        # Step 2: Use the detailed prompt to create the actual setting
        setting_content = self._create_setting_from_prompt(
            detailed_prompt, verbose
        )

        return setting_content

    def _generate_worldbuilding_prompt(self, setting_description: str, novel_concept: str,
                                      verbose: bool = True) -> str:
        """
        Generate a detailed prompt for creating a specific setting.

        Args:
            setting_description: Description of the young adult novel setting
            novel_concept: General concept/theme of the novel
            verbose: Whether to print progress messages

        Returns:
            A detailed prompt for creating the setting
        """
        prompt_generation_request = f"""You are a professional worldbuilding consultant specializing in young adult fiction. Your task is to create a detailed, comprehensive prompt that will guide an AI to develop a compelling setting description for a YA novel.

SETTING DESCRIPTION:
{setting_description}

NOVEL CONCEPT:
{novel_concept}

Based on the above information, create a detailed worldbuilding prompt that will result in a rich, atmospheric setting description (2-3 paragraphs) that will captivate YA readers. The prompt should include specific guidance for:

1. ATMOSPHERIC DETAILS: What sensory elements should be emphasized to create mood
2. VISUAL IMAGERY: Specific visual elements that make the setting memorable and unique
3. CULTURAL ELEMENTS: Social structures, customs, or unique aspects of this world
4. CONFLICT POTENTIAL: Environmental or societal elements that suggest tension or adventure
5. YA APPEAL: Elements that will resonate with teenage readers and their experiences
6. STORY INTEGRATION: How the setting should support and enhance the novel's themes
7. IMMERSIVE QUALITIES: Details that make readers feel like they're truly in this world
8. MYSTERY/INTRIGUE: Elements that create questions and draw readers deeper into the world

Create a comprehensive prompt that will result in a setting description that feels vivid, engaging, and perfectly suited for young adult fiction while supporting the story's themes and conflicts."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert worldbuilding consultant who creates detailed prompts for developing compelling young adult fiction settings."},
                {"role": "user", "content": prompt_generation_request}
            ],
            temperature=0.6,
            max_tokens=2000
        )

        return response.choices[0].message.content.strip()

    def _create_setting_from_prompt(self, detailed_prompt: str, verbose: bool = True) -> str:
        """
        Create a setting description using a detailed prompt.

        Args:
            detailed_prompt: The detailed prompt for creating the setting
            verbose: Whether to print progress messages

        Returns:
            The complete setting description
        """
        setting_creation_instructions = """You are a professional worldbuilder specializing in young adult fiction. Your task is to create a compelling, atmospheric setting description based on the detailed prompt provided.

SETTING DESCRIPTION REQUIREMENTS:
- Create a vivid, immersive setting that appeals to YA readers
- Write 2-3 paragraphs that bring the world to life
- Include sensory details that establish mood and atmosphere
- Highlight unique or intriguing elements that suggest adventure or conflict
- Use language that resonates with young adult audiences
- Focus on elements that make the setting feel alive and compelling
- Avoid overly complex world-building details - prioritize atmosphere and engagement

WRITING STYLE:
- Evocative and atmospheric prose
- Age-appropriate language for 13-18 year old readers
- Balance of concrete details and emotional resonance
- Create a sense of place that readers want to explore
- Integrate elements that support potential story conflicts and themes

Focus on creating a setting description that immediately draws readers in and makes them want to know more about this world and the stories that unfold within it."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": setting_creation_instructions},
                {"role": "user", "content": detailed_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        return response.choices[0].message.content.strip()

    def _create_prompt(self, setting_description: str, novel_concept: str) -> str:
        """Create the prompt for the worldbuilding task."""
        return f"""Based on the following information, create a short, engaging setting description for a young adult novel:

Setting Description: {setting_description}
Novel Concept: {novel_concept}

Please craft a 2-3 paragraph description that brings this world to life and makes readers want to explore it further."""
    
    def generate_multiple_variations(self, setting_description: str, novel_concept: str,
                                   count: int = 3, verbose: bool = True) -> list[str]:
        """
        Generate multiple variations of a setting description using the two-step process.

        Args:
            setting_description: Description of the young adult novel setting
            novel_concept: General concept/theme of the novel
            count: Number of variations to generate
            verbose: Whether to print progress messages

        Returns:
            List of setting description variations
        """
        variations = []

        for i in range(count):
            if verbose:
                print(f"Generating variation {i + 1}/{count}...")
                print(f"WorldbuilderAgent> Step 1: Generating variation prompt {i + 1}...")

            # Step 1: Generate a detailed prompt with variation instructions
            detailed_prompt = self._generate_worldbuilding_prompt(
                setting_description, novel_concept, verbose=False
            )

            # Add variation instruction to the detailed prompt
            variation_instruction = f"\n\nIMPORTANT: This is variation #{i + 1} of {count}. Please provide a unique perspective, emphasis, or angle while maintaining the core elements and themes. Focus on different aspects or present the setting from a fresh viewpoint."
            detailed_prompt += variation_instruction

            if verbose:
                print(f"WorldbuilderAgent> Step 2: Creating variation {i + 1} using generated prompt...")

            # Step 2: Create the setting variation using the detailed prompt
            result = self._create_setting_from_prompt(detailed_prompt, verbose=False)
            variations.append(result)

        return variations

    def update_instructions(self, custom_instructions: str):
        """
        Update the agent's instructions for specialized worldbuilding tasks.

        Args:
            custom_instructions: New instructions for the agent
        """
        self.system_instructions = custom_instructions
