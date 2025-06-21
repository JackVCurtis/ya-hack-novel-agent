from abstract_writer_agent import AbstractWriterAgent
from typing import Optional, Dict


class PlotSummaryAgent(AbstractWriterAgent):
    """
    A specialized agent for creating compelling plot summaries for young adult fiction.
    
    This agent takes a novel concept, setting description, and character descriptions
    to produce a single paragraph plot summary that captures the essence of the story.
    """
    
    def __init__(self, model: str = "gpt-4o-mini", api_key: str = None,
                 writing_style_guide: Optional[str] = None):
        """
        Initialize the PlotSummaryAgent.

        Args:
            model: The OpenAI model to use (default: gpt-4o-mini)
            api_key: OpenAI API key (if None, will use environment variable)
            writing_style_guide: Optional text containing writing style guidelines.
                                If None, uses the default plot summary style guide
        """
        super().__init__(model, api_key, writing_style_guide)
    
    def _get_instructions(self) -> str:
        """Get the specialized instructions for the plot summary agent."""
        return """You are a creative plot summary specialist for young adult fiction. 
        Your task is to take a novel concept, setting description, and character descriptions 
        and craft a compelling single paragraph plot summary that captures the essence of the story.
        
        Focus on:
        - Creating a hook that immediately draws readers in
        - Establishing the main conflict and stakes
        - Highlighting the protagonist's journey and growth
        - Incorporating key setting elements that impact the plot
        - Keeping the summary concise but compelling (1 paragraph only)
        - Creating intrigue without giving away major plot twists
        - Emphasizing themes of growth, discovery, and overcoming challenges
        
        The summary should make readers want to dive into the full story immediately."""

    def _get_default_style_guide(self) -> str:
        """Get the default writing style guide for plot summaries."""
        return """PLOT SUMMARY STYLE GUIDE:
AVOID RUN-ON SENTENCES

STRUCTURE & FLOW:
- Begin with a compelling hook that establishes the protagonist and their world
- Introduce the inciting incident or main conflict early
- Build tension by highlighting what's at stake
- End with a sense of urgency or intrigue that makes readers want more
- Keep the entire summary to exactly one paragraph

TONE & LANGUAGE:
- Use active, engaging language that creates momentum
- Appeal to YA readers (ages 13-18) with age-appropriate vocabulary
- Balance accessibility with sophistication
- Create emotional resonance through character-driven conflict
- Avoid overly complex sentence structures

CONTENT GUIDELINES:
- Focus on the protagonist's journey and what they must overcome
- Highlight unique aspects of the setting that impact the story
- Establish clear stakes - what happens if the protagonist fails?
- Include hints of character growth and transformation
- Create intrigue without spoiling major plot points
- Emphasize themes relevant to young adult readers

WHAT TO AVOID:
- Multiple paragraphs or lengthy descriptions
- Giving away major plot twists or the ending
- Overly detailed world-building exposition
- Passive voice or static descriptions
- Generic or clichéd language"""
    
    def generate_plot_summary(self, novel_concept: str, setting_description: str, 
                             characters: Dict[str, str], verbose: bool = True) -> str:
        """
        Generate a compelling plot summary for a YA novel using a two-step process:
        first generate a detailed prompt, then use that prompt to create the summary.

        Args:
            novel_concept: General concept/theme of the novel
            setting_description: Description of the novel's setting
            characters: Dictionary of character roles and descriptions
            verbose: Whether to print progress messages

        Returns:
            A single paragraph plot summary
        """

        if verbose:
            print("PlotSummaryAgent> Processing novel concept:", novel_concept[:50] + "...")
            print("PlotSummaryAgent> Setting:", setting_description[:50] + "...")
            print("PlotSummaryAgent> Characters:", list(characters.keys()))

        # Use the parent class's two-step generation method
        return self._execute_two_step_generation(
            step1_args=(novel_concept, setting_description, characters),
            step1_kwargs={'verbose': verbose},
            step2_args=(novel_concept, setting_description, characters),
            step2_kwargs={'verbose': verbose},
            verbose=verbose,
            agent_name="PlotSummaryAgent"
        )

    def _generate_detailed_prompt(self, novel_concept: str, setting_description: str,
                                 characters: Dict[str, str], verbose: bool = True) -> str:
        """
        Implementation of abstract method for generating detailed prompts.
        """
        return self._generate_plot_summary_prompt(novel_concept, setting_description, characters, verbose)

    def _create_content_from_prompt(self, detailed_prompt: str, novel_concept: str = None,
                                   setting_description: str = None, characters: Dict[str, str] = None,
                                   verbose: bool = True) -> str:
        """
        Implementation of abstract method for creating content from prompts.
        """
        return self._create_plot_summary_from_prompt(detailed_prompt, verbose)

    def _generate_plot_summary_prompt(self, novel_concept: str, setting_description: str,
                                     characters: Dict[str, str], verbose: bool = True) -> str:
        """
        Generate a detailed prompt for creating a plot summary.

        Args:
            novel_concept: General concept/theme of the novel
            setting_description: Description of the novel's setting
            characters: Dictionary of character roles and descriptions
            verbose: Whether to print progress messages

        Returns:
            A detailed prompt for creating the plot summary
        """
        # Format character information
        character_info = self._format_character_info(characters, max_length=300)
        
        prompt_generation_request = f"""You are a professional plot development consultant specializing in young adult fiction. Your task is to create a detailed, comprehensive prompt that will guide an AI to develop a compelling single paragraph plot summary for a YA novel.

{self._create_context_section("NOVEL CONCEPT", novel_concept)}

{self._create_context_section("SETTING DESCRIPTION", setting_description, max_length=500)}

{self._create_context_section("CHARACTER DESCRIPTIONS", character_info)}

{self._get_style_guide_section()}

Based on the above information, create a detailed plot summary prompt that will result in a compelling single paragraph summary that will captivate YA readers and make them want to read the full novel. The prompt should include specific guidance for:

1. OPENING HOOK: How to begin the summary to immediately engage readers
2. PROTAGONIST FOCUS: How to establish the main character and their initial situation
3. CONFLICT INTRODUCTION: How to present the central conflict or challenge
4. STAKES ESTABLISHMENT: What the protagonist stands to lose or gain
5. SETTING INTEGRATION: How the unique aspects of the setting impact the plot
6. CHARACTER DYNAMICS: How relationships and character interactions drive the story
7. TENSION BUILDING: How to create urgency and momentum in the summary
8. INTRIGUE CREATION: How to hint at deeper mysteries or complications without spoiling
9. EMOTIONAL RESONANCE: How to connect with readers on an emotional level

Create a comprehensive prompt that will result in a plot summary that feels dynamic, engaging, and perfectly suited for young adult fiction while making readers desperate to know what happens next."""

        return self._make_api_call(
            system_content="You are an expert plot development consultant who creates detailed prompts for developing compelling young adult fiction plot summaries.",
            user_content=prompt_generation_request,
            temperature=0.6,
            max_tokens=2000
        )

    def _create_plot_summary_from_prompt(self, detailed_prompt: str, verbose: bool = True) -> str:
        """
        Create a plot summary using a detailed prompt.

        Args:
            detailed_prompt: The detailed prompt for creating the plot summary
            verbose: Whether to print progress messages

        Returns:
            The complete plot summary
        """
        plot_summary_instructions = """You are a professional plot summary writer specializing in young adult fiction. Your task is to create a compelling single paragraph plot summary based on the detailed prompt provided.

PLOT SUMMARY REQUIREMENTS:
- Write exactly ONE paragraph that captures the essence of the story
- Begin with a hook that immediately draws readers in
- Establish the protagonist, their world, and the central conflict
- Highlight what's at stake and why readers should care
- Use language that appeals to YA readers (ages 13-18)
- Create momentum and urgency throughout the summary
- End with intrigue that makes readers want to know more
- Avoid giving away major plot twists or the ending

WRITING STYLE:
- Active, engaging prose that creates forward momentum
- Age-appropriate vocabulary that challenges without overwhelming
- Emotional resonance through character-driven conflict
- Balance of action, character development, and world-building elements
- Clear, compelling language that avoids clichés

Focus on creating a plot summary that serves as an irresistible invitation to read the full novel - one that captures the heart of the story while leaving readers hungry for more."""

        return self._make_api_call(
            system_content=plot_summary_instructions,
            user_content=detailed_prompt,
            temperature=0.7,
            max_tokens=1000
        )
