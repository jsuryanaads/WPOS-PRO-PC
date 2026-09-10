# WPOS PRO V1.1.1

Modern POS 2026 untuk toko sembako Windows offline, satu komputer.

## Teknologi
- Python 3.11+
- PySide6
- SQLite
- SQLAlchemy
- PyInstaller
- Inno Setup

## Alur kasir
Barcode → Keranjang → Diskon → Pembayaran → Kembalian → Stok berkurang → Transaksi tersimpan → Cetak struk.

## Modul
- Login
- Dashboard
- Kasir
- Produk
- Kategori dan Satuan
- Stok & Mutasi
- Pembelian
- Supplier
- Kas
- Pelanggan
- Laporan
- Pengaturan Toko
- Printer
- Backup / Restore
- User & Role Access

## Integritas transaksi
- Invoice unik.
- Barcode unik.
- Stok tidak boleh negatif.
- Penjualan diproses atomically.
- Penjualan CASH menambah kas.
- QRIS/TRANSFER/DEBIT tidak menambah kas.
- Pembayaran non-tunai harus sama persis dengan total.
- Kembalian hanya untuk CASH.
- Mutasi stok dicatat untuk penjualan, pembelian dan penyesuaian stok.

## Versioning
- Perubahan kecil: patch version.
- Perubahan menengah: naik ke target minor patch sesuai aturan proyek.
- Perubahan besar: naik ke versi minor baru, contoh V1.0.1 → V1.1.1.
- Redesign UI/UX Modern POS 2026 ditetapkan sebagai perubahan besar dan ditargetkan pada V1.1.1.

## Default login
- Username: `admin`
- Password: `admin123`

**Penting:** ubah password default sebelum produksi.

## Data Windows
Saat dijalankan sebagai EXE, database dan backup disimpan di `%LOCALAPPDATA%\\WPOS PRO`.

## Menjalankan dari source
```bat
python -m app.main
```

## Testing
```bat
pytest -q
```

## Build EXE
Jalankan `build.bat` pada Windows dengan Python dan PyInstaller terpasang.

## Installer
Compile `installer.iss` menggunakan Inno Setup setelah EXE berhasil dibuat.

## Status
WPOS PRO V1.1.1 adalah target pengembangan Modern POS 2026. Setiap fitur dianggap selesai setelah terintegrasi, diuji, dan diaudit.
