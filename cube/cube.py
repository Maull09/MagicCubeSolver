import random
import math
import tkintertools as tkt
from tkintertools import tools_3d as t3d
from tkintertools import constants

class MagicCube:
    """5x5x5 Magic Cube with local search functionality"""

    def __init__(self, canvas, size=5):
        self.size = size
        self.canvas = canvas
        self.blocks = []
        self.data = self.initialize_cube()
        self.magic_number = self.calculate_magic_number()

        # Larger spacing factor for 3D visualization
        s = 100 # Spacing factor
        center_offset = (self.size - 1) / 2  # Center the cube in 3D space

        # Initialize each cell with a 3D number display
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    value = self.data[x][y][z]

                    # Create a 3D text item for each number at the correct 3D position
                    text_item = t3d.Text3D(
                        canvas,
                        [(x - center_offset) * s, (y - center_offset) * s, (z - center_offset) * s],
                        text=str(value),
                        fill="white",
                        font=("Helvetica", 12, "bold")
                    )
                    self.blocks.append(text_item)

        canvas.space_sort()  # Sort for correct depth rendering

    def initialize_cube(self):
        """Initialize the cube with numbers 1 to size^3."""
        n = self.size ** 3
        numbers = list(range(1, n + 1))
        random.shuffle(numbers)
        return [[[numbers.pop() for _ in range(self.size)] for _ in range(self.size)] for _ in range(self.size)]

    def calculate_magic_number(self):
        """Calculate the target magic number for each row, column, and diagonal."""
        n = self.size
        return n * (n ** 3 + 1) // 2

    def objective_function(self):
        """Calculate the total deviation from the magic number for rows, columns, pillars, and diagonals."""
        total_difference = 0

        # Check rows, columns, and pillars
        for i in range(self.size):
            for j in range(self.size):
                # Sum along each row (yz planes)
                total_difference += abs(sum(self.cube[i][j]) - self.magic_number)
                # Sum along each column (xz planes)
                total_difference += abs(sum(self.cube[k][i][j] for k in range(self.size)) - self.magic_number)
                # Sum along each pillar (xy planes)
                total_difference += abs(sum(self.cube[j][k][i] for k in range(self.size)) - self.magic_number)

        # Check 3D space diagonals
        space_diagonals = [
            sum(self.cube[i][i][i] for i in range(self.size)),  # (0,0,0) to (4,4,4)
            sum(self.cube[i][i][self.size - 1 - i] for i in range(self.size)),  # (0,0,4) to (4,4,0)
            sum(self.cube[i][self.size - 1 - i][i] for i in range(self.size)),  # (0,4,0) to (4,0,4)
            sum(self.cube[i][self.size - 1 - i][self.size - 1 - i] for i in range(self.size))  # (0,4,4) to (4,0,0)
        ]
        total_difference += sum(abs(diag - self.magic_number) for diag in space_diagonals)

        # Check 2D plane diagonals in each slice
        for i in range(self.size):
            # Diagonals within each xy plane
            total_difference += abs(sum(self.cube[i][j][j] for j in range(self.size)) - self.magic_number)
            total_difference += abs(sum(self.cube[i][j][self.size - 1 - j] for j in range(self.size)) - self.magic_number)
            # Diagonals within each xz plane
            total_difference += abs(sum(self.cube[j][i][j] for j in range(self.size)) - self.magic_number)
            total_difference += abs(sum(self.cube[j][i][self.size - 1 - j] for j in range(self.size)) - self.magic_number)
            # Diagonals within each yz plane
            total_difference += abs(sum(self.cube[j][j][i] for j in range(self.size)) - self.magic_number)
            total_difference += abs(sum(self.cube[j][self.size - 1 - j][i] for j in range(self.size)) - self.magic_number)

        return total_difference

    def swap_blocks(self, pos1, pos2):
        """Swap two numbers within the cube and update their displayed positions."""
        x1, y1, z1 = pos1
        x2, y2, z2 = pos2
        # Swap data values
        self.data[x1][y1][z1], self.data[x2][y2][z2] = self.data[x2][y2][z2], self.data[x1][y1][z1]

        # Update the displayed numbers in 3D
        index1 = x1 * self.size ** 2 + y1 * self.size + z1
        index2 = x2 * self.size ** 2 + y2 * self.size + z2
        self.blocks[index1].configure(text=str(self.data[x1][y1][z1]))
        self.blocks[index2].configure(text=str(self.data[x2][y2][z2]))

        # Refresh canvas sorting to maintain correct depth rendering
        self.canvas.space_sort()


