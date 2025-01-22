# PacmanWars
**Do you think you have what it takes to beat all the other players ?**

PacmanWars is a game where multiple bots compete in a grid-based environment to collect food and survive. If you want to fight in this game, you can fork the repo and submit the code of your own bot. 

![game-snapshot](assets/game-snapshot.png)

## How to submit your custom bots

To create a custom bot, follow these steps:

1. Create a new Python file in the [bots](http://_vscodecontentref_/8) directory with any valid name.
2. Define a new class that inherits from the `Bot` class (Keep the class name as your github username).
3. Implement the **move** method.
4. See the reference bots **basic_bot1.py** and **basic_bot2.py**.
5. Use this reference code below to write your new bot.

Example:
```python
from bots.bot import Bot

class CustomBot(Bot):
    def __init__(self, id: int, start_x: int, start_y: int, minimap: list, map_length: int, map_breadth: int):
        super().__init__(id, start_x, start_y, minimap, map_length, map_breadth)

    def move(self, current_x, current_y, minimap):
        self.update_state(current_x, current_y, minimap)
        # Implement your bot's strategy here
        return direction
```

## Features

- Randomly generated game map with obstacles and food
- Multiple bots with unique behaviors coded by different people
- Real-time scoreboard
- Customizable bot strategies

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/xzaviourr/PacmanWars.git
    cd PacmanWars
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv pacmanwars-env
    pacmanwars-env\Scripts\activate  # On Windows
    source pacmanwars-env/bin/activate  # On macOS/Linux
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the game:
    ```sh
    python main.py
    ```

2. Watch the bots compete and collect food. The scoreboard on the right side of the screen shows the current standings.

## Project Structure

- [main.py](http://_vscodecontentref_/1): The main entry point for the game.
- [constants.py](http://_vscodecontentref_/2): Contains game constants and configurations.
- [map_generator.py](http://_vscodecontentref_/3): Generates the game map.
- [food_generator.py](http://_vscodecontentref_/4): Generates food on the map.
- [bot_operations.py](http://_vscodecontentref_/5): Contains functions for bot movements and interactions.
- [bots](http://_vscodecontentref_/6): Directory containing bot implementations.
- [readme.md](http://_vscodecontentref_/7): This file.