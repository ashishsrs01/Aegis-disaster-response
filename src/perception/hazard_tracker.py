from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

class HazardTracker:
    """
    Uses a Bayesian Network to infer the probability of a hazard (Flood)
    given noisy sensor data and environmental conditions.
    """
    
    def __init__(self):
        
        # 1. Define the network structure (Edges)
        # Rain causes Flood -> Flood causes Sensor Reading
        self.model = DiscreteBayesianNetwork([('Rain', 'Flood'), ('Flood', 'Sensor')])

        # 2. Define the Conditional Probability Tables (CPTs)
        
        # P(Rain): 20% chance it's a rainy day
        cpd_rain = TabularCPD(variable='Rain', variable_card=2, values=[[0.8], [0.2]], 
                              state_names={'Rain': ['No', 'Yes']})

        # P(Flood | Rain): If No Rain, 5% flood. If Yes Rain, 70% flood.
        cpd_flood = TabularCPD(
            variable='Flood', variable_card=2,
            values=[[0.95, 0.3],   # No Flood
                    [0.05, 0.7]],  # Flood
            evidence=['Rain'], evidence_card=[2],
            state_names={'Flood': ['No', 'Yes'], 'Rain': ['No', 'Yes']}
        )

        # P(Sensor | Flood): Reliability of the drone
        # If Flood, drone is 90% accurate. If No Flood, 10% false alarm rate.
        cpd_sensor = TabularCPD(
            variable='Sensor', variable_card=2,
            values=[[0.9, 0.1],   # Sensor says "Clear"
                    [0.1, 0.9]],  # Sensor says "Flooded"
            evidence=['Flood'], evidence_card=[2],
            state_names={'Sensor': ['No', 'Yes'], 'Flood': ['No', 'Yes']}
        )

        
        # Add CPTs to the model
        self.model.add_cpds(cpd_rain, cpd_flood, cpd_sensor)
        
        # Validate the model (sums to 1.0, etc.)
        assert self.model.check_model()
        
        # Initialize the Inference engine (Reasoning engine)
        self.inference = VariableElimination(self.model)

    
    def infer_flood_probability(self, drone_observation: str, is_raining: str = 'Yes') -> float:
        """
        Calculates P(Flood | Sensor=observation, Rain=is_raining)
        """
        result = self.inference.query(
            variables=['Flood'], 
            evidence={'Sensor': drone_observation, 'Rain': is_raining}
        )
        # Return the probability that Flood is 'Yes'
        return result.values[1]


# --- Execution Block ---
if __name__ == "__main__":
    tracker = HazardTracker()
    
    # SCENARIO: It is raining, and the drone says "I see a flood!"
    prob = tracker.infer_flood_probability(drone_observation='Yes', is_raining='Yes')
    
    print(f"Chance of actual flood given Rain=Yes and Sensor=Yes: {prob:.2%}")
    
    # SCENARIO: It's a sunny day (No Rain), but the drone says "I see a flood!" 
    # (Checking for a false positive)
    prob_dry = tracker.infer_flood_probability(drone_observation='Yes', is_raining='No')
    print(f"Chance of actual flood given Rain=No and Sensor=Yes: {prob_dry:.2%}")