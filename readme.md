# CryptX – CLI Sederhana untuk Enkripsi & Dekripsi

**CipherBox** adalah tool Command Line Interface (CLI) sederhana untuk melakukan enkripsi dan dekripsi menggunakan **AES**, **Base64**, dan **XOR**.

---

## 📦 Instalasi

### **1️⃣ Buat Virtual Environment (Disarankan)**

Windows:
```bash
python -m venv .venv
```

Linux/macOS:
```bash
python3 -m venv .venv
```

---

### ** Aktifkan Virtual Environment**

Windows (PowerShell):
```bash
.\.venv\Scripts\activate
```

Windows (Git Bash / MINGW64):
```bash
source .venv/Scripts/activate
```

Linux/macOS:
```bash
source .venv/bin/activate
```

Jika berhasil, akan muncul tanda:
```
(.venv)
```

---

### ** Install Package**

Mode pengembangan (editable):
```bash
pip install -e .
```

Atau instal biasa:
```bash
pip install .
```

Cek apakah CLI sudah terpasang:
```bash
cipherbox --help
```

---

## Penggunaan Dasar

Tampilkan bantuan utama:
```bash
cipherbox --help
```

---

# Perintah Enkripsi

## **AES Encryption**
Enkripsi teks:
```bash
cipherbox encrypt --method aes --text "Halo Dunia" --password PASSWORD_ANDA
```

Enkripsi file:
```bash
cipherbox encrypt --method aes --infile input.txt --outfile terenkripsi.bin --password PASSWORD_ANDA
```

---

## **Base64 Encoding**
Enkripsi (encoding) teks:
```bash
cipherbox encrypt --method base64 --text "Halo"
```

Encoding file:
```bash
cipherbox encrypt --method base64 --infile gambar.png --outfile encoded.txt
```

---

## **XOR Encryption**
Enkripsi teks:
```bash
cipherbox encrypt --method xor --text "Halo" --key 123
```

Enkripsi file:
```bash
cipherbox encrypt --method xor --infile input.bin --outfile output.bin --key 55
```

---

# Perintah Dekripsi

## **AES Decryption**
```bash
cipherbox decrypt --method aes --infile terenkripsi.bin --password PASSWORD_ANDA
```

---

## **Base64 Decoding**
```bash
cipherbox decrypt --method base64 --text "SGVsbG8="
```

---

## **XOR Decryption**
```bash
cipherbox decrypt --method xor --infile terenkripsi.bin --outfile hasil.txt --key 123
```

---

# Penjelasan Argumen

| Argumen        | Digunakan Untuk | Deskripsi |
|----------------|------------------|-----------|
| `--method`     | Semua            | Pilih metode (`aes`, `base64`, `xor`) |
| `--text`       | Opsional         | Input berupa teks |
| `--infile`     | Opsional         | Input file |
| `--outfile`    | Opsional         | Output file |
| `--password`   | AES              | Password untuk enkripsi AES |
| `--key`        | XOR              | Kunci XOR |

📝 Jika `--text` dan `--infile` dipakai bersamaan:  
➡️ **Yang digunakan adalah `--infile`.**

---

# Catatan Keamanan

- **AES aman**, cocok untuk data sensitif.  
- **Base64 bukan enkripsi**, hanya encoding.  
- **XOR hanya untuk pembelajaran**, tidak aman untuk data penting.

Gunakan password AES yang kuat.

---

# 🧑‍💻 Penulis
**Bima Rizki**  
Mahasiswa Teknik Informatika & Enthusiast Keamanan Siber