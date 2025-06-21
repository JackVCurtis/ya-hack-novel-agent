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
        and craft a compelling single paragraph plot summary that follows clear narrative structure.

        REQUIRED NARRATIVE STRUCTURE (within one paragraph):
        1. BEGINNING: Establish the protagonist in their ordinary world
        2. RISING ACTION: Introduce the inciting incident and escalating challenges
        3. CLIMAX: Hint at the major confrontation or turning point
        4. FALLING ACTION: Suggest the resolution path without spoiling the outcome

        Focus on:
        - Creating a hook that immediately draws readers in
        - Following the four-part narrative structure seamlessly within one paragraph
        - Establishing clear stakes and what the protagonist must overcome
        - Highlighting the protagonist's journey and potential for growth
        - Incorporating key setting elements that impact the plot
        - Creating intrigue without giving away major plot twists
        - Emphasizing themes of growth, discovery, and overcoming challenges

        The summary should make readers want to dive into the full story immediately while providing a complete narrative arc preview."""

    def _get_default_style_guide(self) -> str:
        """Get the default writing style guide for plot summaries."""
        return """PLOT SUMMARY STYLE GUIDE:
AVOID RUN-ON SENTENCES

NARRATIVE STRUCTURE (within one paragraph):
1. BEGINNING (1-2 sentences): Establish protagonist in their ordinary world, introduce their initial situation
2. RISING ACTION (2-3 sentences): Present the inciting incident, escalating challenges, and mounting obstacles
3. CLIMAX (1-2 sentences): Hint at the major confrontation or turning point without revealing specifics
4. FALLING ACTION (1 sentence): Suggest the resolution path and character growth without spoiling the outcome

STRUCTURE & FLOW:
- Begin with a compelling hook that establishes the protagonist and their ordinary world
- Smoothly transition through the four narrative beats within one cohesive paragraph
- Build tension progressively from beginning through climax
- End with intrigue about the resolution that makes readers want more
- Keep the entire summary to exactly one paragraph (6-8 sentences total)

TONE & LANGUAGE:
- Use active, engaging language that creates momentum
- Appeal to YA readers (ages 13-18) with age-appropriate vocabulary
- Balance accessibility with sophistication
- Create emotional resonance through character-driven conflict
- Employ transitional phrases to connect narrative beats smoothly

CONTENT GUIDELINES:
- Focus on the protagonist's complete journey arc from ordinary world to transformation
- Highlight unique aspects of the setting that impact each story phase
- Establish clear stakes that escalate throughout the narrative structure
- Include hints of character growth and transformation in the falling action
- Create intrigue without spoiling major plot points or the final resolution
- Emphasize themes relevant to young adult readers throughout the arc

WHAT TO AVOID:
- Multiple paragraphs or lengthy descriptions
- Giving away major plot twists or the ending
- Skipping any of the four narrative structure elements
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

Based on the above information, create a detailed plot summary prompt that will result in a compelling single paragraph summary following clear narrative structure that will captivate YA readers and make them want to read the full novel. The prompt should include specific guidance for:

1. NARRATIVE STRUCTURE: How to seamlessly incorporate beginning, rising action, climax, and falling action within one paragraph
2. BEGINNING ESTABLISHMENT: How to establish the protagonist in their ordinary world and initial situation
3. RISING ACTION DEVELOPMENT: How to introduce the inciting incident and escalating challenges
4. CLIMAX POSITIONING: How to hint at the major confrontation or turning point without spoiling
5. FALLING ACTION SUGGESTION: How to suggest resolution and character growth without revealing the ending
6. STAKES PROGRESSION: How stakes should escalate through each narrative beat
7. SETTING INTEGRATION: How the unique aspects of the setting impact each story phase
8. CHARACTER ARC: How to show the protagonist's complete journey from ordinary world to transformation
9. TENSION BUILDING: How to create urgency and momentum that builds through the structure
10. EMOTIONAL RESONANCE: How to connect with readers on an emotional level throughout the arc

Ensure the prompt emphasizes that all four narrative elements (beginning, rising action, climax, falling action) must be present and clearly identifiable within the single paragraph, creating a complete story arc preview.

Create a comprehensive prompt that will result in a plot summary that feels dynamic, engaging, structurally complete, and perfectly suited for young adult fiction while making readers desperate to know what happens next."""

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
        plot_summary_instructions = """You are a professional plot summary writer specializing in young adult fiction. Your task is to create a compelling single paragraph plot summary that follows clear narrative structure based on the detailed prompt provided.

MANDATORY NARRATIVE STRUCTURE (within one paragraph):
1. BEGINNING (1-2 sentences): Establish protagonist in ordinary world, show their initial situation
2. RISING ACTION (2-3 sentences): Introduce inciting incident, escalating challenges, mounting obstacles
3. CLIMAX (1-2 sentences): Hint at major confrontation/turning point without revealing specifics
4. FALLING ACTION (1 sentence): Suggest resolution path and character growth without spoiling outcome

PLOT SUMMARY REQUIREMENTS:
- Write exactly ONE paragraph (6-8 sentences) that includes all four narrative beats
- Begin with the protagonist in their ordinary world (BEGINNING)
- Transition smoothly to the inciting incident and challenges (RISING ACTION)
- Build to hint at the major confrontation (CLIMAX)
- End by suggesting transformation and resolution path (FALLING ACTION)
- Use language that appeals to YA readers (ages 13-18)
- Create momentum that builds through each narrative beat
- Avoid giving away major plot twists or the specific ending

WRITING STYLE:
- Active, engaging prose that creates forward momentum through the structure
- Smooth transitions between narrative beats within the paragraph
- Age-appropriate vocabulary that challenges without overwhelming
- Emotional resonance through character-driven conflict progression
- Balance of action, character development, and world-building elements
- Clear, compelling language that avoids clichés

CRITICAL: The summary must contain all four narrative elements in sequence and be identifiable as a complete story arc preview. Each beat should flow naturally into the next while maintaining the single paragraph format.

Focus on creating a plot summary that serves as an irresistible invitation to read the full novel - one that captures the complete narrative arc while leaving readers hungry for the detailed journey."""

        return self._make_api_call(
            system_content=plot_summary_instructions,
            user_content=detailed_prompt,
            temperature=0.7,
            max_tokens=1000
        )
