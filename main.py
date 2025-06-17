from llama_stack_client import Agent, AgentEventLogger, RAGDocument, LlamaStackClient
from worldbuilder_agent import WorldbuilderAgent
from character_agent import CharacterAgent
from outliner_agent import OutlinerAgent
from chapter_agent import ChapterAgent

def main():
    vector_db_id = "my_demo_vector_db"
    client = LlamaStackClient(base_url="http://localhost:8321")

    models = client.models.list()

    # Select the first LLM and first embedding models
    model_id = next(m for m in models if m.model_type == "llm").identifier
    embedding_model_id = (
        em := next(m for m in models if m.model_type == "embedding")
    ).identifier
    embedding_dimension = em.metadata["embedding_dimension"]

    _ = client.vector_dbs.register(
        vector_db_id=vector_db_id,
        embedding_model=embedding_model_id,
        embedding_dimension=embedding_dimension,
        provider_id="faiss",
    )
    source = "https://www.paulgraham.com/greatwork.html"
    print("rag_tool> Ingesting document:", source)
    document = RAGDocument(
        document_id="document_1",
        content=source,
        mime_type="text/html",
        metadata={},
    )
    client.tool_runtime.rag_tool.insert(
        documents=[document],
        vector_db_id=vector_db_id,
        chunk_size_in_tokens=50,
    )
    agent = Agent(
        client,
        model=model_id,
        instructions="You are a helpful assistant",
        tools=[
            {
                "name": "builtin::rag/knowledge_search",
                "args": {"vector_db_ids": [vector_db_id]},
            }
        ],
    )

    prompt = "How do you do great work?"
    print("prompt>", prompt)

    response = agent.create_turn(
        messages=[{"role": "user", "content": prompt}],
        session_id=agent.create_session("rag_session"),
        stream=True,
    )

    for log in AgentEventLogger().log(response):
        log.print()

def demo_worldbuilder():
    """Demonstrate the WorldbuilderAgent class with example inputs"""

    # Initialize the WorldbuilderAgent
    worldbuilder = WorldbuilderAgent()

    # Example 1: Dystopian academy setting
    setting_desc1 = """A prestigious boarding academy built on a floating island above a post-apocalyptic wasteland.
    The academy trains gifted teenagers in elemental magic, but students are ranked in a strict hierarchy
    based on their magical abilities."""

    concept1 = """A story about a seemingly powerless student who discovers they have a rare and dangerous
    ability that could either save or destroy both the academy and the world below."""

    print("=== WORLDBUILDER AGENT DEMO ===\n")
    print("Example 1: Dystopian Magic Academy")
    print("-" * 40)

    try:
        result1 = worldbuilder.generate_setting(setting_desc1, concept1)
        print("Generated Setting Description:")
        print(result1)
        print("\n" + "="*50 + "\n")
    except Exception as e:
        print(f"Error generating worldbuilding: {e}")

    # Example 2: Urban fantasy setting
    setting_desc2 = """Modern-day Seattle where supernatural creatures live hidden among humans.
    A secret underground network of safe houses and magical shops exists beneath the city."""

    concept2 = """A teenage girl discovers she's half-fae and must navigate both high school drama
    and a brewing war between the supernatural factions while keeping her identity secret."""

    print("Example 2: Urban Fantasy")
    print("-" * 40)

    try:
        result2 = worldbuilder.generate_setting(setting_desc2, concept2)
        print("Generated Setting Description:")
        print(result2)
        print("\n" + "="*50 + "\n")
    except Exception as e:
        print(f"Error generating worldbuilding: {e}")

    # Example 3: Demonstrate multiple variations
    print("Example 3: Multiple Variations")
    print("-" * 40)

    try:
        variations = worldbuilder.generate_multiple_variations(
            setting_desc1, concept1, count=2, verbose=True
        )
        for i, variation in enumerate(variations, 1):
            print(f"Variation {i}:")
            print(variation)
            print("-" * 30)
    except Exception as e:
        print(f"Error generating variations: {e}")


def demo_character_agent():
    """Demonstrate the CharacterAgent class with example inputs"""

    # Initialize agents
    worldbuilder = WorldbuilderAgent()
    character_agent = CharacterAgent()

    # First, generate a setting
    setting_desc = """A prestigious boarding academy built on a floating island above a post-apocalyptic wasteland.
    The academy trains gifted teenagers in elemental magic, but students are ranked in a strict hierarchy
    based on their magical abilities."""

    concept = """A story about a seemingly powerless student who discovers they have a rare and dangerous
    ability that could either save or destroy both the academy and the world below."""

    print("=== CHARACTER AGENT DEMO ===\n")
    print("Generating setting first...")
    print("-" * 40)

    try:
        generated_setting = worldbuilder.generate_setting(setting_desc, concept, verbose=False)
        print("Generated Setting:")
        print(generated_setting[:200] + "...\n")

        # Generate different character types
        character_roles = ["protagonist", "antagonist", "protagonist's best friend", "mentor figure"]

        for role in character_roles:
            print(f"Creating {role.upper()}:")
            print("-" * 40)

            character_desc = character_agent.generate_character(
                concept, generated_setting, role, verbose=False
            )
            print(character_desc)
            print("\n" + "="*60 + "\n")

    except Exception as e:
        print(f"Error in character generation demo: {e}")


