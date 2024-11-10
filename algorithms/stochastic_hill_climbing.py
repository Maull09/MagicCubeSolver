import random
import copy
import time
import datetime
import matplotlib.pyplot as plt
from cube.cube import MagicCube  # Impor kelas MagicCube dari cube.py

class StochasticHillClimbing:
    def __init__(self, magic_cube, max_trials=10000):
        self.magic_cube = magic_cube
        self.max_trials = max_trials
        self.iterations = 0
        self.start_time = None
        self.end_time = None
        self.objective_values = []  # Menyimpan nilai objective function untuk setiap percobaan
        self.initial_cube = copy.deepcopy(self.magic_cube.data)  # Salin kondisi awal kubus
        self.final_cube = None  # Menyimpan kondisi akhir kubus

    def run(self):
        # Simpan waktu mulai
        self.start_time = time.time()

        # Nilai objektif dari kondisi awal kubus
        current_cube = copy.deepcopy(self.initial_cube)
        current_cost = self.objective_function(current_cube)
        self.objective_values.append(current_cost)

        for _ in range(self.max_trials):
            self.iterations += 1

            # Buat tetangga dengan menukar dua posisi acak
            neighbor_cube = copy.deepcopy(current_cube)
            pos1 = self._random_position()
            pos2 = self._random_position(different_from=pos1)
            self.swap(neighbor_cube, pos1, pos2)

            # Hitung nilai objektif dari tetangga
            neighbor_cost = self.objective_function(neighbor_cube)

            # Jika tetangga lebih baik, pindah ke state tersebut
            if neighbor_cost < current_cost:
                current_cube = neighbor_cube
                current_cost = neighbor_cost

            # Simpan nilai objektif untuk setiap percobaan
            self.objective_values.append(current_cost)

            # Berhenti jika solusi optimal (biaya 0) ditemukan
            if current_cost == 0:
                print(f"Solusi optimal ditemukan pada iterasi {self.iterations}")
                break

        # Simpan waktu selesai
        self.end_time = time.time()
        self.final_cube = current_cube  # Simpan kondisi akhir kubus

    def objective_function(self, cube_data):
        original_data = self.magic_cube.data
        self.magic_cube.data = cube_data
        cost = self.magic_cube.objective_function()
        self.magic_cube.data = original_data  # Kembalikan data asli
        return cost

    def _random_position(self, different_from=None):
        size = self.magic_cube.size
        while True:
            position = (random.randint(0, size - 1),
                        random.randint(0, size - 1),
                        random.randint(0, size - 1))
            if position != different_from:
                return position

    def swap(self, cube_data, pos1, pos2):
        x1, y1, z1 = pos1
        x2, y2, z2 = pos2
        cube_data[x1][y1][z1], cube_data[x2][y2][z2] = cube_data[x2][y2][z2], cube_data[x1][y1][z1]

    def report(self):
        duration = self.end_time - self.start_time
        print("===== Laporan Hasil Stochastic Hill Climbing =====")
        print(f"Durasi Pencarian       : {duration:.4f} detik")
        print(f"Total Iterasi          : {self.iterations}")
        print(f"Nilai Objective Awal   : {self.objective_values[0]}")
        print(f"Initial State: ")
        print((self.initial_cube))
        print(f"Nilai Objective Akhir  : {self.objective_values[-1]}")
        print(f"Final State: ")
        print((self.final_cube))
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Plot hasil
        plt.figure(figsize=(10, 5))
        plt.plot(self.objective_values)
        plt.xlabel('Iterasi')
        plt.ylabel('Nilai Objective Function')
        plt.title('Performa Stochastic Hill Climbing')
        plt.grid(True)
        plt.savefig(f'./data/stochastic_hill_climbing_plot_{timestamp}.png', format='png')
        plt.show()
        

if __name__ == "__main__":
    cube_size = 5
    magic_cube = MagicCube(size=cube_size)
    shc = StochasticHillClimbing(magic_cube, max_trials=10000)
    shc.run()
    shc.report()