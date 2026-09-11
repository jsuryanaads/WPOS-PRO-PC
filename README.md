# WPOS PRO V1.1.6

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
- Perubahan besar: naik ke versi minor baru.
- **V1.1.6** adalah milestone UI/UX hardening: unified visual system, konsistensi halaman/dialog, focus state, keyboard navigation sidebar, accessibility metadata, dan release validation tanpa mengubah business logic transaksi.

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

## Release gate V1.1.6
- Source compile/test harus PASS.
- Windows packaging harus PASS.
- Branding/icon verification harus PASS.
- Visual smoke test pada Windows tetap menjadi validasi akhir sebelum merge/release production.
