from typing import Dict

class Observation(Dict[str, any]):
    def __init__(self, player=0) -> None:
        super().__init__()
        self.player = player