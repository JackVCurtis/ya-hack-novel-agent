from llama_stack_client import Agent, LlamaStackClient, AgentEventLogger
from typing import Dict, List


class OutlinerAgent:
    """
    A specialized agent for creating structured young adult fiction outlines.
    
    This agent takes a novel concept, setting description, and character descriptions
    to produce a 17-chapter outline following the Hero's Journey structure.
    """
    
    def __init__(self, base_url: str = "http://localhost:8321"):
        """
        Initialize the OutlinerAgent.
        
        Args:
            base_url: The base URL for the LlamaStack client
        """
        self.base_url = base_url
        self.client = None
        self.model_id = None
        self.agent = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the LlamaStack client and set up the agent."""
        self.client = LlamaStackClient(base_url=self.base_url)
        
        models = self.client.models.list()
        self.model_id = next(m for m in models if m.model_type == "llm").identifier
        
        self.agent = Agent(
            self.client,
            model=self.model_id,
            instructions=self._get_instructions(),
            tools=[]
        )
    
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
        - Age-appropriate content for YA readers
        - Strong character arcs and growth
        - Compelling conflicts and stakes
        - Emotional resonance and themes
        - Proper pacing across all three acts
        - Integration of setting elements
        - Utilization of all major characters"""
    
    def generate_outline(self, novel_concept: str, setting_description: str, 
                        characters: Dict[str, str], verbose: bool = True) -> str:
        """
        Generate a 17-chapter outline following the Hero's Journey structure.
        
        Args:
            novel_concept: The overall concept/theme of the novel
            setting_description: Description of the novel's setting/world
            characters: Dictionary of character roles and their descriptions
            verbose: Whether to print progress messages
            
        Returns:
            A structured 17-chapter outline
        """
        if not self.agent:
            raise RuntimeError("Agent not properly initialized")
        
        prompt = self._create_prompt(novel_concept, setting_description, characters)
        
        if verbose:
            print("OutlinerAgent> Creating 17-chapter outline...")
            print("OutlinerAgent> Novel concept:", novel_concept[:50] + "...")
            print("OutlinerAgent> Characters:", list(characters.keys()))
        
        response = self.agent.create_turn(
            messages=[{"role": "user", "content": prompt}],
            session_id=self.agent.create_session("outline_creation"),
            stream=True,
        )

        # Extract the content from the response
        result = ""
        for log in AgentEventLogger().log(response):
            result += log.content
        
        return result.strip()
    
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
                                          verbose: bool = True) -> str:
        """
        Generate a detailed breakdown for a specific chapter.
        
        Args:
            novel_concept: The overall concept/theme of the novel
            setting_description: Description of the novel's setting/world
            characters: Dictionary of character roles and their descriptions
            chapter_number: The specific chapter to detail (1-17)
            verbose: Whether to print progress messages
            
        Returns:
            A detailed breakdown of the specified chapter
        """
        if not 1 <= chapter_number <= 17:
            raise ValueError("Chapter number must be between 1 and 17")
        
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
        
        character_info = "\n".join([
            f"{role.upper()}:\n{description[:200]}...\n" 
            for role, description in characters.items()
        ])
        
        prompt = f"""Create a detailed breakdown for Chapter {chapter_number} of a 17-chapter YA novel.

NOVEL CONCEPT: {novel_concept}
SETTING: {setting_description}
CHARACTERS: {character_info}

CHAPTER DETAILS:
- Chapter {chapter_number} (Part {part})
- Hero's Journey Stage: {stage}

Please provide:
1. Chapter title
2. Detailed scene-by-scene breakdown
3. Character interactions and development
4. Specific setting usage
5. Conflict and tension elements
6. How this chapter advances the overall story
7. Emotional beats and themes
8. Transition to next chapter

Focus on creating a compelling, detailed chapter that serves its role in the Hero's Journey while maintaining YA appeal."""
        
        if verbose:
            print(f"OutlinerAgent> Creating detailed breakdown for Chapter {chapter_number}")
            print(f"OutlinerAgent> Hero's Journey Stage: {stage}")
        
        response = self.agent.create_turn(
            messages=[{"role": "user", "content": prompt}],
            session_id=self.agent.create_session(f"chapter_{chapter_number}_detail"),
            stream=True,
        )

        result = ""
        for log in AgentEventLogger().log(response):
            result += log.content
        
        return result.strip()
    
    def update_instructions(self, custom_instructions: str):
        """
        Update the agent's instructions for specialized outlining tasks.
        
        Args:
            custom_instructions: New instructions for the agent
        """
        self.agent = Agent(
            self.client,
            model=self.model_id,
            instructions=custom_instructions,
            tools=[]
        )
