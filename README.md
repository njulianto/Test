# Sistem Pelacakan Kegiatan Harian

Sistem sederhana untuk mencatat dan melihat laporan kegiatan harian (Harian), data karyawan, dan master task.

## Struktur Folder

- `data/tasks.csv` — data utama (jangan diubah baris lama)
- `data/employees.csv` — daftar karyawan + gaji saat ini
- `data/task_master.csv` — daftar task yang diizinkan
- `docs/SCHEMA.md` — penjelasan kolom
- `scripts/` — skrip validasi, laporan, export
- `reports/index.html` — dashboard (dibuat otomatis)
- `exports/` — file export

## Cara Melihat Laporan

1. Buka folder `reports/` di GitHub.
2. Download `index.html` lalu buka di browser, **atau**
3. Jika GitHub Pages diaktifkan (lihat panduan di bawah), buka link Pages.

## Cara Menambah Data Baru (via Claude atau manual)

1. Minta Claude menghasilkan baris CSV baru (lihat template di bawah).
2. Buat Pull Request yang menambahkan baris di bagian bawah `data/tasks.csv`.
3. Jangan pernah mengedit baris lama (terutama kolom `rate_per_hk`).

## Cara Mengubah Gaji Karyawan

1. Edit file `data/employees.csv`.
2. Ubah kolom `current_rate_per_hk`.
3. Buat Pull Request.
4. Data lama di `tasks.csv` **tidak berubah**. Hanya data baru yang akan memakai gaji baru.

## Cara Export

Jalankan di komputer yang sudah install Python:

```bash
pip install -r requirements.txt
python scripts/export.py
```

File hasil ada di folder `exports/`.

## Template untuk Claude (salin-tempel)

```
Kamu adalah asisten input data. Selalu keluarkan baris CSV baru untuk file data/tasks.csv dengan kolom PERSIS seperti ini (urutan tidak boleh berubah):

date,task,employee_name,position,hk,overtime,output,output_premium,total_output,unit,estate,block,notes,rate_per_hk,premium_rate,hk_amount,premium_amount,overtime_amount,group

Aturan:
- date format YYYY-MM-DD
- employee_name harus persis sama dengan yang ada di data/employees.csv
- task harus persis sama dengan yang ada di data/task_master.csv
- rate_per_hk ambil dari current_rate_per_hk karyawan tersebut (jangan tebak)
- Jika tidak ada nilai, kosongkan saja (jangan tulis 0 atau N/A)
- Keluarkan HANYA baris CSV, tanpa penjelasan lain.

Data yang ingin ditambahkan:
[isi di sini]
```

## Validasi Otomatis

Setiap Pull Request akan dicek oleh GitHub Actions. Jika ada nama karyawan/task yang tidak dikenal, format salah, atau duplikat, PR akan ditolak.
