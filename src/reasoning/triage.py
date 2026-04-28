from typing import Dict

class TriageEngine:
    """
    Knowledge Representation & Reasoning module.
    Uses propositional logic to categorize victims based on medical signs.
    """
    
    def __init__(self):
        # In a high-grade system, these rules could be loaded from a JSON file
        # to allow doctors to update them without touching the code.
        pass

    def evaluate(self, vitals: Dict[str, bool]) -> str:
        """
        An inference engine that applies START triage rules.
        Inputs: vitals like {'breathing': True, 'pulse': True, 'conscious': False}
        Returns: 'RED', 'YELLOW', 'GREEN', or 'BLACK'
        """
        # Rule 1: If not breathing, they are Black tag (Deceased)
        if not vitals.get('breathing', False):
            return "BLACK"

        # Rule 2: If breathing but unconscious, they are Red tag (Immediate)
        if not vitals.get('conscious', True):
            return "RED"

        # Rule 3: If breathing and conscious but no pulse (Shock), they are Red tag
        if not vitals.get('pulse', True):
            return "RED"

        # Rule 4: If breathing, conscious, and has pulse, they are Yellow (Delayed)
        # (Assuming they need an ambulance but aren't dying this second)
        return "YELLOW"

# --- Execution Block ---
if __name__ == "__main__":
    engine = TriageEngine()
    
    # Test Case: A victim who is breathing but unconscious
    victim_a = {'breathing': True, 'pulse': True, 'conscious': False}
    # Test Case: A victim who is breathing and conscious
    victim_b = {'breathing': True, 'pulse': True, 'conscious': True}
    
    print(f"Victim A Priority: {engine.evaluate(victim_a)}") # Expected: RED
    print(f"Victim B Priority: {engine.evaluate(victim_b)}") # Expected: YELLOW