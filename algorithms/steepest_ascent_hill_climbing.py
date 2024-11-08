import datetime
import itertools
import time
import copy
import matplotlib.pyplot as plt
from cube.cube import MagicCube

# The Steepest Ascent Hill Climbing class
class SteepestAscentHillClimbing:
    def __init__(self, magic_cube):
        self.magic_cube = magic_cube
        self.iterations = 0
        self.start_time = None
        self.end_time = None
        self.objective_values = []
        self.initial_cube = copy.deepcopy(self.magic_cube.data)
        self.final_cube = None

    def objective_function(self, cube_data):
        """Calculate the objective function value for a given cube state."""
        original_data = self.magic_cube.data
        self.magic_cube.data = cube_data
        objective_value = self.magic_cube.objective_function()
        self.magic_cube.data = original_data  # Restore original data
        return -objective_value  # Return negative for hill climbing

    def find_best_neighbor(self):
        """Find the best neighboring configuration by checking all possible swaps."""
        indices = [(i, j, k) for i in range(self.magic_cube.size) for j in range(self.magic_cube.size) for k in range(self.magic_cube.size)]
        best_neighbor = None
        best_value = float('-inf')
        current_data = copy.deepcopy(self.magic_cube.data)  # Copy the current cube data for evaluation

        for pos1, pos2 in itertools.combinations(indices, 2):
            # Create a deep copy of the cube data to test the swap
            temp_data = copy.deepcopy(current_data)
            # Perform the swap on the temporary data
            x1, y1, z1 = pos1
            x2, y2, z2 = pos2
            temp_data[x1][y1][z1], temp_data[x2][y2][z2] = temp_data[x2][y2][z2], temp_data[x1][y1][z1]

            # Evaluate this neighbor
            neighbor_value = self.objective_function(temp_data)
            if neighbor_value > best_value:
                best_neighbor = (pos1, pos2)
                best_value = neighbor_value

        return best_neighbor, best_value

    def run(self):
        """Run the Steepest Ascent Hill Climbing algorithm with search log display."""
        self.start_time = time.time()
        current_value = self.objective_function(self.magic_cube.data)
        self.objective_values.append(-current_value)  # Store initial objective value

        while True:
            best_neighbor, best_value = self.find_best_neighbor()
            self.iterations += 1

            # Track objective function over iterations
            self.objective_values.append(-best_value)

            # Calculate elapsed time for this iteration
            elapsed_time = time.time() - self.start_time

            # Log iteration details to the console
            print(f"Iteration {self.iterations}: Objective = {-best_value}, Time = {elapsed_time:.4f} seconds")

            # Stop if no better neighbor is found
            if best_neighbor is None or best_value <= current_value:
                break

            # Apply the best swap to the actual cube
            pos1, pos2 = best_neighbor
            self.magic_cube.swap(pos1, pos2)
            current_value = best_value

        self.end_time = time.time()
        # Capture the final state of the cube
        self.final_cube = copy.deepcopy(self.magic_cube.data)

    def report(self):
        """Display the results and plot the progress."""
        print("\nExperiment Report:")
        print(f"Initial State: {self.initial_cube}")
        print(f"Final State: {self.final_cube}")
        print(f"Final Objective Value: {self.objective_values[-1]}")
        print(f"Total Iterations: {self.iterations}")
        print(f"Duration: {self.end_time - self.start_time:.4f} seconds")

        # Generate the current timestamp in the desired format (e.g., YYYYMMDD_HHMMSS)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot(self.objective_values, label='Objective Function')
        plt.xlabel('Iterations')
        plt.ylabel('Objective Function Value')
        plt.title('Objective Function Value over Iterations')
        plt.legend()
        plt.grid(True)

        # Save the plot with a timestamp in the filename
        plt.savefig(f'./data/objective_function_plot_{timestamp}.png', format='png')

        # Display the plot
        plt.show()


if __name__ == "__main__":
    cube = MagicCube(size=5)
    hill_climber = SteepestAscentHillClimbing(cube)
    hill_climber.run()
    hill_climber.report()