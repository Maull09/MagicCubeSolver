import random
import time
from cube.cube import MagicCube
from algorithm.steepest_ascent_hill_climbing import SteepestAscentHillClimbing

def random_restart_hill_climbing(restart_limit=5):
    """Random Restart Hill Climbing to find the global optimum for the Magic Cube."""
    best_cube = None
    best_value = float('-inf')
    for restart in range(restart_limit):
        print(f"\nRestart {restart + 1}")
        cube = MagicCube(size=5)
        SteepestAscentHillClimbing(cube)
        local_optimum_value = -cube.objective_function()
        print(f"Local Optimum Objective: {-local_optimum_value}")
        if local_optimum_value > best_value:
            best_value = local_optimum_value
            best_cube = cube
    return best_cube

# Example usage
if __name__ == "__main__":
    final_cube = random_restart_hill_climbing()
    print("Best Objective Found:", -final_cube.objective_function())