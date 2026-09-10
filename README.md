# WPOS PRO V1.0

POS toko sembako Windows offline, satu komputer.

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
- Penjualan diproses atomically: transaksi, item, pengurangan stok dan mutasi stok berhasil bersama atau dibatalkan bersama.
- Penjualan CASH menambah kas.
- QRIS/TRANSFER/DEBIT tidak menambah kas.
- Pembayaran non-tunai harus sama persis dengan total.
- Kembalian hanya untuk CASH.
- Mutasi stok dicatat untuk penjualan, pembelian dan penyesuaian stok.

## Keamanan akun
- Password menggunakan PBKDF2-HMAC-SHA256 dengan salt acak.
- Hanya akun aktif yang dapat login.
- Policy role dipusatkan di `app/services/access.py`.
- Administrator terakhir tidak boleh dinonaktifkan.
- Akun sendiri tidak boleh dinonaktifkan melalui user-management service.

## Default login
- Username: `admin`
- Password: `admin123`

**Penting:** ubah password default sebelum produksi.

## Data Windows
Saat dijalankan sebagai EXE, database dan backup disimpan di `%LOCALAPPDATA%\\WPOS PRO`, sehingga aplikasi tidak perlu menulis database ke Program Files.

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
Repository ini adalah master source pengembangan WPOS PRO V1.0. Setiap fitur dianggap selesai setelah terintegrasi, diuji, dan diaudit; bukan hanya setelah source berhasil di-commit.
