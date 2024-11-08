import random
import copy
import time
import matplotlib.pyplot as plt
from cube.cube import MagicCube  # Impor kelas MagicCube dari cube.py

class StochasticHillClimbing:
    def __init__(self, magic_cube, max_trials=10000):
        """
        Inisialisasi algoritma Stochastic Hill Climbing.

        Parameters:
        - magic_cube: objek MagicCube yang menjadi kubus awal.
        - max_trials: batas maksimum percobaan sebelum berhenti.
        """
        self.magic_cube = magic_cube
        self.max_trials = max_trials
        self.history = []  # Menyimpan nilai objective function untuk setiap percobaan
        self.iterations = 0  # Menyimpan jumlah iterasi
        self.duration = 0  # Menyimpan durasi pencarian

    def run(self):
        """
        Jalankan algoritma Stochastic Hill Climbing untuk menemukan solusi terbaik.
        """
        # Simpan waktu mulai
        start_time = time.time()

        # Simpan nilai objektif dari kondisi awal kubus
        current_cube = copy.deepcopy(self.magic_cube)  # Duplikasi objek awal
        initial_state = copy.deepcopy(current_cube.data)  # Simpan state awal
        current_cost = current_cube.objective_function()  # Hitung nilai objektif awal
        self.history.append(current_cost)

        for trial in range(self.max_trials):
            self.iterations += 1

            # Buat tetangga dengan menukar dua posisi acak
            neighbor_cube = copy.deepcopy(current_cube)
            pos1 = self._random_position()
            pos2 = self._random_position(different_from=pos1)
            neighbor_cube.swap(pos1, pos2)  # Tukar dua angka di posisi acak

            # Hitung nilai objektif dari tetangga
            neighbor_cost = neighbor_cube.objective_function()

            # Jika tetangga lebih baik, pindah ke state tersebut
            if neighbor_cost < current_cost:
                current_cube = neighbor_cube
                current_cost = neighbor_cost

            # Simpan nilai objektif untuk setiap percobaan
            self.history.append(current_cost)

            # Berhenti jika solusi optimal (biaya 0) ditemukan
            if current_cost == 0:
                print(f"Solusi optimal ditemukan pada iterasi {self.iterations}")
                break

        # Simpan waktu selesai dan hitung durasi
        end_time = time.time()
        self.duration = end_time - start_time

        # Simpan kondisi akhir setelah pencarian
        final_state = copy.deepcopy(current_cube.data)
        self.magic_cube = current_cube  # Perbarui magic_cube dengan solusi terbaik

        # Tampilkan laporan
        self.report(initial_state, final_state, current_cost)

    def _random_position(self, different_from=None):
        """
        Menghasilkan posisi acak dalam kubus 3D.

        Parameters:
        - different_from: tuple posisi yang harus dihindari (opsional)

        Returns:
        - Tuple (x, y, z) yang mewakili posisi dalam kubus.
        """
        size = self.magic_cube.size
        while True:
            position = (random.randint(0, size - 1),
                        random.randint(0, size - 1),
                        random.randint(0, size - 1))
            if position != different_from:
                return position

    def report(self, initial_state, final_state, final_cost):
        """
        Tampilkan hasil akhir dari pencarian dengan format sesuai file random restart.
        """
        print("===== Laporan Hasil Stochastic Hill Climbing =====")
        print(f"Durasi Pencarian       : {self.duration:.4f} detik")
        print(f"Total Iterasi          : {self.iterations}")
        print(f"Nilai Objective Awal   : {self.history[0]}")
        print(f"Nilai Objective Akhir  : {final_cost}")
        print("\nState Awal Kubus:")
        print(self._format_cube(initial_state))
        print("\nState Akhir Kubus:")
        print(self._format_cube(final_state))

        # Plot hasil
        plt.figure(figsize=(10, 5))
        plt.plot(self.history)
        plt.xlabel('Iterasi')
        plt.ylabel('Nilai Objective Function')
        plt.title('Performa Stochastic Hill Climbing')
        plt.grid(True)
        plt.show()

    def _format_cube(self, cube_data):
        """
        Format data kubus untuk ditampilkan.

        Parameters:
        - cube_data: data kubus yang akan diformat

        Returns:
        - String yang mewakili kubus dalam format yang mudah dibaca.
        """
        size = self.magic_cube.size
        cube_str = ""
        for z in range(size):
            cube_str += f"Layer {z + 1}:\n"
            for y in range(size):
                row = [str(cube_data[x][y][z]).rjust(3) for x in range(size)]
                cube_str += ' '.join(row) + '\n'
            cube_str += '\n'
        return cube_str

# Contoh penggunaan
if __name__ == "__main__":
    # Asumsikan Anda memiliki kelas MagicCube yang sudah diimplementasikan
    cube_size = 5
    magic_cube = MagicCube(size=cube_size)
    magic_cube.initialize_random()  # Metode untuk inisialisasi kubus secara acak

    shc = StochasticHillClimbing(magic_cube, max_trials=10000)
    shc.run()
