# UB-SR-5-MENTOR — Mentor Service

Service backend FastAPI untuk fitur mentor AI Sekolah Rakyat Tim 5.
Service ini menerima request dari backend utama (MVP BE) dan meneruskannya ke LLM endpoint Tim 5 dengan system prompt yang sesuai.

---

## Arsitektur

```
Backend Utama (MVP BE)
        │
        │ HTTP POST
        ▼
Mentor Service (repo ini) ── port 8004
        │
        │ HTTP POST (OpenAI-compatible)
        ▼
LLM Endpoint Tim 5
```

---

## Cara Kerja CI/CD

Setiap kali ada **push ke branch `main`**, GitHub Actions otomatis:

1. **Build** — Docker image di-build dan di-push ke GitHub Container Registry (GHCR)
2. **Deploy** — Image terbaru di-pull ke VPS dan container di-restart otomatis

Jadi tim 5 tidak perlu SSH ke VPS secara manual. Cukup:

```
push ke main → tunggu deploy selesai → perubahan live di VPS
```

Status CI/CD bisa dipantau di tab **Actions** di GitHub repo ini.

---

## Struktur Project

```
ub-sr-5-mentor/
├── .github/
│   └── workflows/
│       └── backend.yml        # CI/CD pipeline
├── routers/
│   ├── __init__.py            # Router aggregator (prefix /mentor_api)
│   ├── mentor_chat.py         # Endpoint POST /mentor_api/chat
│   ├── mentor_pilgan_evaluasi.py  # Endpoint POST /mentor_api/pilihan_ganda
│   └── mentor_essay_evaluasi.py   # Endpoint POST /mentor_api/essay
├── src/
│   └── mentor_service.py      # Logic call ke LLM endpoint
├── core/
│   └── config.py              # Konfigurasi environment variables
├── system_prompts/            # <== AREA KERJA TIM 5
│   └── prompts.py             # Tulis system prompt di sini
├── schemas/
│   └── mentor.py              # Pydantic schema request/response
├── main.py
├── pyproject.toml
├── uv.lock
├── Dockerfile
├── docker-compose.yml         # Untuk run lokal
├── docker-compose.deploy.yml  # Untuk deploy VPS
├── .env.example               # Template environment variables
└── README.md
```

---

## Kontribusi Tim 5 — Fokus di Sini

### File yang perlu diisi

**`system_prompts/prompts.py`** — ini satu-satunya file yang perlu diubah tim 5:

```python
def system_prompt_chat(payload: dict) -> str:
    # Tulis system prompt untuk chat response di sini
    # Gunakan payload untuk konteks siswa
    return ""

def system_prompt_pilgan(payload: dict) -> str:
    # Tulis system prompt untuk evaluasi pilihan ganda di sini
    return ""

def system_prompt_essay(payload: dict) -> str:
    # Tulis system prompt untuk evaluasi essay di sini
    return ""
```

Setelah selesai, panggil di `src/mentor_service.py`:

```python
from system_prompts.prompts import system_prompt_chat

async def chat_response(self, chat_messages: list, payload: dict):
    system_prompt = system_prompt_chat(payload)  # ganti string kosong ini
    return await self._call_llm(system_prompt, chat_messages)
```

---

