import algorithms.genetic_algorithm
import algorithms.hill_climbing_with_sideways_move
import algorithms.random_restart_hill_climbing
import algorithms.simulated_annealing
import algorithms.steepest_ascent_hill_climbing
import algorithms.stochastic_hill_climbing
from cube.cube import MagicCube
import algorithms
import copy
import matplotlib.pyplot as plt

# Algorithm selection constants
STEEPEST_ASCENT_HC = 1
STOCHASTIC_HC = 2
SIDEWAYS_MOVE_HC = 3
RANDOM_RESTART_HC = 4
SIMULATED_ANNEALING = 5
GENETIC_ALGORITHM = 6

# Global variable to control the selected algorithm
SEARCH_ALGO = STEEPEST_ASCENT_HC  # Default to Steepest Ascent HC

# Select the search algorithm based on user input
def select_search_algo(value: int):
    global SEARCH_ALGO
    if 1 <= value <= 6:
        SEARCH_ALGO = value
        algo_names = ['Steepest Ascent HC', 'Stochastic HC', 'HC with Sideways Move',
                      'Random Restart HC', 'Simulated Annealing', 'Genetic Algorithm']
        print(f"Selected search algorithm: {algo_names[SEARCH_ALGO - 1]}")
    else:
        raise ValueError("Invalid algorithm selection. Please choose a number between 1 and 6.")

# Start the local search based on the selected algorithm
def start_search(magic_cube):
    print("\nStarting Local Search...")

    # Create a deep copy of the cube to ensure the search runs on a fresh copy
    cube_copy = copy.deepcopy(magic_cube)
    
    try:
        # Instantiate and run the selected search algorithm
        if SEARCH_ALGO == STEEPEST_ASCENT_HC:
            algorithm = algorithms.steepest_ascent_hill_climbing.SteepestAscentHillClimbing(cube_copy)
        elif SEARCH_ALGO == STOCHASTIC_HC:
            algorithm = algorithms.stochastic_hill_climbing.StochasticHillClimbing(cube_copy)
        elif SEARCH_ALGO == SIDEWAYS_MOVE_HC:
            algorithm = algorithms.hill_climbing_with_sideways_move.HillClimbingWithSidewaysMove(cube_copy)
        elif SEARCH_ALGO == RANDOM_RESTART_HC:
            algorithm = algorithms.random_restart_hill_climbing.RandomRestartHillClimbing(cube_copy)
        elif SEARCH_ALGO == SIMULATED_ANNEALING:
            algorithm = algorithms.simulated_annealing.SimulatedAnnealing(cube_copy)
        elif SEARCH_ALGO == GENETIC_ALGORITHM:
            algorithm = algorithms.genetic_algorithm.GeneticAlgorithm(cube_copy)
        else:
            raise ValueError("Selected algorithm is not implemented.")
        
        # Run the algorithm
        algorithm.run()
        
        # Report results
        algorithm.report()

    except Exception as e:
        print(f"An error occurred during the search: {e}")

# Main function to handle user input and algorithm initialization
def main():
    print("Welcome to the Magic Cube Solver")
    
    # Initialize Magic Cube
    print("\nInitializing Magic Cube...")
    try:
        mc = MagicCube(size=5)
    except Exception as e:
        print(f"An error occurred while initializing the Magic Cube: {e}")
        return  # Exit if cube initialization fails

    while True:
        print("\nAvailable Algorithms:")
        print("1: Steepest Ascent HC")
        print("2: Stochastic HC")
        print("3: HC with Sideways Move")
        print("4: Random Restart HC")
        print("5: Simulated Annealing")
        print("6: Genetic Algorithm")
        print("0: Exit Program")

        # Get user input for algorithm selection
        while True:
            try:
                choice = int(input("Select an algorithm (1-6, or 0 to exit): "))
                if choice == 0:
                    print("Exiting the program. Goodbye!")
                    return  # Exit the program
                select_search_algo(choice)
                break
            except ValueError as e:
                print(f"Error: {e}. Please enter a valid number between 0 and 6.")

        # Start the search based on the selected algorithm
        start_search(mc)

if __name__ == "__main__":
    main()
