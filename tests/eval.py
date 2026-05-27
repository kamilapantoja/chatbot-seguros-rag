"""Script de avaliação manual: roda as 20 perguntas e salva respostas em markdown."""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from rag import RAGChain


def main():
    questions_path = Path(__file__).parent / "eval_questions.json"
    output_path = Path(__file__).parent / "eval_results.md"
    questions = json.loads(questions_path.read_text(encoding="utf-8"))
    chain = RAGChain()

    lines = ["# Avaliação Manual — Chatbot Dracarys\n"]
    for q in questions:
        print(f"\n[{q['id']}/{len(questions)}] ({q['categoria']}) {q['pergunta']}")
        t0 = time.time()
        try:
            result = chain.answer(q["pergunta"])
            elapsed = time.time() - t0
            answer = result["answer"]
            sources = result["sources"]
        except Exception as e:
            elapsed = time.time() - t0
            answer = f"ERRO: {e}"
            sources = []
        print(f"  -> {elapsed:.1f}s, {len(sources)} fontes")

        lines.append(f"## {q['id']}. [{q['categoria']}] {q['pergunta']}\n")
        lines.append(f"**Resposta** ({elapsed:.1f}s):\n\n{answer}\n")
        if sources:
            uniq = []
            for s in sources:
                if s not in uniq:
                    uniq.append(s)
            lines.append("**Fontes:** " + ", ".join(f"`{s}`" for s in uniq) + "\n")
        lines.append("\n---\n")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nResultados em {output_path}")


if __name__ == "__main__":
    main()
