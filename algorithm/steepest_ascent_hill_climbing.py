import itertools
import time
import copy
import matplotlib.pyplot as plt
from cube.cube import MagicCube

class SteepestAscentHillClimbing:
    def __init__(self, magic_cube):
        self.magic_cube = magic_cube
        self.iterations = 0
        self.start_time = None
        self.end_time = None
        self.objective_values = []
        self.initial_cube = copy.deepcopy(self.magic_cube.cube)
        self.final_cube = None

    def objective_function(self):
        """Returns the negative of the current objective for hill climbing purposes."""
        return -self.magic_cube.objective_function()

    def find_best_neighbor(self):
        """Find the best neighboring configuration."""
        indices = [(i, j, k) for i in range(self.magic_cube.size) for j in range(self.magic_cube.size) for k in range(self.magic_cube.size)]
        best_neighbor = None
        best_value = float('-inf')

        for pos1, pos2 in itertools.combinations(indices, 2):
            self.magic_cube.swap(pos1, pos2)
            neighbor_value = self.objective_function()
            if neighbor_value > best_value:
                best_neighbor = (pos1, pos2)
                best_value = neighbor_value
            self.magic_cube.swap(pos1, pos2)  # Revert to original state

        return best_neighbor, best_value

    def run(self):
        """Run the Steepest Ascent Hill Climbing algorithm."""
        self.start_time = time.time()
        current_value = self.objective_function()
        self.objective_values.append(-current_value)  # Store initial objective value

        while True:
            best_neighbor, best_value = self.find_best_neighbor()
            self.iterations += 1

            # Track objective function over iterations
            self.objective_values.append(-best_value)
            print(f"Iteration {self.iterations}: Objective = {-current_value}, Time = {time.time() - self.start_time:.4f} seconds")

            if best_neighbor is None or best_value <= current_value:
                # Stop if no better neighbor is found
                break

            # Apply the best swap permanently
            pos1, pos2 = best_neighbor
            self.magic_cube.swap(pos1, pos2)
            current_value = best_value

        self.end_time = time.time()
        # Capture the final state of the cube
        self.final_cube = copy.deepcopy(self.magic_cube.cube)

    def report(self):
        """Display the results and plot the progress."""
        print("\nExperiment Report:")
        print(f"Initial State: {self.initial_cube}")
        print(f"Final State: {self.final_cube}")
        print(f"Final Objective Value: {self.objective_values[-1]}")
        print(f"Total Iterations: {self.iterations}")
        print(f"Duration: {self.end_time - self.start_time:.4f} seconds")

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot(self.objective_values, label='Objective Function')
        plt.xlabel('Iterations')
        plt.ylabel('Objective Function Value')
        plt.title('Objective Function Value over Iterations')
        plt.legend()
        plt.grid(True)
        plt.show()
        
# Example usage
if __name__ == "__main__":
    cube = MagicCube(size=5)
    hill_climber = SteepestAscentHillClimbing(cube)
    hill_climber.run()
    hill_climber.report()
