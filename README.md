# YA Novel Generator

A comprehensive AI-powered tool for creating young adult fiction, featuring world-building, character creation, story outlining, and chapter writing capabilities.

## Features

- **Story Concept & Setting**: Define your core story idea and initial setting
- **World Building**: Generate detailed, immersive setting descriptions
- **Character Creation**: Create comprehensive character profiles with personalities, goals, and flaws
- **Story Outline**: Generate 17-chapter outlines following the Hero's Journey structure
- **Chapter Writing**: Write complete chapters with proper structure (sensory openings, rising action, falling action)

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure you have LlamaStack running locally on `http://localhost:8321`

## Usage

### Web Interface (Streamlit)

Run the Streamlit web application:
```bash
streamlit run streamlit_app.py
```

This will open a web interface where you can:
1. Enter your story concept and setting
2. Generate detailed world-building
3. Create character profiles
4. Generate a 17-chapter outline
5. Write individual chapters

### Command Line Interface

You can also use the agents directly in Python:

```python
from worldbuilder_agent import WorldbuilderAgent
from character_agent import CharacterAgent
from outliner_agent import OutlinerAgent
from chapter_agent import ChapterAgent

# Initialize agents
worldbuilder = WorldbuilderAgent()
character_agent = CharacterAgent()
outliner = OutlinerAgent()
chapter_writer = ChapterAgent()

# Generate story elements
setting = worldbuilder.generate_setting(initial_setting, concept)
characters = character_agent.generate_character_ensemble(concept, setting, roles)
outline = outliner.generate_outline(concept, setting, characters)
chapter = chapter_writer.write_chapter(chapter_outline, characters, setting, 1)
```

## Project Structure

- `streamlit_app.py` - Web interface for the novel generator
- `worldbuilder_agent.py` - Agent for creating detailed setting descriptions
- `character_agent.py` - Agent for generating character profiles
- `outliner_agent.py` - Agent for creating 17-chapter Hero's Journey outlines
- `chapter_agent.py` - Agent for writing complete chapters
- `main.py` - Command-line demos and examples

## Requirements

- Python 3.8+
- LlamaStack server running locally
- Streamlit for web interface
- All dependencies listed in `requirements.txt`

## Hero's Journey Structure

The outliner follows the classic Hero's Journey structure:

**Part I - Departure (Chapters 1-6)**
- Ordinary World
- Call to Adventure
- Refusal of the Call
- Meeting with the Mentor
- Crossing the First Threshold
- The Belly of the Whale

**Part II - Initiation (Chapters 7-13)**
- The Road of Trials
- Tests, Allies, and Enemies
- Approach to the Inmost Cave
- The Ordeal
- Reward
- The Meeting with the Goddess
- Atonement with the Father

**Part III - Return (Chapters 14-17)**
- Refusal of the Return
- The Magic Flight
- Rescue from Without
- The Crossing of the Return Threshold
- Master of the Two Worlds
- Freedom to Live