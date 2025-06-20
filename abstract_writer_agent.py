from abc import ABC, abstractmethod
from openai import OpenAI
from typing import Optional, Dict


class AbstractWriterAgent(ABC):
    """
    Abstract base class for all writer agents that follow the two-step pattern:
    1. Generate a detailed prompt from context
    2. Use that prompt to create the actual content
    
    This class provides common functionality for OpenAI client initialization,
    instruction management, and the core two-step generation pattern.
    """
    
    def __init__(self, model: str = "gpt-4o-mini", api_key: str = None,
                 writing_style_guide: Optional[str] = None):
        """
        Initialize the AbstractWriterAgent.

        Args:
            model: The OpenAI model to use (default: gpt-4o-mini)
            api_key: OpenAI API key (if None, will use environment variable)
            writing_style_guide: Optional text containing writing style guidelines.
                                If None, uses the default style guide from _get_default_style_guide()
        """
        self.model = model
        self.client = OpenAI(api_key=api_key)
        self.writing_style_guide = writing_style_guide or self._get_default_style_guide()
        self.system_instructions = self._get_instructions()

    def _initialize_client(self):
        """Initialize the OpenAI client - kept for compatibility."""
        pass  # No longer needed with OpenAI client

    @abstractmethod
    def _get_instructions(self) -> str:
        """
        Get the specialized instructions for this specific agent.

        Returns:
            String containing the system instructions for the agent
        """
        pass

    @abstractmethod
    def _get_default_style_guide(self) -> str:
        """
        Get the default writing style guide for this specific agent.

        Returns:
            String containing the default writing style guidelines for the agent
        """
        pass

    def _make_api_call(self, system_content: str, user_content: str, 
                      temperature: float = 0.6, max_tokens: int = 2000) -> str:
        """
        Make a standardized API call to OpenAI.
        
        Args:
            system_content: The system message content
            user_content: The user message content
            temperature: The temperature for generation (default: 0.6)
            max_tokens: Maximum tokens to generate (default: 2000)
            
        Returns:
            The generated content from the API
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content.strip()

    @abstractmethod
    def _generate_detailed_prompt(self, *args, **kwargs) -> str:
        """
        Generate a detailed prompt for content creation (Step 1 of two-step process).
        
        This method should take the input parameters and create a comprehensive
        prompt that will guide the content generation in step 2.
        
        Returns:
            A detailed prompt for content creation
        """
        pass

    @abstractmethod
    def _create_content_from_prompt(self, detailed_prompt: str, *args, **kwargs) -> str:
        """
        Create the actual content using the detailed prompt (Step 2 of two-step process).
        
        Args:
            detailed_prompt: The detailed prompt generated in step 1
            *args, **kwargs: Additional arguments specific to the content type
            
        Returns:
            The generated content
        """
        pass

    def _execute_two_step_generation(self, step1_args: tuple, step1_kwargs: dict,
                                   step2_args: tuple, step2_kwargs: dict,
                                   verbose: bool = True, agent_name: str = "Agent") -> str:
        """
        Execute the standard two-step generation process.
        
        Args:
            step1_args: Arguments for step 1 (prompt generation)
            step1_kwargs: Keyword arguments for step 1
            step2_args: Arguments for step 2 (content creation)
            step2_kwargs: Keyword arguments for step 2
            verbose: Whether to print progress messages
            agent_name: Name of the agent for verbose output
            
        Returns:
            The generated content
        """
        if verbose:
            print(f"{agent_name}> Step 1: Generating detailed prompt...")

        # Step 1: Generate detailed prompt
        detailed_prompt = self._generate_detailed_prompt(*step1_args, **step1_kwargs)

        if verbose:
            print(f"{agent_name}> Step 2: Creating content using generated prompt...")

        # Step 2: Create content from prompt
        content = self._create_content_from_prompt(detailed_prompt, *step2_args, **step2_kwargs)

        return content

    def update_instructions(self, custom_instructions: str):
        """
        Update the agent's instructions for specialized tasks.

        Args:
            custom_instructions: New instructions for the agent
        """
        self.system_instructions = custom_instructions

    def _format_character_info(self, characters: Dict[str, str], max_length: Optional[int] = None) -> str:
        """
        Helper method to format character information consistently across agents.
        
        Args:
            characters: Dictionary of character roles and descriptions
            max_length: Optional maximum length for each character description
            
        Returns:
            Formatted character information string
        """
        if max_length:
            return "\n".join([
                f"{role.upper()}:\n{description[:max_length]}{'...' if len(description) > max_length else ''}\n"
                for role, description in characters.items()
            ])
        else:
            return "\n".join([
                f"{role.upper()}:\n{description}\n"
                for role, description in characters.items()
            ])

    def _create_context_section(self, title: str, content: str, max_length: Optional[int] = None) -> str:
        """
        Helper method to create formatted context sections for prompts.

        Args:
            title: The section title
            content: The section content
            max_length: Optional maximum length for content truncation

        Returns:
            Formatted context section
        """
        if max_length and len(content) > max_length:
            content = content[:max_length] + "..."

        return f"{title}:\n{content}\n"

    def _get_style_guide_section(self) -> str:
        """
        Get a formatted writing style guide section for inclusion in prompts.

        Returns:
            Formatted writing style guide section
        """
        return self._create_context_section("WRITING STYLE GUIDE", self.writing_style_guide)
