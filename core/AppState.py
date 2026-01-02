from enum import Enum, auto

class AppState(Enum):
    RUNNING = auto()
    PAUSED = auto()
    STOPPED = auto()