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
        """Menghasilkan populasi awal dengan state kubus acak."""
        self.population = [self.magic_cube.initialize_cube() for _ in range(self.population_size)]
    
    def calculate_fitness(self, individual):
        """Menggunakan fungsi objektif dari magic cube sebagai ukuran fitness."""
        self.magic_cube.data = individual  # Set cube state
        return -self.magic_cube.objective_function()  # Gunakan negatif untuk memperlakukan nilai yang lebih kecil sebagai lebih baik

    def select_parents(self):
        """Memilih dua orang tua menggunakan tournament_size."""
        tournament_size = min(4, self.population_size)  # Safely set tournament size
        parents = []
        for _ in range(2):  # Membutuhkan dua orang tua
            candidates = random.sample(self.population, tournament_size)
            parents.append(min(candidates, key=self.calculate_fitness))
        return parents

    def crossover(self, parent1, parent2):
        """Crossover dua induk dengan memilih baris secara acak dari setiap induk."""
        child = []
        for layer1, layer2 in zip(parent1, parent2):
            # Memilih baris secara acak dari salah satu orang tua
            child_layer = [random.choice([r1, r2]) for r1, r2 in zip(layer1, layer2)]
            child.append(child_layer)
        return child

    def mutate(self, individual):
        """Melakukan mutasi pada individu dengan mengacak satu row dalam satu layer."""
        if random.random() < self.mutation_rate:
            layer = random.choice(individual)
            row = random.choice(layer)
            random.shuffle(row)

    def evolve_population(self):
        """Menciptakan populasi baru melalui seleksi, crossover, dan mutasi."""
        new_population = []
        while len(new_population) < self.population_size:
            parent1, parent2 = self.select_parents()
            child = self.crossover(parent1, parent2)
            self.mutate(child)
            new_population.append(child)
        self.population = new_population

    def run(self):
        """Run genetic algorithm untuk mengoptimalkan magic cube."""
        self.start_time = time.time()
        
        self.initialize_population()
        self.initial_state = copy.deepcopy(self.magic_cube.data)

        for iteration in range(self.amount_iteration):
            fitness_values = [self.calculate_fitness(individual) for individual in self.population]
            best_index = fitness_values.index(max(fitness_values))
            best_fitness = -fitness_values[best_index]  # Mengubah kembali ke nilai positif untuk objective value

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
        """Plot best dan average objective values selama iterasi."""
        iterations, best_values, avg_values = zip(*self.objective_values_history)
        plt.plot(iterations, best_values, label='Best Objective Value')
        plt.plot(iterations, avg_values, label='Average Objective Value')
        plt.xlabel('Iterations')
        plt.ylabel('Objective Function Value')
        plt.title('Genetic Algorithm Optimization of Magic Cube')
        plt.legend()
        plt.show()

    def report(self):
        """Menampilkan hasil termasuk initial and final state, objective value, population size, iterations, and duration."""
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