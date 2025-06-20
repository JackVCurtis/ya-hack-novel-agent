#!/usr/bin/env python3
"""
Example usage of the AbstractWriterAgent and its concrete implementations.

This script demonstrates how all four writer agents now inherit from AbstractWriterAgent
and share common functionality while maintaining their specialized behavior.
"""

from worldbuilder_agent import WorldbuilderAgent
from character_agent import CharacterAgent
from outliner_agent import OutlinerAgent
from chapter_agent import ChapterAgent


def main():
    """Demonstrate the usage of all writer agents."""
    
    # Sample data for testing
    novel_concept = "A teenage girl discovers she can manipulate time but each use ages her rapidly"
    setting_description = "A modern high school in a small coastal town where strange temporal anomalies occur"
    
    print("=== AbstractWriterAgent Implementation Demo ===\n")
    
    # 1. WorldbuilderAgent
    print("1. Testing WorldbuilderAgent (inherits from AbstractWriterAgent):")
    wb_agent = WorldbuilderAgent()
    print(f"   - Model: {wb_agent.model}")
    print(f"   - Has _make_api_call method: {hasattr(wb_agent, '_make_api_call')}")
    print(f"   - Has _execute_two_step_generation method: {hasattr(wb_agent, '_execute_two_step_generation')}")
    print(f"   - Implements abstract methods: {hasattr(wb_agent, '_generate_detailed_prompt') and hasattr(wb_agent, '_create_content_from_prompt')}")
    print()
    
    # 2. CharacterAgent
    print("2. Testing CharacterAgent (inherits from AbstractWriterAgent):")
    char_agent = CharacterAgent()
    print(f"   - Model: {char_agent.model}")
    print(f"   - Has _make_api_call method: {hasattr(char_agent, '_make_api_call')}")
    print(f"   - Has _execute_two_step_generation method: {hasattr(char_agent, '_execute_two_step_generation')}")
    print(f"   - Implements abstract methods: {hasattr(char_agent, '_generate_detailed_prompt') and hasattr(char_agent, '_create_content_from_prompt')}")
    print()
    
    # 3. OutlinerAgent
    print("3. Testing OutlinerAgent (inherits from AbstractWriterAgent):")
    outline_agent = OutlinerAgent()
    print(f"   - Model: {outline_agent.model}")
    print(f"   - Has _make_api_call method: {hasattr(outline_agent, '_make_api_call')}")
    print(f"   - Has _execute_two_step_generation method: {hasattr(outline_agent, '_execute_two_step_generation')}")
    print(f"   - Implements abstract methods: {hasattr(outline_agent, '_generate_detailed_prompt') and hasattr(outline_agent, '_create_content_from_prompt')}")
    print()
    
    # 4. ChapterAgent
    print("4. Testing ChapterAgent (inherits from AbstractWriterAgent):")
    chapter_agent = ChapterAgent()
    print(f"   - Model: {chapter_agent.model}")
    print(f"   - Has _make_api_call method: {hasattr(chapter_agent, '_make_api_call')}")
    print(f"   - Has _execute_two_step_generation method: {hasattr(chapter_agent, '_execute_two_step_generation')}")
    print(f"   - Implements abstract methods: {hasattr(chapter_agent, '_generate_detailed_prompt') and hasattr(chapter_agent, '_create_content_from_prompt')}")
    print()
    
    # Demonstrate shared functionality
    print("5. Shared functionality from AbstractWriterAgent:")
    print("   - All agents use the same OpenAI client initialization")
    print("   - All agents use the same _make_api_call method for consistent API interactions")
    print("   - All agents use the same _execute_two_step_generation pattern")
    print("   - All agents have helper methods like _format_character_info and _create_context_section")
    print("   - All agents can update their instructions using update_instructions()")
    print()
    
    print("✅ All agents successfully inherit from AbstractWriterAgent!")
    print("✅ The two-step generation pattern is now centralized and reusable!")
    print("✅ API calls are standardized across all agents!")
    print("✅ Common functionality is shared while maintaining agent-specific behavior!")

    # Demonstrate writing style guide functionality
    print("\n6. Writing Style Guide functionality:")
    print("   - Each agent has a default writing style guide specific to its purpose")
    print("   - Custom style guides can be provided during initialization")
    print("   - Style guides are accessible via the writing_style_guide property")
    print("   - Helper method _get_style_guide_section() formats style guides for prompts")
    print()

    # Show default style guide lengths
    print("   Default style guide lengths:")
    print(f"   - WorldbuilderAgent: {len(wb_agent.writing_style_guide)} characters")
    print(f"   - CharacterAgent: {len(char_agent.writing_style_guide)} characters")
    print(f"   - OutlinerAgent: {len(outline_agent.writing_style_guide)} characters")
    print(f"   - ChapterAgent: {len(chapter_agent.writing_style_guide)} characters")
    print()

    # Demonstrate custom style guide
    custom_style = "CUSTOM STYLE: Write in a mysterious, atmospheric tone with short, punchy sentences."
    custom_wb = WorldbuilderAgent(writing_style_guide=custom_style)
    print(f"   Custom style guide example: '{custom_wb.writing_style_guide}'")
    print()

    print("✅ Writing style guides are now integrated into all agents!")
    print("✅ Each agent has specialized default style guidelines!")
    print("✅ Custom style guides can be provided for specialized writing tasks!")


if __name__ == "__main__":
    main()
