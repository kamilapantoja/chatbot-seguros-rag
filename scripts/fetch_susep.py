"""Baixa documentos públicos da SUSEP para a base de conhecimento."""
import sys
from pathlib import Path

import requests
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent.parent))
import config

# URLs públicas da SUSEP e materiais de educação financeira sobre seguros.
# Em caso de 404, o script só pula — o usuário pode complementar manualmente.
SOURCES = [
    # Cartilhas do consumidor
    ("https://www.gov.br/susep/pt-br/centrais-de-conteudo/publicacoes/livretos/seguros-um-guia-para-o-consumidor.pdf",
     "susep/cartilha_consumidor_seguros.pdf"),
    ("https://www.gov.br/susep/pt-br/centrais-de-conteudo/publicacoes/livretos/seguro-de-automovel-um-guia-para-o-consumidor.pdf",
     "susep/cartilha_seguro_automovel.pdf"),
    ("https://www.gov.br/susep/pt-br/centrais-de-conteudo/publicacoes/livretos/seguro-de-vida-um-guia-para-o-consumidor.pdf",
     "susep/cartilha_seguro_vida.pdf"),
    ("https://www.gov.br/susep/pt-br/centrais-de-conteudo/publicacoes/livretos/seguro-residencial-um-guia-para-o-consumidor.pdf",
     "susep/cartilha_seguro_residencial.pdf"),
    ("https://www.gov.br/susep/pt-br/centrais-de-conteudo/publicacoes/livretos/microsseguros-um-guia-para-o-consumidor.pdf",
     "susep/cartilha_microsseguros.pdf"),
]


def download(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        with requests.get(url, stream=True, timeout=30, headers={"User-Agent": "Mozilla/5.0"}) as r:
            if r.status_code != 200:
                print(f"[fetch] {r.status_code} -> {url}")
                return False
            total = int(r.headers.get("content-length", 0))
            with open(dest, "wb") as f, tqdm(total=total, unit="B", unit_scale=True, desc=dest.name) as bar:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    bar.update(len(chunk))
        return True
    except Exception as e:
        print(f"[fetch] erro em {url}: {e}")
        return False


def main():
    ok = 0
    for url, rel in SOURCES:
        dest = config.DATA_RAW / rel
        if dest.exists() and dest.stat().st_size > 0:
            print(f"[fetch] ja existe: {rel}")
            ok += 1
            continue
        if download(url, dest):
            ok += 1
    print(f"\n[fetch] {ok}/{len(SOURCES)} baixados em {config.DATA_RAW}")


if __name__ == "__main__":
    main()
