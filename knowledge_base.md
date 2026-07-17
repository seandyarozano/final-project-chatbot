# Kenapa Jawaban Chatbot Kurang Valid, dan Cara Memperbaikinya

## 1. Faktor yang mempengaruhi validitas jawaban

Chatbot ini (sebelum perubahan di panduan ini) hanya punya **dua sumber pengetahuan**:

1. **Pengetahuan bawaan model Gemini** — hasil training Google, ada batas
   *knowledge cutoff*-nya sendiri (model tidak otomatis tahu kejadian/perubahan
   terbaru setelah tanggal cutoff tersebut).
2. **Teks yang saya tulis manual di `SYSTEM_PROMPT`** — ini statis, hanya seakurat
   riset yang saya lakukan saat menulisnya, dan tidak pernah berubah sendiri
   walau kenyataan di lapangan (biaya, jadwal, prodi) sudah berubah.

Tidak ada satu pun dari dua sumber itu yang otomatis "browsing" internet — makanya
kalau ditanya hal yang butuh info terbaru (jadwal PMB tahun ini, biaya kuliah
tahun ajaran berjalan), model bisa saja:
- Menjawab berdasarkan info lama yang ada di training data-nya (berpotensi salah/usang), atau
- **Berhalusinasi** — mengarang angka/tanggal yang terdengar masuk akal tapi sebenarnya tidak ada dasarnya

Faktor lain yang berpengaruh ke kualitas jawaban:
- **Pilihan model**: model "flash-lite" dioptimalkan untuk kecepatan & biaya rendah,
  bukan untuk reasoning/akurasi maksimal — ada trade-off.
- **Kualitas & kelengkapan system prompt**: makin detail & terstruktur instruksinya,
  makin kecil kemungkinan model mengarang.
- **Tidak ada verifikasi/citation**: model tidak menunjukkan dari mana info itu berasal,
  jadi pengguna (dan kita) tidak bisa langsung cek kebenarannya.

---

## 2. Perubahan yang sudah saya terapkan: Google Search Grounding

Saya sudah mengaktifkan fitur **Google Search grounding** bawaan Gemini di `app.py`.
Dengan ini, model bisa melakukan pencarian Google secara real-time sebelum menjawab,
lalu meracik jawaban dari hasil pencarian tersebut — bukan cuma mengandalkan
pengetahuan statis.

Perubahan kodenya:
```python
client = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

SEARCH_GROUNDING_ENABLED = True
if SEARCH_GROUNDING_ENABLED:
    client = client.bind_tools([{"google_search": {}}])
```

Saya juga menyesuaikan `SYSTEM_PROMPT` supaya bot tahu dia sekarang boleh mencari info
terkini, tapi tetap diminta jujur kalau hasil pencarian tidak jelas, dan tetap mengimbau
konfirmasi ulang ke website resmi untuk hal-hal penting (biaya, deadline).

**Catatan penting:**
- Fitur ini pakai kuota/biaya tersendiri dari Google (di luar biaya token biasa) —
  cek [halaman pricing Gemini API](https://ai.google.dev/gemini-api/docs/pricing) kalau
  ingin tahu detailnya, terutama kalau app sudah dipakai banyak orang.
- Grounding search membantu, tapi **bukan jaminan 100% akurat** — hasil pencarian bisa
  saja mengambil dari sumber yang tidak resmi/tidak terbaru. Karena itu instruksi di
  system prompt tetap meminta bot mengarahkan ke sumber resmi untuk keputusan penting.

---

## 3. Opsi lain untuk meningkatkan akurasi & kekinian data

Kalau proyek ini mau dikembangkan lebih jauh (misalnya untuk dipakai sungguhan oleh
kampus), ada beberapa tingkatan solusi, dari yang paling sederhana ke paling canggih:

### A. Update manual `SYSTEM_PROMPT` secara berkala (paling sederhana)
Cocok untuk info yang jarang berubah (sejarah, visi-misi, alamat kampus). Cukup buka
`app.py`, edit teks di `SYSTEM_PROMPT`, lalu deploy ulang. Sarankan jadwalkan review
tiap awal semester/tahun ajaran.

### B. Google Search Grounding (sudah diterapkan)
Lihat bagian 2 di atas — solusi paling praktis untuk data yang sering berubah tanpa
perlu infrastruktur tambahan.

### C. RAG (Retrieval-Augmented Generation) — level lanjut
Ini pendekatan paling akurat untuk chatbot institusi resmi:
1. Kumpulkan/scrape halaman resmi Tel-U Jakarta (jadwal PMB, biaya, daftar prodi, dll)
   secara berkala (mis. terjadwal tiap minggu).
2. Simpan teksnya ke *vector database* (mis. ChromaDB, FAISS, atau Pinecone).
3. Setiap ada pertanyaan dari user, sistem mencari potongan teks paling relevan dari
   database itu (*retrieval*), lalu menyisipkannya sebagai konteks tambahan ke prompt
   sebelum dikirim ke model.
4. Hasilnya: jawaban model benar-benar didasarkan pada dokumen resmi terbaru yang kita
   kontrol sendiri, bukan hasil pencarian umum atau ingatan model.

Ini butuh effort development lebih besar (di luar cakupan proyek akhir pelatihan
sederhana ini), tapi cocok jadi bahan pengembangan lanjutan kalau tertarik.

### D. Kombinasi B + C
Idealnya: RAG untuk data resmi kampus yang kita kontrol penuh (paling akurat), + Google
Search grounding sebagai pelengkap untuk pertanyaan umum di luar cakupan data RAG.

---

## 4. Bisakah upgrade model? Ya — tinggal ganti nama model

Model Gemini yang dipakai ditentukan lewat satu baris ini:
```python
client = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")
```

Ganti `"gemini-3.1-flash-lite"` dengan nama model lain sesuai kebutuhan. Per
pengecekan terbaru saya, beberapa opsi Gemini yang tersedia:

| Model | Karakteristik | Cocok untuk |
|---|---|---|
| `gemini-3.1-flash-lite` (yang dipakai sekarang) | Paling cepat & murah, reasoning standar | Chatbot volume tinggi, tugas sederhana seperti sekarang |
| `gemini-3.5-flash` | Reasoning jauh lebih baik, tetap harga wajar | Kalau butuh jawaban lebih pintar tanpa biaya setinggi model Pro |
| `gemini-3-pro` | Paling capable, reasoning kompleks, biaya paling tinggi | Kasus yang butuh analisis mendalam, bukan sekadar tanya-jawab info kampus |

**Penting:** upgrade model **tidak otomatis membuat data lebih update** — kalau tidak
dikombinasikan dengan grounding/RAG di atas, model yang lebih pintar pun tetap bisa
menjawab dengan info lama kalau tidak dikasih akses ke data terkini. Upgrade model lebih
berpengaruh ke kualitas *pemahaman & penalaran* bahasa, bukan ke kekinian faktanya.

Untuk proyek akhir pelatihan skala kecil seperti ini, kombinasi **model flash-lite +
Google Search grounding** (yang sudah diterapkan) sudah cukup seimbang antara biaya,
kecepatan, dan validitas jawaban.
