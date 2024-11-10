import matplotlib.pyplot as plt
import time
import random
import copy
import datetime
from cube.cube import MagicCube

class GeneticAlgorithm:
    def __init__(self, magic_cube, amount_iteration, population_size, mutation_rate=0.01):
        self.magic_cube = magic_cube
        self.amount_iteration = amount_iteration

        self.population_size = population_size
        self.mutation_rate = mutation_rate

        self.population = []
        self.best_solution = None
        self.best_objective_value = float('inf')
        self.objective_values_history = []
        self.start_time = None
        self.end_time = None
        self.initial_state = None
        self.final_state = None

    def initialize_population(self):
        """Initialize the population with random cube states."""
        self.population = [self.magic_cube.initialize_cube() for _ in range(self.population_size)]
    
    def calculate_fitness(self, individual):
        """Calculate the fitness of an individual based on the objective function."""
        self.magic_cube.data = individual  # Set cube state
        return -self.magic_cube.objective_function()  # Use negative to treat smaller values as better

    def select_parents(self):
        """Select two parents using tournament selection."""
        tournament_size = min(2, self.population_size)  # Safely set tournament size
        parents = []
        for _ in range(2):  # We need two parents
            candidates = random.sample(self.population, tournament_size)
            parents.append(min(candidates, key=self.calculate_fitness))
        return parents

    def crossover(self, parent1, parent2):
        """Crossover two parents by randomly selecting rows from each parent."""
        child = []
        for layer1, layer2 in zip(parent1, parent2):
            # Randomly select rows from either parent
            child_layer = [random.choice([r1, r2]) for r1, r2 in zip(layer1, layer2)]
            child.append(child_layer)
        return child

    def mutate(self, individual):
        """Mutate an individual by randomly shuffling a row in a layer."""
        if random.random() < self.mutation_rate:
            layer = random.choice(individual)
            row = random.choice(layer)
            random.shuffle(row)

    def evolve_population(self):
        """Create a new population by selecting parents, performing crossover, and mutating."""
        new_population = []
        while len(new_population) < self.population_size:
            parent1, parent2 = self.select_parents()
            child = self.crossover(parent1, parent2)
            self.mutate(child)
            new_population.append(child)
        self.population = new_population

    def run(self):
        """Run the genetic algorithm to optimize the magic cube."""
        self.start_time = time.time()
        
        self.initialize_population()
        self.initial_state = copy.deepcopy(self.magic_cube.data)

        for iteration in range(self.amount_iteration):
            fitness_values = [self.calculate_fitness(individual) for individual in self.population]
            best_index = fitness_values.index(max(fitness_values))
            best_fitness = -fitness_values[best_index]  # Convert back to positive for objective value

            if best_fitness < self.best_objective_value:
                self.best_objective_value = best_fitness
                self.best_solution = self.population[best_index]

            self.objective_values_history.append((iteration, best_fitness, sum(-f for f in fitness_values) / self.population_size))
            
            elapsed_time = time.time() - self.start_time
            print(f"Iteration {iteration}: Objective = {best_fitness}, Time = {elapsed_time:.4f} seconds")

            self.evolve_population()

        self.end_time = time.time()
        self.final_state = self.best_solution

    def plot_objective_values(self):
        """Plot best and average objective values over iterations."""
        iterations, best_values, avg_values = zip(*self.objective_values_history)
        plt.plot(iterations, best_values, label='Best Objective Value')
        plt.plot(iterations, avg_values, label='Average Objective Value')
        plt.xlabel('Iterations')
        plt.ylabel('Objective Function Value')
        plt.title('Genetic Algorithm Optimization of Magic Cube')
        plt.legend()
        plt.show()

    def report(self):
        """Display the results including initial and final state, objective value, population size, iterations, and duration."""
        duration = self.end_time - self.start_time
        print("Initial State:")
        print(self.initial_state)
        print("\nFinal State:")
        print(self.final_state)
        print(f"\nFinal Objective Value: {self.best_objective_value}")
        print(f"Population Size: {self.population_size}")
        print(f"Iterations: {self.amount_iteration}")
        print(f"Duration: {duration:.2f} seconds")

        self.plot_objective_values()

if __name__ == "__main__":
    from cube.cube import MagicCube  
    amount_iteration = 100
    mutation_rate = 0.01
    population_size = 8

    magic_cube = MagicCube(size=5)  
    ga_solver = GeneticAlgorithm(magic_cube, amount_iteration, population_size, mutation_rate)
    ga_solver.run()
    ga_solver.plot_objective_values()
    ga_solver.report()