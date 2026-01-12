import json
from pathlib import Path
from typing import List, Dict, Tuple

import faiss
import numpy as np

from .embed import load_embedder, embed_texts


def load_meta(meta_jsonl: Path) -> List[Dict]:
    metas = []
    with meta_jsonl.open("r", encoding="utf-8") as f:
        for line in f:
            metas.append(json.loads(line))
    return metas


def search_with_citations(
    query: str,
    faiss_index_path: Path,
    meta_jsonl_path: Path,
    embed_model_name: str,
    top_k: int = 5,
) -> List[Dict]:
    if not faiss_index_path.exists():
        raise FileNotFoundError(f"Missing FAISS index: {faiss_index_path}")
    if not meta_jsonl_path.exists():
        raise FileNotFoundError(f"Missing metadata file: {meta_jsonl_path}")

    index = faiss.read_index(str(faiss_index_path))
    metas = load_meta(meta_jsonl_path)

    model = load_embedder(embed_model_name)
    qv = embed_texts(model, [query])  # shape (1, dim)

    scores, idxs = index.search(qv, top_k)
    scores = scores[0].tolist()
    idxs = idxs[0].tolist()

    results = []
    for score, i in zip(scores, idxs):
        if i == -1:
            continue
        m = metas[i]
        results.append({
            "score": float(score),
            "file": m["file"],
            "page": m["page"],
            "path": m["path"],
            "snippet": (m["text"][:300] + "…") if len(m["text"]) > 300 else m["text"],
        })

    return results