## Endpoint

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/` | Health check |
| POST | `/mentor_api/chat` | Chat response mentor |
| POST | `/mentor_api/pilihan_ganda` | Evaluasi jawaban pilihan ganda |
| POST | `/mentor_api/essay` | Evaluasi jawaban essay |

Dokumentasi interaktif tersedia di `/docs` setelah service berjalan.

---

## Request Payload

Salah satu contoh *payload* di mode chat:

```json
{
  "chat_messages": [
    {
      "role": "user",
      "content": "Sebutkan fenomena fenomena pada sosiologi"
    },
    {
      "role": "assistant",
      "content": "Sosiologi mempelajari berbagai fenomena sosial..."
    },
    {
      "role": "user",
      "content": "jelaskan lebih lanjut"
    }
  ],
  "payload": {
    "siswa_id": "84154072-9fa6-4b2e-8238-61dad4a5d46b",
    "sesi_id": "93c05233-4fbf-44a3-b228-6c40e0818e9b",
    "mapel_id": "4",
    "elemen_id": "10",
    "elemen_label": "Pemahaman Konsep",
    "materi": "Ilmu Pengetahuan Sosial",
    "materi_id": "75",
    "atp": [
      "Peserta didik memahami sosiologi sebagai ilmu yang mengkaji masyarakat secara kritis, analitis, kreatif, dan solutif.",
      "Peserta didik mampu membedakan pendekatan kualitatif, kuantitatif, dan campuran dalam penelitian sosial."
    ],
    "level": "Low",
    "message": "jelaskan lebih lanjut",
    "context": {
      "emosi": "antusias",
      "progress": null,
      "publish_id": "127",
      "content_bundle_id": "127",
      "bundle_id": "127",
      "bacaan": "### Memahami Fenomena Sosial...(isi bacaan)"
    },
    "mentorMode": "materi"
  }
}
```

### Keterangan field `payload`

| Field | Tipe | Keterangan |
|-------|------|-----------|
| `siswa_id` | string | UUID siswa |
| `sesi_id` | string | UUID sesi belajar |
| `mapel_id` | string | ID mata pelajaran |
| `elemen_id` | string | ID elemen kompetensi |
| `elemen_label` | string | Label elemen (misal: "Pemahaman Konsep") |
| `materi` | string | Nama mata pelajaran |
| `materi_id` | string | ID materi |
| `atp` | list[string] | Alur Tujuan Pembelajaran |
| `level` | string | Level siswa: `"Low"`, `"Medium"`, `"High"` |
| `message` | string | Pesan terakhir siswa |
| `context.emosi` | string | Emosi siswa saat ini |
| `context.bacaan` | string | Konten bacaan/materi dalam markdown |
| `mentorMode` | string | Mode mentor: `"materi"`, dll |

---

## Setup Lokal

### Prerequisites
- Python 3.13
- Docker & Docker Compose
- uv (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Run dengan Docker

```bash
# Clone repo
git clone https://github.com/<org>/ub-sr-5-mentor.git
cd ub-sr-5-mentor

# Buat .env dari template
cp .env.example .env
# Edit .env sesuai konfigurasi

# Build dan run
docker compose up --build
```

### Run tanpa Docker

```bash
# Install dependencies
uv sync

# Jalankan service
uv run uvicorn main:app --reload --port 8004
```

Akses dokumentasi di `http://localhost:8004/docs`

---

## Environment Variables

Buat file `.env` dari template:

```bash
cp .env.example .env
```

Isi file `.env`:

```env
MENTOR_LLM_ENDPOINT=https://llm-endpoint-tim5.example.com/v1/chat/completions
MENTOR_LLM_MODEL=nama-model-tim5
```

---

## Setup GitHub Secrets (untuk Admin Repo)

Secrets dibutuhkan agar CI/CD bisa deploy ke VPS. Hanya admin repo yang bisa mengisi ini.

### Langkah-langkah

1. Buka repo di GitHub
2. Klik **Settings** → **Secrets and variables** → **Actions**
3. Klik **New repository secret**
4. Tambahkan secret berikut:

| Secret Name | Isi |
|-------------|-----|
| `ENV_FILE` | Seluruh isi file `.env` production (copy-paste isi filenya, bukan path-nya) |

### Contoh isi `ENV_FILE`

```
MENTOR_LLM_ENDPOINT=https://llm-endpoint-tim5.example.com/v1/chat/completions
MENTOR_LLM_MODEL=nama-model-tim5
```

> ⚠️ Jangan pernah commit file `.env` ke repository. File ini sudah ada di `.gitignore`.

---

## Alur Kerja Tim 5

```
1. Clone repo
2. Buat branch baru untuk eksperimen system prompt
3. Edit system_prompts/prompts.py
4. Test lokal dengan docker compose up --build
5. Kalau sudah oke, buat Pull Request ke main
6. Setelah di-merge, CI/CD otomatis deploy ke VPS
```

---

## Kontak

Untuk pertanyaan teknis terkait infrastruktur dan CI/CD, hubungi TIM MVP. 