def demo_character_ensemble():
    """Demonstrate generating multiple characters at once"""

    character_agent = CharacterAgent()

    concept = """A teenage girl discovers she's half-fae and must navigate both high school drama
    and a brewing war between the supernatural factions while keeping her identity secret."""

    setting = """Modern-day Seattle where supernatural creatures live hidden among humans.
    A secret underground network of safe houses and magical shops exists beneath the city."""

    roles = ["protagonist", "antagonist", "love interest", "mentor"]

    print("=== CHARACTER ENSEMBLE DEMO ===\n")
    print("Generating character ensemble...")
    print("-" * 40)

    try:
        characters = character_agent.generate_character_ensemble(
            concept, setting, roles, verbose=True
        )

        for role, description in characters.items():
            print(f"\n{role.upper()}:")
            print("-" * 30)
            print(description[:300] + "...")

    except Exception as e:
        print(f"Error in ensemble generation: {e}")


def demo_full_story_pipeline():
    """Demonstrate all three agents working together to create a complete story foundation"""

    # Initialize all agents
    worldbuilder = WorldbuilderAgent()
    character_agent = CharacterAgent()
    outliner = OutlinerAgent()

    # Define the story concept
    concept = """A story about a seemingly powerless student at a magical academy who discovers
    they have a rare and dangerous ability that could either save or destroy both the academy
    and the world below."""

    initial_setting = """A prestigious boarding academy built on a floating island above a
    post-apocalyptic wasteland. The academy trains gifted teenagers in elemental magic,
    but students are ranked in a strict hierarchy based on their magical abilities."""

    print("=== FULL STORY PIPELINE DEMO ===\n")

    try:
        # Step 1: Generate detailed setting
        print("STEP 1: Generating detailed setting...")
        print("-" * 50)
        setting = worldbuilder.generate_setting(initial_setting, concept, verbose=False)
        print("Generated Setting:")
        print(setting)
        print("\n" + "="*70 + "\n")

        # Step 2: Generate character ensemble
        print("STEP 2: Generating character ensemble...")
        print("-" * 50)
        character_roles = ["protagonist", "antagonist", "mentor figure", "love interest"]
        characters = character_agent.generate_character_ensemble(
            concept, setting, character_roles, verbose=True
        )

        for role, description in characters.items():
            print(f"\n{role.upper()}:")
            print("-" * 30)
            print(description[:250] + "...")

        print("\n" + "="*70 + "\n")

        # Step 3: Generate 17-chapter outline
        print("STEP 3: Generating 17-chapter Hero's Journey outline...")
        print("-" * 50)
        outline = outliner.generate_outline(concept, setting, characters, verbose=True)
        print("\nGenerated Outline:")
        print(outline)

        print("\n" + "="*70 + "\n")
        print("STORY FOUNDATION COMPLETE!")
        print("You now have:")
        print("✓ Detailed world/setting description")
        print("✓ Complete character ensemble")
        print("✓ 17-chapter Hero's Journey outline")

    except Exception as e:
        print(f"Error in full story pipeline: {e}")


def demo_detailed_chapter():
    """Demonstrate detailed chapter breakdown functionality"""

    outliner = OutlinerAgent()

    # Simplified inputs for chapter detail demo
    concept = "A powerless student discovers dangerous magical abilities"
    setting = "A magical academy on a floating island above a wasteland"
    characters = {
        "protagonist": "A seemingly powerless 16-year-old student named Alex...",
        "mentor": "An enigmatic professor who sees potential in Alex...",
        "antagonist": "The academy's top student who views Alex as a threat..."
    }

    print("=== DETAILED CHAPTER BREAKDOWN DEMO ===\n")

    try:
        # Generate detailed breakdown for Chapter 1
        chapter_detail = outliner.generate_detailed_chapter_breakdown(
            concept, setting, characters, chapter_number=1, verbose=True
        )

        print("\nDetailed Chapter 1 Breakdown:")
        print("-" * 40)
        print(chapter_detail)

    except Exception as e:
        print(f"Error in chapter detail generation: {e}")


