
# Terabox API — Vercel-ready (Full Pack)

API siap deploy ke **Vercel**, dengan:
- Endpoint **GET/POST** `/api/dl`
- Multi-backend **fallback** (bisa diatur via ENV `BACKENDS`)
- Endpoint `/api/info` untuk debug (raw upstream)
- Contoh **bot Telegram** (folder `bot`) yang memanggil endpoint ini
- Utilitas normalisasi URL share (auto tambah `pwd` bila diberikan)

## Deploy ke Vercel
1. Buat project baru di Vercel → import repo ZIP ini (atau push ke GitHub lalu import).
2. Konfirmasi framework: **Other**; config default.
3. (Opsional) Set **Environment Variable** `BACKENDS` jika ingin menambah/mengganti daftar upstream, pisahkan dengan koma.
4. Deploy.

### Endpoint
- **GET**  `/api/dl?url=<share_url>[&pwd=XXXX]`
- **POST** `/api/dl` body: `{"url":"<share_url>", "pwd":"XXXX"}` *(pwd opsional)*
- **GET**  `/api/info?url=<share_url>` → raw dari upstream untuk diagnosa
- **GET**  `/api/health`

**Respons (contoh ringkas):**
```json
{
  "ok": true,
  "filename": "video.mp4",
  "size": "123 MB",
  "download_url": "https://...",
  "streaming_url": "https://...",
  "original_download_url": "https://...",
  "via": "https://<backend-used>"
}
```

> Catatan:
> - Jika share link memakai **extract code (password)**, Anda bisa mengirimnya lewat query `pwd` atau field JSON `pwd`. Library akan menambahkan ke URL jika belum ada.
> - Endpoint default menggunakan backend Cloudflare Worker publik yang saat dibuat masih live.
> - Anda bisa menambahkan backend lain via ENV `BACKENDS` (format sama: endpoint yang menerima `?url=` dan memberi `{success, files[]}`).
> - Untuk mengganti ke **resolver internal** (tanpa upstream), ganti isi `resolve_via_worker()` di `app/backends.py` dengan logika Anda.

## Bot Telegram (contoh)
Di folder `bot/` ada `bot_example.py` (minimal). Jalankan di Termux/server dengan env:
```bash
export API_BASE="https://<project>.vercel.app"
export BOT_TOKEN="123456:ABC-DEF..."
python bot/bot_example.py
```

## Pengembangan lokal
Anda bisa menjalankan lokal dengan Uvicorn untuk uji:
```bash
pip install -r requirements.txt
uvicorn api.index:app --reload --port 8000
```

Lalu akses:
```
http://127.0.0.1:8000/api/health
http://127.0.0.1:8000/api/dl?url=https://www.terabox.com/s/XXXX
```

## Lisensi
MIT
