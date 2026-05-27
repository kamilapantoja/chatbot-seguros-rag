"""Empacota o desafio-2 em ZIP pronto pra enviar, excluindo venv/cache/logs."""
import sys
import zipfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
ZIP_NAME = "Desafio2_Dracarys_KamilaPantoja.zip"

EXCLUDE_DIRS = {".venv", "__pycache__", ".chainlit", ".files"}
EXCLUDE_DATA_SUBDIRS = {"chroma"}
EXCLUDE_EXTENSIONS = {".log", ".pyc"}
EXCLUDE_FILES = {".pip-install.log", ".ingest.log"}


def should_skip(rel_parts: tuple[str, ...], name: str, suffix: str) -> bool:
    if any(part in EXCLUDE_DIRS for part in rel_parts):
        return True
    if len(rel_parts) >= 2 and rel_parts[0] == "data" and rel_parts[1] in EXCLUDE_DATA_SUBDIRS:
        return True
    if name in EXCLUDE_FILES:
        return True
    if suffix in EXCLUDE_EXTENSIONS:
        return True
    return False


def main():
    zip_path = PROJECT / ZIP_NAME
    if zip_path.exists():
        zip_path.unlink()

    included = 0
    skipped = 0
    renamed = 0
    total_bytes = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for f in PROJECT.rglob("*"):
            if not f.is_file():
                continue
            if f == zip_path:
                continue
            rel = f.relative_to(PROJECT)
            if should_skip(rel.parts, f.name, f.suffix.lower()):
                skipped += 1
                continue
            arcname = Path("desafio-2") / rel
            # Gmail bloqueia .bat dentro de zip. Renomeia para .bat.txt
            # (o professor renomeia de volta para executar, ou apenas le o conteudo).
            if f.suffix.lower() == ".bat":
                arcname = arcname.with_suffix(".bat.txt")
                renamed += 1
            zf.write(f, arcname.as_posix())
            included += 1
            total_bytes += f.stat().st_size

    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"[zip] OK")
    print(f"[zip] arquivos incluidos: {included}")
    print(f"[zip] renomeados .bat -> .bat.txt: {renamed}")
    print(f"[zip] arquivos ignorados: {skipped}")
    print(f"[zip] tamanho descomprimido: {total_bytes / (1024*1024):.1f} MB")
    print(f"[zip] tamanho final: {size_mb:.1f} MB")
    print(f"[zip] saida: {zip_path}")


if __name__ == "__main__":
    main()
