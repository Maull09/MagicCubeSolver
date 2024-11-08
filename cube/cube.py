import random
import math

class MagicCube:
    """5x5x5 Magic Cube with local search functionality"""

    def __init__(self, size=5):
        self.size = size
        self.data = self.initialize_cube()
        self.magic_number = self.calculate_magic_number()

    def initialize_cube(self):
        """Initialize the cube with numbers 1 to size^3."""
        n = self.size ** 3
        numbers = list(range(1, n + 1))
        random.shuffle(numbers)
        # Create a 3D cube structure with the shuffled numbers
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
                total_difference += abs(sum(self.data[i][j]) - self.magic_number)
                # Sum along each column (xz planes)
                total_difference += abs(sum(self.data[k][i][j] for k in range(self.size)) - self.magic_number)
                # Sum along each pillar (xy planes)
                total_difference += abs(sum(self.data[j][k][i] for k in range(self.size)) - self.magic_number)

        # Check 3D space diagonals
        space_diagonals = [
            sum(self.data[i][i][i] for i in range(self.size)),  # (0,0,0) to (size-1,size-1,size-1)
            sum(self.data[i][i][self.size - 1 - i] for i in range(self.size)),  # (0,0,size-1) to (size-1,size-1,0)
            sum(self.data[i][self.size - 1 - i][i] for i in range(self.size)),  # (0,size-1,0) to (size-1,0,size-1)
            sum(self.data[i][self.size - 1 - i][self.size - 1 - i] for i in range(self.size))  # (0,size-1,size-1) to (size-1,0,0)
        ]
        total_difference += sum(abs(diag - self.magic_number) for diag in space_diagonals)

        # Check 2D plane diagonals in each slice
        for i in range(self.size):
            # Diagonals within each xy plane
            total_difference += abs(sum(self.data[i][j][j] for j in range(self.size)) - self.magic_number)
            total_difference += abs(sum(self.data[i][j][self.size - 1 - j] for j in range(self.size)) - self.magic_number)
            # Diagonals within each xz plane
            total_difference += abs(sum(self.data[j][i][j] for j in range(self.size)) - self.magic_number)
            total_difference += abs(sum(self.data[j][i][self.size - 1 - j] for j in range(self.size)) - self.magic_number)
            # Diagonals within each yz plane
            total_difference += abs(sum(self.data[j][j][i] for j in range(self.size)) - self.magic_number)
            total_difference += abs(sum(self.data[j][self.size - 1 - j][i] for j in range(self.size)) - self.magic_number)

        return total_difference

    def swap(self, pos1, pos2):
        """Swap two numbers within the cube."""
        x1, y1, z1 = pos1
        x2, y2, z2 = pos2
        # Swap values in the data attribute
        self.data[x1][y1][z1], self.data[x2][y2][z2] = self.data[x2][y2][z2], self.data[x1][y1][z1]
