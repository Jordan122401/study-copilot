from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from study_copilot.config import load_config
from study_copilot.search import search_with_citations


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('Usage: python scripts\\ask.py "your question"')

    query = " ".join(sys.argv[1:])
    cfg = load_config()

    results = search_with_citations(
        query=query,
        faiss_index_path=cfg.faiss_path,
        meta_jsonl_path=cfg.meta_path,
        embed_model_name=cfg.embed_model,
        top_k=cfg.top_k,
    )

    print(f"\nQ: {query}\n")
    if not results:
        print("No results found. (Did you build the index?)")
        raise SystemExit(0)

    print("Top evidence:\n")
    for i, r in enumerate(results, 1):
        print(f"{i}) {r['file']} (p. {r['page']})  score={r['score']:.3f}")
        print(f"   {r['snippet']}\n")
