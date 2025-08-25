from ollama import Client
import os

def get_client():
    """
    ambil client ollama.
    - default ke localhost:11434
    - bisa override via env OLLAMA_HOST (penting buat Docker)
    """
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    # antisipasi user isi tanpa http
    if host and not host.startswith("http"):
        host = f"http://{host}"
    return Client(host=host)
