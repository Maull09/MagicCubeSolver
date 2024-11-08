import copy
import datetime
from matplotlib import pyplot as plt
from algorithms.steepest_ascent_hill_climbing import SteepestAscentHillClimbing
from cube.cube import MagicCube

class RandomRestartHillClimbing:
    def __init__(self, magic_cube, max_restarts=5):
        self.magic_cube = magic_cube
        self.max_restarts = max_restarts
        self.best_cube_state = None
        self.best_objective_value = float('inf')
        self.all_objective_values_by_restart = []  # Store objective values for each restart

    def run(self):
        for restart in range(self.max_restarts):
            print(f"\nRestart {restart + 1}/{self.max_restarts}...")
            
            # Randomize initial state for each restart
            self.magic_cube.data = self.magic_cube.initialize_cube()
            cube_copy = copy.deepcopy(self.magic_cube)  # Copy the randomized state
            
            # Run Steepest Ascent Hill Climbing on the randomized cube
            hill_climber = SteepestAscentHillClimbing(cube_copy)
            hill_climber.run()
            
            # Append the objective values of this restart
            self.all_objective_values_by_restart.append(hill_climber.objective_values)
            
            # Check if this restart found a better solution
            final_value = hill_climber.objective_values[-1]
            if final_value < self.best_objective_value:
                self.best_objective_value = final_value
                self.best_cube_state = copy.deepcopy(hill_climber.magic_cube.data)

    def report(self):
        """Plot the objective values over all restarts with a different color for each restart."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Plotting
        plt.figure(figsize=(10, 6))
        for restart_index, objective_values in enumerate(self.all_objective_values_by_restart):
            plt.plot(objective_values, label=f'Restart {restart_index + 1}')
        
        plt.xlabel('Iterations')
        plt.ylabel('Objective Function Value')
        plt.title('Objective Function Value over Iterations (with Random Restarts)')
        plt.legend(title='Restart')
        plt.grid(True)

        # Save the plot with a timestamp in the filename
        plt.savefig(f'./data/random_restart_hill_climbing_plot_{timestamp}.png', format='png')
        plt.show()

if __name__ == "__main__":
    cube = MagicCube(size=5)
    random_restart_hill_climber = RandomRestartHillClimbing(cube, max_restarts=5)
    random_restart_hill_climber.run()
    random_restart_hill_climber.report()
