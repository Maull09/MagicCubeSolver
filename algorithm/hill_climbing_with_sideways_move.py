import time
from cube.cube import MagicCube

def hill_climbing_with_sideways_move(magic_cube):
    """Hill Climbing with sideways moves for the Magic Cube."""
    current_value = -magic_cube.objective_function()
    iteration = 0
    start_time = time.time()

    while True:
        neighbors = []
        for i in range(magic_cube.size):
            for j in range(magic_cube.size):
                for k in range(magic_cube.size):
                    for x in range(magic_cube.size):
                        for y in range(magic_cube.size):
                            for z in range(magic_cube.size):
                                if (i, j, k) != (x, y, z):  # Ensure distinct positions
                                    magic_cube.swap((i, j, k), (x, y, z))
                                    neighbor_value = -magic_cube.objective_function()
                                    neighbors.append(((i, j, k), (x, y, z), neighbor_value))
                                    magic_cube.swap((i, j, k), (x, y, z))  # Revert swap

        best_neighbor = max(neighbors, key=lambda n: n[2], default=None)
        
        # Print iteration and timing
        iteration += 1
        elapsed_time = time.time() - start_time
        print(f"Iteration {iteration}: Current Objective = {-current_value}, Time Elapsed = {elapsed_time:.4f} seconds")

        # Stop if no better or sideways move can be made
        if best_neighbor is None or best_neighbor[2] < current_value:
            break

        # Perform the best swap
        pos1, pos2, best_value = best_neighbor
        magic_cube.swap(pos1, pos2)
        current_value = best_value

    return magic_cube.cube

# # Example usage
# if __name__ == "__main__":
#     cube = MagicCube(size=5)
#     print("Initial Objective:", cube.objective_function())
#     final_state = hill_climbing_with_sideways_move(cube)
#     print("Final Objective:", cube.objective_function())
