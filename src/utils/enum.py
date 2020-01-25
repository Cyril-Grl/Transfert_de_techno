from enum import Enum

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    BUCKET = 1
    LION = 2
    SHEEP = 3
    WIN = 4
    LOSE = 5