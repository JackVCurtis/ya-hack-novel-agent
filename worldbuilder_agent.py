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
        Generate a compelling setting description for a YA novel.
        
        Args:
            setting_description: Description of the young adult novel setting
            novel_concept: General concept/theme of the novel
            verbose: Whether to print progress messages
            
        Returns:
            A short, polished description of the setting
        """
        prompt = self._create_prompt(setting_description, novel_concept)

        if verbose:
            print("WorldbuilderAgent> Processing setting:", setting_description[:50] + "...")
            print("WorldbuilderAgent> Novel concept:", novel_concept[:50] + "...")

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_instructions},
                {"role": "user", "content": prompt}
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
        Generate multiple variations of a setting description.
        
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
            
            # Add variation instruction to the prompt
            variation_prompt = self._create_prompt(setting_description, novel_concept)
            variation_prompt += f"\n\nThis is variation #{i + 1}. Please provide a unique perspective or emphasis while maintaining the core elements."
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_instructions},
                    {"role": "user", "content": variation_prompt}
                ],
                temperature=0.8,  # Slightly higher for variations
                max_tokens=2000
            )

            result = response.choices[0].message.content.strip()
            
            variations.append(result)

        return variations

    def update_instructions(self, custom_instructions: str):
        """
        Update the agent's instructions for specialized worldbuilding tasks.

        Args:
            custom_instructions: New instructions for the agent
        """
        self.system_instructions = custom_instructions
