# MagicCubeSolver

MagicCubeSolver dibuat untuk untuk menyelesaikan permasalahan diagonal magic cube, menggunakan algoritma-algoritma local search. Proyek ini dikembangkan untuk memenuhi tugas besar mata kuliah IF3070 Dasar Inteligensi Artifisial Tahun Ajaran 2024/2025.

## Deskripsi Proyek

Diagonal Magic Cube adalah kubus yang berisi angka dari 1 hingga \( n^3 \) yang diatur sedemikian rupa sehingga setiap baris, kolom, tiang, dan diagonal dari kubus memiliki jumlah yang sama, yang disebut magic number. MagicCubeSolver mengimplementasikan algoritma local search untuk mencari solusi dari permasalahan tersebut.
### Algoritma yang Diimplementasikan

Repository ini berisi implementasi dari beberapa algoritma *local search*, yaitu:
1. **Hill-Climbing**:
   - *Steepest Ascent Hill-Climbing*
   - *Stochastic Hill-Climbing*
   - *Hill-Climbing with Sideways Move*
   - *Random Restart Hill-Climbing*
2. **Simulated Annealing**
3. **Genetic Algorithm**

## Persyaratan

Proyek ini membutuhkan library matplotlib untuk visualisasi hasil eksperimen

- Instal matplotlib dengan perintah berikut:
```
pip install matplotlib
```

## Cara Menjalankan program

1. Clone repository

   ```
   git clone https://github.com/Maull09/MagicCubeSolver.git
   ```
2. Masuk ke directory
   ```
   cd MagicCubeSolver/src
   ```
3. Jalankan program
   ```
   python main.py
   ```

## Kontributor
|NIM | Nama | Tugas|
|:-|:-|:-|
|18222104|Adinda Khairunnisa I| Stochastic Hill-Climbing, Simulated Annealing|
|18222126|Alfaza Naufal Zakiy| Genetic Algorithm|
|18222132|Chairul Nur Wahid|Hill-Climbing with Sideways Move, Simulated Annealing|
|18222140|M. Maulana Firdaus R|Steepest Ascent Hill-Climbing, Random Restart Hill-Climbing|
