# set_simulator.py
from typing import List
from itertools import combinations
import random
from class_card import Card
from class_setalgorithms import SetAlgorithms

"""
Welcome to the Set Simulator file. 
This file contains statistical tools  for analyzing SET game probabilities

The simulator analyses how set probability changes with different table sizes.

The simulator is mostly used for the report,
"""
class SetSimulator:
    @staticmethod
    def simulate_no_set_probability(sample_sizes: List[int], num_simulations: int = 10000) -> dict:
        # Generate all possible cards once
        all_cards = SetAlgorithms.generate_all_cards()
        results = {}
        
        for size in sample_sizes:
            no_set_count = 0
            
            for _ in range(num_simulations):
                # Random sample without replacement
                sample = random.sample(all_cards, size)
                
                # Check if this sample has no sets
                if SetAlgorithms.is_cap_set(sample):
                    no_set_count += 1
            
            probability = no_set_count / num_simulations
            results[size] = probability
            print(f"Sample size {size}: No-set probability = {probability:.15f}")
            
        return results

if __name__ == "__main__":
    # Example usage
    simulator = SetSimulator()
    results = simulator.simulate_no_set_probability(
        sample_sizes=[12, 15, 18, 21],
        num_simulations=10000  # Increase for more accuracy
    )