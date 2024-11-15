import random
import math
import copy
import matplotlib.pyplot as plt
from datetime import datetime
from cube.cube import MagicCube

class SimulatedAnnealing:
    def __init__(self, magic_cube, initial_temp, cooling_rate):
        self.magic_cube = magic_cube
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.iterations = 0
        self.start_time = None
        self.end_time = None
        self.objective_values = []
        self.acceptance_probabilities = []  
        self.local_optima_stuck_count = 0 
        self.initial_cube = copy.deepcopy(self.magic_cube.data)
        self.final_cube = None

    def find_neighbor(self):
        pos1 = (random.randint(0, self.magic_cube.size - 1),
                random.randint(0, self.magic_cube.size - 1),
                random.randint(0, self.magic_cube.size - 1))
        
        pos2 = (random.randint(0, self.magic_cube.size - 1),
                random.randint(0, self.magic_cube.size - 1),
                random.randint(0, self.magic_cube.size - 1))
        
        # Ensure pos1 and pos2 are different
        while pos1 == pos2:
            pos2 = (random.randint(0, self.magic_cube.size - 1),
                    random.randint(0, self.magic_cube.size - 1),
                    random.randint(0, self.magic_cube.size - 1))
        
        neighbor_cube = copy.deepcopy(self.magic_cube)
        neighbor_cube.swap(pos1, pos2)

        return neighbor_cube

    def run(self):
        current_temp = self.initial_temp
        current_objective = self.magic_cube.objective_function()
        best_objective = current_objective
        best_cube = copy.deepcopy(self.magic_cube.data)
        self.start_time = datetime.now()

        while True:
            # Find neighbor
            neighbor_cube = self.find_neighbor()
            new_objective = neighbor_cube.objective_function()
            delta_e = new_objective - current_objective

            # Compute acceptance probability
            if delta_e < 0:
                acceptance_prob = 1.0
            else:
                acceptance_prob = math.exp(-delta_e / current_temp)
            
            # Accept the neighbor based on the probability
            if delta_e < 0 or random.uniform(0, 1) < acceptance_prob:
                self.magic_cube = neighbor_cube
                current_objective = new_objective

                if current_objective < best_objective:
                    best_objective = current_objective
                    best_cube = copy.deepcopy(self.magic_cube.data)
            else:
                # Increment the counter if we are "stuck" in a local optimum
                self.local_optima_stuck_count += 1
            
            # Store values
            self.objective_values.append(current_objective)
            self.acceptance_probabilities.append(acceptance_prob)
            self.iterations += 1

            print(f"Iteration {self.iterations}: Temp = {current_temp:.4f}, Objective = {current_objective}, Acceptance Probability = {acceptance_prob:.4f}")

            # Update temperature
            current_temp *= self.cooling_rate

            # Termination condition
            if current_temp < 1e-10 or best_objective == 0:
                break

        # Final state
        self.final_cube = best_cube
        self.end_time = datetime.now()
        
    def report(self):
        # Execution time
        duration = (self.end_time - self.start_time).total_seconds()

        print("=== Simulated Annealing Report ===")
        print(f"Initial Objective Value: {self.objective_values[0]}")
        print(f"Final Objective Value: {self.objective_values[-1]}")
        print(f"Total Iterations: {self.iterations}")
        print(f"Execution Time: {duration:.4f} seconds")
        print(f"Frequency of getting stuck in local optima: {self.local_optima_stuck_count}")
        print("\nInitial State:")
        print((self.initial_cube))
        print("\nFinal State:")
        print((self.final_cube))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Plot changes in objective function and acceptance probability over iterations
        plt.figure(figsize=(12, 5))

        # Plot objective function values over iterations
        plt.subplot(1, 2, 1)
        plt.plot(self.objective_values, label='Objective Value')
        plt.xlabel("Iterations")
        plt.ylabel("Objective Function Value")
        plt.title("Objective Function vs. Iterations")
        plt.legend()

        # Plot acceptance probabilities over iterations
        plt.subplot(1, 2, 2)
        plt.plot(self.acceptance_probabilities, label='Acceptance Probability')
        plt.xlabel("Iterations")
        plt.ylabel("Acceptance Probability")
        plt.title("Acceptance Probability vs. Iterations")
        plt.legend()
        plt.tight_layout()
        
        # Save the plot
        plt.savefig(f'src/data/simulated_annealing_plot_{timestamp}.png', format='png')
        plt.show()
        

if __name__ == "__main__":
    n = 5
    initial_temp = 1000
    cooling_rate = 0.95

    magic_cube = MagicCube(n)
    sa = SimulatedAnnealing(magic_cube, initial_temp, cooling_rate)

    sa.run()
    sa.report()
