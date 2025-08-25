# 🚀 AI Chatbot Customer Support

Solusi chatbot AI untuk customer support toko online yang dibangun untuk memenuhi challenge technical test dari PT Synapsis Sinergi Digital.

## 📋 Fitur Utama

- ✅ Menangani 3 jenis pertanyaan pengguna (status pesanan, informasi produk, kebijakan garansi)
- ✅ Memori percakapan (3 interaksi terakhir)
- ✅ Penyimpanan history percakapan di SQLite database
- ✅ Tool calling untuk mendapatkan status pesanan
- ✅ Model LLM lokal dengan Ollama (llama3.2:3b)
- ✅ REST API sederhana dengan FastAPI
- ✅ Docker containerization lengkap

## 🛠️ Teknologi yang Digunakan

### Backend Framework
- **Python 3.11** - Bahasa pemrograman utama
- **FastAPI** - Web framework modern dan cepat
- **SQLAlchemy** - ORM untuk database operations
- **Pydantic** - Data validation dan settings management

### AI & Machine Learning
- **Ollama** - Platform untuk menjalankan model LLM lokal
- **Llama3.2:3b** - Large Language Model untuk pemrosesan bahasa alami

### Database
- **SQLite** - Database relational untuk penyimpanan data
- **SQLAlchemy ORM** - Object-Relational Mapping

### Deployment & Containerization
- **Docker** - Containerization platform
- **Docker Compose** - Multi-container application management

## 🗃️ Desain Database

### Schema Diagram
user_data
├── id (PK)
├── name
└── email

produk
├── id (PK)
├── sku (UNIQUE)
├── nama
└── deskripsi

order_data
├── id (PK)
├── order_number (UNIQUE)
├── user_id (FK → user_data.id)
├── produk_id (FK → produk.id)
├── status
└── created_at

session_chat
├── id (PK)
├── session_id (INDEX)
├── user_id (FK → user_data.id)
└── created_at

msg_log
├── id (PK)
├── session_id (FK → session_chat.id)
├── role (user/assistant)
├── content
└── created_at


### Relationship
- One-to-Many: `user_data` → `order_data`
- One-to-Many: `produk` → `order_data`
- One-to-Many: `session_chat` → `msg_log`
- One-to-Many: `user_data` → `session_chat`

## 📦 Instalasi & Setup

### Prerequisites
- Docker dan Docker Compose
- Git
- Minimal 4GB RAM (untuk menjalankan Llama3.2:3b)

### Langkah-langkah Instalasi

1. **Clone repository**
   ```bash
   git clone <your-repo-url>
   cd jr-ai-challenge
   
2. Jalankan aplikasi dengan Docker Compose
    ```bash
    docker-compose up -d
   
3. Pull model Llama3.2:3b (setelah container Ollama running)
    ```bash
    docker exec -it ollama-server ollama pull llama3.2:3b
    
4. Inisialisasi database dengan data sample
    ```bash
    docker exec jr-ai-chatbot python seed_db.py
    
5. Verifikasi aplikasi berjalan
    ```bash
    curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test1","user_id":1,"message":"Cek status pesanan ORD001"}'
  
  
🔌 API Documentation
Base URL
http://localhost:8000

Endpoints
POST /chat
Mengirim pesan ke chatbot dan mendapatkan respons

Request Body:
```json
{
  "session_id": "string",
  "user_id": 1,
  "message": "string"
}

Response:
```json
{
  "reply": "string"
}

Contoh Usage:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session-123",
    "user_id": 1,
    "message": "Cek status pesanan ORD001"
  }'


❓ Pertanyaan yang Dapat Dijawab
1. Status Pesanan
"Dimana pesanan saya?"
"Cek status pesanan ORD001"
"Kapan pesanan saya dikirim?"
"Status order ORD001"
"Pesanan saya sampai mana?"

2. Informasi Produk
"Apa kelebihan Kopi Arabika?"
"Deskripsi produk SKU-001"
"Apa saja produk yang tersedia?"
"Ceritakan tentang Kopi Arabika"
"Spesifikasi produk SKU-001"

3. Kebijakan Garansi
"Bagaimana cara claim garansi?"
"Syarat dan ketentuan garansi"
"Lama waktu garansi"
"Cara klaim garansi produk"
"Ketentuan garansi toko"


🛠️ Tool Calling Capabilities
Chatbot mendukung tool calling untuk operasi khusus:

get_order_status
Mendapatkan status pesanan berdasarkan nomor order

Format Tool Call:
```json
{
  "tool": "get_order_status",
  "order_number": "ORD001"
}

Contoh Response:
```json
{
  "found": true,
  "status": "Diproses"
}

📁 Project Structure
jr-ai-challenge/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application dan endpoint
│   ├── models.py               # SQLAlchemy database models
│   ├── db_setup.py            # Database configuration dan setup
│   └── ollama_wrap.py         # Ollama client wrapper
├── schema.sql                 # SQL schema definition
├── requirements.txt           # Python dependencies
├── Dockerfile                # Docker configuration untuk chatbot
├── docker-compose.yml        # Docker compose setup
├── seed_db.py               # Database initializer (root level)
└── README.md                # Documentation


🐛 Troubleshooting
1. Model Tidak Ditemukan
```bash
# Cek model yang tersedia
docker exec ollama-server ollama list
# Pull model manual
docker exec -it ollama-server ollama pull llama3.2:3b


2. Database Error
```bash
# Re-inisialisasi database
docker exec jr-ai-chatbot python seed_db.py

3. Port Sudah Digunakan
Pastikan port 8000 dan 11434 tidak digunakan aplikasi lain
atau ubah port di file docker-compose.yml

4. Container Tidak Berjalan
```bash
# Cek status container
docker-compose ps
# Restart container
docker-compose restart
# Lihat logs
docker-compose logs ollama
docker-compose logs chatbot

🚀 Deployment Notes
Environment Variables
OLLAMA_HOST - URL Ollama server (default: http://ollama:11434)

Performance Considerations
Model Llama3.2:3b membutuhkan minimal 4GB RAM

Response time tergantung spesifikasi hardware

Untuk production, consider menggunakan model yang lebih optimized

👨‍💻 Developer Information
Dibangun oleh Siti Auliaddina untuk memenuhi technical challenge PT Synapsis Sinergi Digital.