# import random

# class MagicCube:
#     """Represents a 5x5x5 Diagonal Magic Cube with position swapping."""

#     def __init__(self, size=5):
#         self.size = size  # Cube dimension (5x5x5)
#         self.cube = self.initialize_cube()
#         self.magic_number = self.calculate_magic_number()

#     def initialize_cube(self):
#         """Randomly initializes the cube with numbers 1 through 125."""
#         numbers = list(range(1, self.size ** 3 + 1))
#         random.shuffle(numbers)
#         # Reshape into 5x5x5 grid
#         return [[[numbers.pop() for _ in range(self.size)] for _ in range(self.size)] for _ in range(self.size)]

#     def calculate_magic_number(self):
#         """Calculate the magic number for a 5x5x5 cube."""
#         n = self.size
#         return n * (n ** 3 + 1) // 2

#     def objective_function(self):
#         """Calculate the total deviation from the magic number for rows, columns, pillars, and diagonals."""
#         total_difference = 0

#         # Check rows, columns, and pillars
#         for i in range(self.size):
#             for j in range(self.size):
#                 # Sum along each row (yz planes)
#                 total_difference += abs(sum(self.cube[i][j]) - self.magic_number)
#                 # Sum along each column (xz planes)
#                 total_difference += abs(sum(self.cube[k][i][j] for k in range(self.size)) - self.magic_number)
#                 # Sum along each pillar (xy planes)
#                 total_difference += abs(sum(self.cube[j][k][i] for k in range(self.size)) - self.magic_number)

#         # Check 3D space diagonals
#         space_diagonals = [
#             sum(self.cube[i][i][i] for i in range(self.size)),  # (0,0,0) to (4,4,4)
#             sum(self.cube[i][i][self.size - 1 - i] for i in range(self.size)),  # (0,0,4) to (4,4,0)
#             sum(self.cube[i][self.size - 1 - i][i] for i in range(self.size)),  # (0,4,0) to (4,0,4)
#             sum(self.cube[i][self.size - 1 - i][self.size - 1 - i] for i in range(self.size))  # (0,4,4) to (4,0,0)
#         ]
#         total_difference += sum(abs(diag - self.magic_number) for diag in space_diagonals)

#         # Check 2D plane diagonals in each slice
#         for i in range(self.size):
#             # Diagonals within each xy plane
#             total_difference += abs(sum(self.cube[i][j][j] for j in range(self.size)) - self.magic_number)
#             total_difference += abs(sum(self.cube[i][j][self.size - 1 - j] for j in range(self.size)) - self.magic_number)
#             # Diagonals within each xz plane
#             total_difference += abs(sum(self.cube[j][i][j] for j in range(self.size)) - self.magic_number)
#             total_difference += abs(sum(self.cube[j][i][self.size - 1 - j] for j in range(self.size)) - self.magic_number)
#             # Diagonals within each yz plane
#             total_difference += abs(sum(self.cube[j][j][i] for j in range(self.size)) - self.magic_number)
#             total_difference += abs(sum(self.cube[j][self.size - 1 - j][i] for j in range(self.size)) - self.magic_number)

#         return total_difference

#     def swap(self, pos1, pos2):
#         """Swaps two positions within the cube."""
#         x1, y1, z1 = pos1
#         x2, y2, z2 = pos2
#         self.cube[x1][y1][z1], self.cube[x2][y2][z2] = self.cube[x2][y2][z2], self.cube[x1][y1][z1]

#     def get_cube_numbers(self):
#         """Flatten the cube with 3D coordinates and values for visualization."""
#         cube_data = []
#         for x in range(self.size):
#             for y in range(self.size):
#                 for z in range(self.size):
#                     value = self.cube[x][y][z]
#                     cube_data.append((x, y, z, value))
#         return cube_data

#     def get_cube_blocks(self):
#         """Returns cube blocks with coordinates and values for visualization."""
#         center_offset = (self.size - 1) / 2
#         cube_data = []
#         for x in range(self.size):
#             for y in range(self.size):
#                 for z in range(self.size):
#                     value = self.cube[x][y][z]
#                     # Offset to center the cube in 3D space
#                     cube_data.append((x - center_offset, y - center_offset, z - center_offset, value))
#         return cube_data
