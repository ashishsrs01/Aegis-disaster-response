from src.core.environment import CityGraph
from src.navigation.pathfinder import Pathfinder
from src.perception.hazard_tracker import HazardTracker
from src.reasoning.triage import TriageEngine
from src.core.victim import Victim

def main():
    # 1. Setup
    city = CityGraph(width=7, height=7)
    router = Pathfinder(city)
    triage = TriageEngine()
    
    # 2. Spawn two victims
    # Victim 1 is at (6,6), unconscious (Serious!)
    v1 = Victim(id=1, location=(6, 6), vitals={'breathing': True, 'conscious': False})
    # Victim 2 is at (0,6), conscious (Less serious)
    v2 = Victim(id=2, location=(0, 6), vitals={'breathing': True, 'conscious': True})
    
    # 3. AI Reasoning: The Triage Phase
    for v in [v1, v2]:
        v.priority = triage.evaluate(v.vitals)
        print(f"Inferred: {v}")

    # 4. Decision Making: Who do we save first?
    # Logic: Pick RED over YELLOW
    targets = sorted([v1, v2], key=lambda x: (x.priority != "RED"))
    primary_target = targets[0]
    
    print(f"\nAI DECISION: Heading to {primary_target} first because priority is {primary_target.priority}")

    # 5. Route to the high-priority victim
    path, time = router.a_star((0,0), primary_target.location)
    city.visualize(path=path)

if __name__ == "__main__":
    main()