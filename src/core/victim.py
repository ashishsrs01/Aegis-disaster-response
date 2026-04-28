from typing import Tuple, Dict

class Victim:
    def __init__(self, id: int, location: Tuple[int, int], vitals: Dict[str, bool]):
        self.id = id
        self.location = location
        self.vitals = vitals
        self.priority = "UNKNOWN"

    def __repr__(self):
        return f"Victim_{self.id}(Loc: {self.location}, Priority: {self.priority})"