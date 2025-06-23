from abstract_writer_agent import AbstractWriterAgent
from typing import Dict, Optional


class OutlinerAgent(AbstractWriterAgent):
    """
    A specialized agent for creating structured young adult fiction outlines.
    
    This agent takes a novel concept, setting description, and character descriptions
    to produce a 17-chapter outline following the Hero's Journey structure.
    """
    
    def __init__(self, model: str = "gpt-4o-mini", api_key: str = None,
                 writing_style_guide: Optional[str] = None):
        """
        Initialize the OutlinerAgent.

        Args:
            model: The OpenAI model to use (default: gpt-4o-mini)
            api_key: OpenAI API key (if None, will use environment variable)
            writing_style_guide: Optional text containing writing style guidelines.
                                If None, uses the default outlining style guide
        """
        super().__init__(model, api_key, writing_style_guide)
    
    def _get_instructions(self) -> str:
        """Get the specialized instructions for the outline creation agent."""
        return """You are a professional story structure consultant specializing in young adult fiction.
        Your task is to create compelling 17-chapter outlines that follow the Hero's Journey structure,
        divided into three distinct parts.
        
        STRUCTURE REQUIREMENTS:
        - 17 chapters total, divided into 3 parts
        - Part I (Departure): Chapters 1-6
        - Part II (Initiation): Chapters 7-13  
        - Part III (Return): Chapters 14-17
        
        HERO'S JOURNEY ELEMENTS TO INCORPORATE:
        
        PART I - DEPARTURE (Chapters 1-6):
        - Ordinary World
        - Call to Adventure
        - Refusal of the Call
        - Meeting with the Mentor
        - Crossing the First Threshold
        - The Belly of the Whale
        
        PART II - INITIATION (Chapters 7-13):
        - The Road of Trials
        - Tests, Allies, and Enemies
        - Approach to the Inmost Cave
        - The Ordeal
        - Reward (Seizing the Sword)
        - The Meeting with the Goddess
        - Atonement with the Father
        
        PART III - RETURN (Chapters 14-17):
        - Refusal of the Return
        - The Magic Flight
        - Rescue from Without
        - The Crossing of the Return Threshold
        - Master of the Two Worlds
        - Freedom to Live
        
        For each chapter, provide:
        1. Chapter title
        2. Hero's Journey stage it represents
        3. 2-3 sentence summary of key events
        4. Character development focus
        5. How it advances the overall plot
        
        Focus on:
        - Strong character arcs and growth
        - Compelling conflicts and stakes
        - Emotional resonance and themes
        - Proper pacing across all three acts
        - Integration of setting elements
        - Utilization of all major characters"""

    def _get_default_style_guide(self) -> str:
        """Get the default writing style guide for outlining."""
        return """OUTLINING STYLE GUIDE:

STRUCTURE PRINCIPLES:
- Follow the Hero's Journey framework adapted for YA fiction
- Ensure clear three-act structure with proper pacing
- Balance character development with plot advancement
- Create compelling chapter hooks and cliffhangers

CHAPTER ORGANIZATION:
- Each chapter should have a clear purpose and advance the story
- Include both external plot events and internal character growth
- Vary chapter types (action, character development, world-building, etc.)
- End chapters with emotional impact or compelling questions

PACING GUIDELINES:
- Front-load world-building and character introduction in early chapters
- Build tension progressively through the middle chapters
- Create multiple climactic moments leading to the final confrontation
- Allow for proper resolution and character arc completion

NARRATIVE FLOW:
- Ensure smooth transitions between chapters and story beats
- Create satisfying character arcs that span the entire narrative
- Build subplots that enhance rather than distract from the main story
- Develop conflicts that escalate naturally and resolve meaningfully"""

    def generate_outline(self, novel_concept: str, setting_description: str,
                        characters: Dict[str, str], plot_summary: Optional[str] = None,
                        verbose: bool = True) -> str:
        """
        Generate a 17-chapter outline following the Hero's Journey structure using a two-step process:
        first generate a detailed prompt, then use that prompt to create the outline.

        Args:
            novel_concept: The overall concept/theme of the novel
            setting_description: Description of the novel's setting/world
            characters: Dictionary of character roles and their descriptions
            plot_summary: Optional single paragraph plot summary to guide the outline
            verbose: Whether to print progress messages

        Returns:
            A structured 17-chapter outline
        """

        if verbose:
            print("OutlinerAgent> Creating 17-chapter outline...")
            print("OutlinerAgent> Novel concept:", novel_concept[:50] + "...")
            print("OutlinerAgent> Characters:", list(characters.keys()))
            if plot_summary:
                print("OutlinerAgent> Using plot summary for guidance")

        # Use the parent class's two-step generation method
        return self._execute_two_step_generation(
            step1_args=(novel_concept, setting_description, characters, plot_summary),
            step1_kwargs={'verbose': verbose},
            step2_args=(),
            step2_kwargs={'verbose': verbose},
            verbose=verbose,
            agent_name="OutlinerAgent"
        )

    def _generate_detailed_prompt(self, novel_concept: str, setting_description: str,
                                 characters: Dict[str, str], plot_summary: Optional[str] = None,
                                 verbose: bool = True) -> str:
        """
        Implementation of abstract method for generating detailed prompts.
        """
        return self._generate_outline_prompt(novel_concept, setting_description, characters, plot_summary, verbose)

    def _create_content_from_prompt(self, detailed_prompt: str, verbose: bool = True) -> str:
        """
        Implementation of abstract method for creating content from prompts.
        """
        return self._create_outline_from_prompt(detailed_prompt, verbose)

    def _generate_outline_prompt(self, novel_concept: str, setting_description: str,
                                characters: Dict[str, str], plot_summary: Optional[str] = None,
                                verbose: bool = True) -> str:
        """
        Generate a detailed prompt for creating a specific outline.

        Args:
            novel_concept: The overall concept/theme of the novel
            setting_description: Description of the novel's setting/world
            characters: Dictionary of character roles and their descriptions
            plot_summary: Optional single paragraph plot summary to guide the outline
            verbose: Whether to print progress messages

        Returns:
            A detailed prompt for creating the outline
        """
        # Format character information
        character_info = self._format_character_info(characters)

        # Format plot summary section if provided
        plot_summary_section = ""
        if plot_summary:
            plot_summary_section = self._create_context_section("PLOT SUMMARY", plot_summary)

        prompt_generation_request = f"""You are a professional story structure consultant specializing in young adult fiction. Your task is to create a detailed, comprehensive prompt that will guide an AI to develop a compelling 17-chapter outline following the Hero's Journey structure for a YA novel.

{self._create_context_section("NOVEL CONCEPT", novel_concept)}

{self._create_context_section("SETTING DESCRIPTION", setting_description, max_length=500)}

{self._create_context_section("CHARACTER PROFILES", character_info)}

{plot_summary_section}

Based on the above information, create a detailed outline creation prompt that will result in a rich, well-structured 17-chapter outline. The prompt should include specific guidance for:

1. HERO'S JOURNEY INTEGRATION: How to properly map the 17 chapters to Hero's Journey stages
2. CHARACTER ARC DEVELOPMENT: How each character should grow and change throughout the story
3. PACING AND STRUCTURE: How to balance action, character development, and plot progression
4. SETTING UTILIZATION: How to effectively use the world and environment in each part
5. CONFLICT ESCALATION: How tensions and stakes should build across the three acts
6. PLOT SUMMARY ALIGNMENT: {"How to ensure the outline aligns with and expands upon the provided plot summary" if plot_summary else "How to develop compelling plot threads that serve the story"}
7. CHAPTER TRANSITIONS: How chapters should connect and flow into each other
8. CLIMAX AND RESOLUTION: How to build to a satisfying climax and meaningful resolution
9. CHARACTER RELATIONSHIPS: How relationships should develop and change
10. PLOT THREADS: How to weave multiple plot elements together effectively

The outline should be divided into:
- Part I (Departure): Chapters 1-6
- Part II (Initiation): Chapters 7-13
- Part III (Return): Chapters 14-17

{"Ensure the outline expands upon and stays true to the plot summary while providing detailed chapter-by-chapter structure." if plot_summary else ""}

Create a comprehensive prompt that will result in a detailed outline that serves as a strong foundation for writing a compelling YA novel."""

        return self._make_api_call(
            system_content="You are an expert story structure consultant who creates detailed prompts for developing compelling young adult fiction outlines.",
            user_content=prompt_generation_request,
            temperature=0.6,
            max_tokens=2000
        )

    def _create_outline_from_prompt(self, detailed_prompt: str, verbose: bool = True) -> str:
        """
        Create an outline using a detailed prompt.

        Args:
            detailed_prompt: The detailed prompt for creating the outline
            verbose: Whether to print progress messages

        Returns:
            The complete 17-chapter outline
        """
        outline_creation_instructions = """You are a professional story structure consultant specializing in young adult fiction. Your task is to create a comprehensive 17-chapter outline following the Hero's Journey structure based on the detailed prompt provided.

OUTLINE REQUIREMENTS:
- Create exactly 17 chapters divided into three parts
- Follow the Hero's Journey structure closely
- Ensure each chapter serves a specific narrative purpose
- Balance character development with plot advancement
- Create compelling conflicts and emotional stakes
- Maintain appropriate pacing for YA readers
- Integrate all characters meaningfully throughout the story

OUTLINE STRUCTURE:
Part I - DEPARTURE (Chapters 1-6)
Part II - INITIATION (Chapters 7-13)
Part III - RETURN (Chapters 14-17)

For each chapter, provide:
1. Chapter number and compelling title
2. Hero's Journey stage it represents
3. Plot summary (2-3 sentences describing key events)
4. Character development focus (which characters grow/change)
5. Setting and atmosphere notes
6. Conflict and tension elements
7. How it advances the overall story

Focus on creating an outline that provides a strong foundation for writing a compelling YA novel that will engage teenage readers while following proven story structure principles."""

        return self._make_api_call(
            system_content=outline_creation_instructions,
            user_content=detailed_prompt,
            temperature=0.7,
            max_tokens=4000
        )

    def _create_prompt(self, novel_concept: str, setting_description: str,
                      characters: Dict[str, str]) -> str:
        """Create the prompt for the outline creation task."""
        
        # Format character information
        character_info = "\n".join([
            f"{role.upper()}:\n{description[:300]}...\n" 
            for role, description in characters.items()
        ])
        
        return f"""Create a detailed 17-chapter outline for a young adult novel following the Hero's Journey structure.

NOVEL CONCEPT:
{novel_concept}

SETTING DESCRIPTION:
{setting_description}

CHARACTERS:
{character_info}

Please create a comprehensive outline with:

PART I - DEPARTURE (Chapters 1-6)
PART II - INITIATION (Chapters 7-13)
PART III - RETURN (Chapters 14-17)

For each chapter, provide:
- Chapter number and title
- Hero's Journey stage
- Plot summary (2-3 sentences)
- Character focus
- Story progression notes

Ensure the outline:
- Follows the Hero's Journey structure closely
- Integrates all provided characters meaningfully
- Utilizes the setting effectively
- Maintains appropriate pacing for YA fiction
- Creates compelling conflicts and character growth
- Builds to a satisfying climax and resolution"""
    
    def generate_detailed_chapter_breakdown(self, novel_concept: str, setting_description: str,
                                          characters: Dict[str, str], chapter_number: int,
                                          plot_summary: Optional[str] = None, verbose: bool = True) -> str:
        """
        Generate a detailed breakdown for a specific chapter using a two-step process.

        Args:
            novel_concept: The overall concept/theme of the novel
            setting_description: Description of the novel's setting/world
            characters: Dictionary of character roles and their descriptions
            chapter_number: The specific chapter to detail (1-17)
            plot_summary: Optional single paragraph plot summary to guide the breakdown
            verbose: Whether to print progress messages

        Returns:
            A detailed breakdown of the specified chapter
        """
        if not 1 <= chapter_number <= 17:
            raise ValueError("Chapter number must be between 1 and 17")

        if verbose:
            print(f"OutlinerAgent> Creating detailed breakdown for Chapter {chapter_number}")
            if plot_summary:
                print("OutlinerAgent> Using plot summary for guidance")
            print("OutlinerAgent> Step 1: Generating detailed chapter breakdown prompt...")

        # Step 1: Generate a detailed prompt for chapter breakdown
        detailed_prompt = self._generate_chapter_breakdown_prompt(
            novel_concept, setting_description, characters, chapter_number, plot_summary, verbose
        )

        if verbose:
            print("OutlinerAgent> Step 2: Creating chapter breakdown using generated prompt...")

        # Step 2: Use the detailed prompt to create the actual chapter breakdown
        breakdown_content = self._create_chapter_breakdown_from_prompt(
            detailed_prompt, chapter_number, verbose
        )

        return breakdown_content

    def _generate_chapter_breakdown_prompt(self, novel_concept: str, setting_description: str,
                                         characters: Dict[str, str], chapter_number: int,
                                         plot_summary: Optional[str] = None, verbose: bool = True) -> str:
        """
        Generate a detailed prompt for creating a specific chapter breakdown.

        Args:
            novel_concept: The overall concept/theme of the novel
            setting_description: Description of the novel's setting/world
            characters: Dictionary of character roles and their descriptions
            chapter_number: The specific chapter to detail (1-17)
            plot_summary: Optional single paragraph plot summary to guide the breakdown
            verbose: Whether to print progress messages

        Returns:
            A detailed prompt for creating the chapter breakdown
        """
        # Determine which part and Hero's Journey stage
        if 1 <= chapter_number <= 6:
            part = "I - DEPARTURE"
            stages = ["Ordinary World", "Call to Adventure", "Refusal of the Call",
                     "Meeting with the Mentor", "Crossing the First Threshold", "The Belly of the Whale"]
            stage = stages[chapter_number - 1]
        elif 7 <= chapter_number <= 13:
            part = "II - INITIATION"
            stages = ["The Road of Trials", "Tests, Allies, and Enemies", "Approach to the Inmost Cave",
                     "The Ordeal", "Reward", "The Meeting with the Goddess", "Atonement with the Father"]
            stage = stages[chapter_number - 7]
        else:  # 14-17
            part = "III - RETURN"
            stages = ["Refusal of the Return", "The Magic Flight", "Rescue from Without",
                     "The Crossing of the Return Threshold/Master of the Two Worlds/Freedom to Live"]
            stage = stages[min(chapter_number - 14, 3)]

        # Format character information
        character_info = self._format_character_info(characters)

        # Format plot summary section if provided
        plot_summary_section = ""
        if plot_summary:
            plot_summary_section = self._create_context_section("PLOT SUMMARY", plot_summary)

        prompt_generation_request = f"""You are a professional story structure consultant specializing in young adult fiction. Your task is to create a detailed, comprehensive prompt that will guide an AI to develop a compelling breakdown for Chapter {chapter_number} of a 17-chapter YA novel.

{self._create_context_section("NOVEL CONCEPT", novel_concept)}

{self._create_context_section("SETTING DESCRIPTION", setting_description, max_length=500)}

{self._create_context_section("CHARACTER PROFILES", character_info)}

{plot_summary_section}

CHAPTER CONTEXT:
- Chapter {chapter_number} (Part {part})
- Hero's Journey Stage: {stage}

Based on the above information, create a detailed chapter breakdown prompt that will result in a rich, comprehensive breakdown for Chapter {chapter_number}. The prompt should include specific guidance for:

1. SCENE STRUCTURE: How to break down the chapter into compelling scenes
2. CHARACTER FOCUS: Which characters should be featured and how they develop
3. HERO'S JOURNEY ELEMENTS: How to properly incorporate the {stage} stage
4. CONFLICT AND TENSION: What conflicts should drive this chapter
5. SETTING INTEGRATION: How to use the world effectively in this chapter
6. EMOTIONAL BEATS: What emotions and themes should be explored
7. PLOT ADVANCEMENT: How this chapter moves the overall story forward
8. PACING CONSIDERATIONS: How to structure the chapter for optimal pacing
9. CHAPTER TRANSITIONS: How to connect to previous and next chapters
10. YA APPEAL: Elements that will engage teenage readers

Create a comprehensive prompt that will result in a detailed chapter breakdown that serves as a strong foundation for writing Chapter {chapter_number} of a compelling YA novel."""

        return self._make_api_call(
            system_content="You are an expert story structure consultant who creates detailed prompts for developing compelling young adult fiction chapter breakdowns.",
            user_content=prompt_generation_request,
            temperature=0.6,
            max_tokens=2000
        )

    def _create_chapter_breakdown_from_prompt(self, detailed_prompt: str, chapter_number: int,
                                            verbose: bool = True) -> str:
        """
        Create a chapter breakdown using a detailed prompt.

        Args:
            detailed_prompt: The detailed prompt for creating the chapter breakdown
            chapter_number: The chapter number being detailed
            verbose: Whether to print progress messages

        Returns:
            The complete chapter breakdown
        """
        breakdown_creation_instructions = """You are a professional story structure consultant specializing in young adult fiction. Your task is to create a comprehensive, detailed chapter breakdown based on the detailed prompt provided.

CHAPTER BREAKDOWN REQUIREMENTS:
- Create a detailed breakdown that serves as a strong foundation for writing
- Include scene-by-scene structure with clear progression
- Focus on character development and interactions
- Integrate Hero's Journey elements appropriately
- Maintain compelling conflict and tension throughout
- Ensure age-appropriate content and themes for YA readers
- Provide specific, actionable details for each scene

BREAKDOWN STRUCTURE:
1. Chapter title (compelling and thematic)
2. Hero's Journey stage and its significance
3. Scene-by-scene breakdown with:
   - Setting and atmosphere
   - Characters involved
   - Key events and actions
   - Dialogue highlights
   - Emotional beats
4. Character development focus
5. Conflict and tension elements
6. Setting utilization
7. Plot advancement notes
8. Themes and emotional resonance
9. Transition to next chapter

Focus on creating a breakdown that provides clear, detailed guidance for writing a compelling chapter that serves its role in the overall story structure."""

        return self._make_api_call(
            system_content=breakdown_creation_instructions,
            user_content=detailed_prompt,
            temperature=0.7,
            max_tokens=2000
        )
    
    def update_instructions(self, custom_instructions: str):
        """
        Update the agent's instructions for specialized outlining tasks.

        Args:
            custom_instructions: New instructions for the agent
        """
        self.system_instructions = custom_instructions