def demo_chapter_writing():
    """Demonstrate the ChapterAgent writing a complete chapter"""

    # Initialize chapter writer
    chapter_writer = ChapterAgent()

    setting = """Aethermoor Academy floats serenely above the Shattered Lands, a
    post-apocalyptic wasteland where magic once ran wild. The academy's crystal spires
    pierce the clouds, connected by bridges of solidified starlight. Students are ranked
    by their elemental affinities - Fire, Water, Earth, Air, and the rare Spirit magic."""

    characters = {
        "protagonist": """Kira Chen, 16, appears to be one of the 'Nulls' - students with no
        detectable magical ability. She has straight black hair, dark eyes, and tends to wear
        oversized academy robes to blend in. Quiet and observant, she loves ancient history
        and has a secret talent for sensing magical disturbances. Her goal is to prove she
        belongs at the academy despite her apparent lack of power.""",

        "mentor": """Professor Thorne, 45, teaches Magical Theory and secretly monitors students
        with unusual abilities. He has silver-streaked brown hair, kind green eyes, and always
        carries an ancient leather journal. He sees potential in Kira that others miss.""",

        "antagonist": """Marcus Blackwood, 17, is the academy's top Fire magic student and heir
        to a powerful magical family. Tall, blonde, and arrogant, he views Nulls as inferior
        and believes the academy should only accept the magically gifted."""
    }

    # Sample chapter outline (Chapter 1)
    chapter_outline = """
    CHAPTER 1: "The Null's Shadow"
    Hero's Journey Stage: Ordinary World

    Plot Summary: Kira attends her first day of Advanced Magical Theory, where she's the only
    Null in a class of gifted students. During a practical demonstration, something goes wrong
    with Marcus's fire spell, and Kira instinctively reaches out to help - causing a strange
    reaction that everyone notices but no one understands.

    Character Focus: Establish Kira's status as an outsider and hint at her hidden abilities.

    Story Progression: Introduce the academy's hierarchy and Kira's place at the bottom of it,
    while foreshadowing that she's more than she appears.
    """

    print("=== CHAPTER WRITING DEMO ===\n")

    try:
        print("Writing Chapter 1...")
        print("-" * 50)

        chapter_1 = chapter_writer.write_chapter(
            chapter_outline=chapter_outline,
            characters=characters,
            setting_description=setting,
            chapter_number=1,
            previous_chapter=None,
            verbose=True
        )

        print("\nCHAPTER 1: 'The Null's Shadow'")
        print("=" * 50)
        print(chapter_1)

        # Demonstrate writing a second chapter with previous chapter context
        print("\n" + "="*70 + "\n")
        print("Writing Chapter 2 with previous chapter context...")
        print("-" * 50)

        chapter_2_outline = """
        CHAPTER 2: "Whispers in the Library"
        Hero's Journey Stage: Call to Adventure

        Plot Summary: Kira researches what happened in class, discovering references to
        'Shadow Magic' in forbidden texts. Professor Thorne finds her and reveals he's
        been watching her, hinting that her abilities are both rare and dangerous.

        Character Focus: Kira begins to question her identity and Professor Thorne emerges
        as a potential mentor figure.

        Story Progression: The call to adventure begins as Kira learns she may not be
        powerless after all.
        """

        chapter_2 = chapter_writer.write_chapter(
            chapter_outline=chapter_2_outline,
            characters=characters,
            setting_description=setting,
            chapter_number=2,
            previous_chapter=chapter_1,  # Provide context from Chapter 1
            verbose=True
        )

        print("\nCHAPTER 2: 'Whispers in the Library'")
        print("=" * 50)
        print(chapter_2[:1000] + "...")  # Show first 1000 characters
        print("\n[Chapter continues...]")

    except Exception as e:
        print(f"Error in chapter writing demo: {e}")


def demo_pov_chapter_writing():
    """Demonstrate writing a chapter from a specific character's POV"""

    chapter_writer = ChapterAgent()

    # Simplified story elements for POV demo
    characters = {
        "protagonist": "Kira Chen, 16, a seemingly powerless student who secretly has rare Shadow Magic abilities...",
        "antagonist": "Marcus Blackwood, 17, arrogant Fire magic prodigy who looks down on Nulls..."
    }

    setting = "Aethermoor Academy, a magical school floating above a post-apocalyptic wasteland..."

    chapter_outline = """
    CHAPTER 3: "The Fire Prince's Doubt"

    Plot Summary: Marcus reflects on the strange incident with Kira in class. Despite his
    arrogance, he's troubled by what he witnessed and begins to question whether Nulls
    might be more than they appear.

    Character Focus: Show Marcus's internal conflict and hint at his deeper insecurities
    beneath his confident exterior.
    """

    print("=== POV CHAPTER WRITING DEMO ===\n")

    try:
        print("Writing Chapter 3 from Marcus's POV...")
        print("-" * 50)

        marcus_chapter = chapter_writer.write_chapter_with_specific_pov(
            chapter_outline=chapter_outline,
            characters=characters,
            setting_description=setting,
            chapter_number=3,
            pov_character="antagonist",
            verbose=True
        )

        print("\nCHAPTER 3: 'The Fire Prince's Doubt' (Marcus's POV)")
        print("=" * 60)
        print(marcus_chapter[:800] + "...")  # Show first 800 characters
        print("\n[Chapter continues...]")

    except Exception as e:
        print(f"Error in POV chapter writing demo: {e}")


if __name__ == "__main__":
    # Uncomment the line below to run the original RAG demo
    # main()

    # Run individual agent demos
    # demo_worldbuilder()
    # demo_character_agent()
    # demo_character_ensemble()

    # Run the full story pipeline demo
    # demo_full_story_pipeline()

    # Run detailed chapter demo
    # demo_detailed_chapter()

    # Run chapter writing demos
    demo_chapter_writing()

    # Uncomment to run POV chapter demo
    # demo_pov_chapter_writing()
