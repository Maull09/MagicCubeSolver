from cube import MagicCube
import random

def main():
    # Initialize a 5x5x5 magic cube
    magic_cube = MagicCube(size=5)
    
    # Print initial state of the cube and calculate the magic number
    print("Initial Cube State:")
    for layer in magic_cube.cube:
        for row in layer:
            print(row)
        print()
    
    print("Magic Number:", magic_cube.magic_number)

    # Evaluate initial objective function value
    initial_diff = magic_cube.objective_function()
    print("Initial Objective Function (Total Difference):", initial_diff)
    
    # Perform a few random swaps and evaluate again
    for _ in range(5):  # Perform 5 random swaps
        pos1 = (random.randint(0, 4), random.randint(0, 4), random.randint(0, 4))
        pos2 = (random.randint(0, 4), random.randint(0, 4), random.randint(0, 4))
        magic_cube.swap(pos1, pos2)
        print(f"Swapped positions {pos1} and {pos2}")

    # Evaluate objective function after swaps
    new_diff = magic_cube.objective_function()
    print("Objective Function After Swaps (Total Difference):", new_diff)

    # Summary of the result
    if new_diff < initial_diff:
        print("The swaps brought the cube closer to the magic properties.")
    else:
        print("The swaps did not improve the cube's alignment with the magic properties.")

    for layer in magic_cube.cube:
        for row in layer:
            print(row)
        print()
        
if __name__ == "__main__":
    main()
