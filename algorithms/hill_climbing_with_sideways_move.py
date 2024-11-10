import datetime
import itertools
import time
import copy
import matplotlib.pyplot as plt
from cube.cube import MagicCube

class HillClimbingWithSidewaysMove:
    def __init__(self, magic_cube, max_sideways):
        self.magic_cube = magic_cube
        self.max_sideways = max_sideways
        self.iterations = 0
        self.sideways_moves = 0
        self.start_time = None
        self.end_time = None
        self.objective_values = []
        self.initial_cube = copy.deepcopy(self.magic_cube.data)
        self.final_cube = None

    def objective_function(self, cube_data):
        original_data = self.magic_cube.data
        self.magic_cube.data = cube_data
        objective_value = self.magic_cube.objective_function()
        self.magic_cube.data = original_data
        return -objective_value

    def find_best_neighbor(self):
        indices = [(i, j, k) for i in range(self.magic_cube.size) for j in range(self.magic_cube.size) for k in range(self.magic_cube.size)]
        best_neighbor = None
        best_value = float('-inf')
        current_data = copy.deepcopy(self.magic_cube.data)

        for pos1, pos2 in itertools.combinations(indices, 2):
            temp_data = copy.deepcopy(current_data)
            x1, y1, z1 = pos1
            x2, y2, z2 = pos2
            temp_data[x1][y1][z1], temp_data[x2][y2][z2] = temp_data[x2][y2][z2], temp_data[x1][y1][z1]

            neighbor_value = self.objective_function(temp_data)
            if neighbor_value > best_value:
                best_neighbor = (pos1, pos2)
                best_value = neighbor_value

        return best_neighbor, best_value

    def run(self):
        self.start_time = time.time()
        current_value = self.objective_function(self.magic_cube.data)
        self.objective_values.append(-current_value)

        while True:
            best_neighbor, best_value = self.find_best_neighbor()
            self.iterations += 1

            # Laporan tiap iterasi
            elapsed_time = time.time() - self.start_time
            print(f"Iteration {self.iterations}: Objective = {-best_value}, Sideways Moves = {self.sideways_moves}, Time Elapsed = {elapsed_time:.4f} seconds")

            if best_neighbor is None:
                break

            if best_value > current_value:
                self.sideways_moves = 0
            elif best_value == current_value and self.sideways_moves < self.max_sideways:
                self.sideways_moves += 1
            else:
                break

            pos1, pos2 = best_neighbor
            self.magic_cube.swap(pos1, pos2)
            current_value = best_value
            self.objective_values.append(-best_value)

        self.end_time = time.time()
        self.final_cube = copy.deepcopy(self.magic_cube.data)
    
    def report(self):
        print("\nExperiment Report:")
        print(f"Initial State: ")
        print(self._format_cube(self.initial_cube))
        print(f"Final State: ")
        print(self._format_cube(self.final_cube))
        print(f"Final Objective Value: {self.objective_values[-1]}")
        print(f"Total Iterations: {self.iterations}")
        print(f"Total Sideways Moves: {self.sideways_moves}")
        print(f"Duration: {self.end_time - self.start_time:.4f} seconds")
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
        plt.savefig(f'./data/hill_climbing_with_sideways_move_plot_{timestamp}.png', format='png')
        plt.show()
        
if __name__ == "__main__":
    cube = MagicCube(size=5)
    hill_climber = HillClimbingWithSidewaysMove(cube, max_sideways=100)
    hill_climber.run()
    hill_climber.report()