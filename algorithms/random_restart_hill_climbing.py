import copy
import datetime
import time
from matplotlib import pyplot as plt
from algorithms.steepest_ascent_hill_climbing import SteepestAscentHillClimbing
from cube.cube import MagicCube

class RandomRestartHillClimbing:
    def __init__(self, magic_cube, max_restarts=5):
        self.magic_cube = magic_cube
        self.max_restarts = max_restarts
        self.best_cube_state = None
        self.best_objective_value = float('inf')
        self.all_objective_values_by_restart = []  
        self.final_objective_values = []  
        self.initial_cube_states = []  
        self.final_cube_states = []  
        self.restart_durations = []  
        self.iterations_per_restart = []  # Track iterations for each restart

    def run(self):
        overall_start_time = time.time()

        for restart in range(self.max_restarts):
            print(f"\nRestart {restart + 1}/{self.max_restarts}...")
            
            # Randomize initial state for each restart
            self.magic_cube.data = self.magic_cube.initialize_cube()
            self.initial_cube_states.append(copy.deepcopy(self.magic_cube.data))  # Save initial state for reporting
            
            # Copy randomized cube state for the steepest ascent hill climbing algorithm
            cube_copy = copy.deepcopy(self.magic_cube)
            hill_climber = SteepestAscentHillClimbing(cube_copy)

            # Track time and iterations for this restart
            restart_start_time = time.time()
            hill_climber.run()
            restart_end_time = time.time()
            self.restart_durations.append(restart_end_time - restart_start_time)
            self.iterations_per_restart.append(hill_climber.iterations)  # Track iterations
            
            # Append the objective values of this restart
            self.all_objective_values_by_restart.append(hill_climber.objective_values)
            
            # Store the final state and objective value of this restart
            final_value = hill_climber.objective_values[-1]
            self.final_objective_values.append(final_value)
            self.final_cube_states.append(copy.deepcopy(hill_climber.magic_cube.data))
            
            # Check if this restart found a better solution
            if final_value < self.best_objective_value:
                self.best_objective_value = final_value
                self.best_cube_state = copy.deepcopy(hill_climber.magic_cube.data)

        overall_end_time = time.time()
        self.total_duration = overall_end_time - overall_start_time

    def report(self):
        """Generate a report with detailed information and plots."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print("\nExperiment Report:")
        total_iterations = sum(self.iterations_per_restart)
        for i in range(self.max_restarts):
            print(f"\nRestart {i + 1}/{self.max_restarts}:")
            print(f"Initial State: {self.initial_cube_states[i]}")
            print(f"Final State: {self.final_cube_states[i]}")
            print(f"Final Objective Value: {self.final_objective_values[i]}")
            print(f"Iterations: {self.iterations_per_restart[i]}")
            print(f"Duration: {self.restart_durations[i]:.4f} seconds")

        print("\nBest Overall Solution:")
        print(f"Final Objective Value: {self.best_objective_value}")
        print(f"Best Final Cube State: {self.best_cube_state}")
        print(f"Total Iterations Across All Restarts: {total_iterations}")
        print(f"Total Duration (all restarts): {self.total_duration:.4f} seconds")

        # Plot 1: Objective Function Value over Iterations (with Random Restarts)
        plt.figure(figsize=(12, 6))
        
        # Subplot 1: Iterations vs. Objective Function Value for each restart
        plt.subplot(1, 2, 1)
        for restart_index, objective_values in enumerate(self.all_objective_values_by_restart):
            plt.plot(objective_values, label=f'Restart {restart_index + 1}')
        
        plt.xlabel('Iterations')
        plt.ylabel('Objective Function Value')
        plt.title('Objective Function Value over Iterations (Random Restarts)')
        plt.legend(title='Restart')
        plt.grid(True)

        # Subplot 2: Final Objective Function Value per Restart
        plt.subplot(1, 2, 2)
        plt.plot(range(1, self.max_restarts + 1), self.final_objective_values, 'o-', color='red')
        plt.xlabel('Restart Number')
        plt.ylabel('Final Objective Function Value')
        plt.title('Final Objective Function Value per Restart')
        plt.grid(True)

        # Adjust layout to prevent overlap
        plt.tight_layout()

        # Save the combined plot with a timestamp in the filename
        plt.savefig(f'./data/random_restart_hill_climbing_combined_plot_{timestamp}.png', format='png')
        plt.show()

if __name__ == "__main__":
    cube = MagicCube(size=5)
    random_restart_hill_climber = RandomRestartHillClimbing(cube, max_restarts=5)
    random_restart_hill_climber.run()
    random_restart_hill_climber.report()
