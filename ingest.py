"""Pipeline de ingestão: PDFs/HTML → chunks → embeddings BGE-M3 → Chroma."""
from pathlib import Path
import shutil

import pdfplumber
from bs4 import BeautifulSoup
from tqdm import tqdm
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

import config


def parse_pdf(path: Path) -> str:
    text_parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            t = page.extract_text() or ""
            if t.strip():
                text_parts.append(t)
    return "\n\n".join(text_parts)


def parse_html(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(raw, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)


def load_documents(raw_dir: Path) -> list[Document]:
    docs: list[Document] = []
    extensions = ("*.pdf", "*.html", "*.htm", "*.txt", "*.md")
    files = sorted({f for ext in extensions for f in raw_dir.rglob(ext)})
    print(f"[ingest] {len(files)} arquivos encontrados em {raw_dir}")
    for f in tqdm(files, desc="Lendo documentos"):
        try:
            if f.suffix.lower() == ".pdf":
                text = parse_pdf(f)
            elif f.suffix.lower() in (".html", ".htm"):
                text = parse_html(f)
            else:
                text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"[ingest] erro em {f.name}: {e}")
            continue

        if not text.strip():
            print(f"[ingest] vazio: {f.name}")
            continue

        rel = f.relative_to(raw_dir)
        source_label = str(rel).replace("\\", "/")
        docs.append(Document(
            page_content=text,
            metadata={"source": source_label, "filename": f.name, "category": rel.parts[0] if len(rel.parts) > 1 else "outros"},
        ))
    return docs


def chunk_documents(docs: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=config.PT_BR_SEPARATORS,
    )
    chunks = splitter.split_documents(docs)
    print(f"[ingest] {len(docs)} documentos -> {len(chunks)} chunks")
    return chunks


def build_vectorstore(chunks: list[Document], reset: bool = True) -> Chroma:
    if reset and config.DATA_CHROMA.exists():
        print(f"[ingest] limpando Chroma em {config.DATA_CHROMA}")
        shutil.rmtree(config.DATA_CHROMA)
    config.DATA_CHROMA.mkdir(parents=True, exist_ok=True)

    print(f"[ingest] carregando embeddings {config.EMBEDDING_MODEL}...")
    embeddings = HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL,
        model_kwargs={"device": config.EMBEDDING_DEVICE},
        encode_kwargs={"normalize_embeddings": True},
    )

    print(f"[ingest] indexando {len(chunks)} chunks no Chroma...")
    vs = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=config.COLLECTION_NAME,
        persist_directory=str(config.DATA_CHROMA),
    )
    print(f"[ingest] OK. Vectorstore em {config.DATA_CHROMA}")
    return vs


def main():
    print(f"[ingest] data/raw = {config.DATA_RAW}")
    docs = load_documents(config.DATA_RAW)
    if not docs:
        print("[ingest] nenhum documento lido. Coloque PDFs/HTML em data/raw/ antes de rodar.")
        return
    chunks = chunk_documents(docs)
    build_vectorstore(chunks, reset=True)


if __name__ == "__main__":
    main()
