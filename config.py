"""Configurações centralizadas do chatbot Dracarys."""
from pathlib import Path
import os

ROOT = Path(__file__).parent
DATA_RAW = ROOT / "data" / "raw"
DATA_CHROMA = ROOT / "data" / "chroma"

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11435")
LLM_MODEL = os.getenv("LLM_MODEL", "gemma2:27b")
LLM_TEMPERATURE = 0.2
LLM_NUM_CTX = 8192

EMBEDDING_MODEL = "BAAI/bge-m3"
EMBEDDING_DEVICE = "cpu"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
PT_BR_SEPARATORS = ["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " ", ""]

RETRIEVAL_TOP_K = 6
COLLECTION_NAME = "dracarys-seguros"
