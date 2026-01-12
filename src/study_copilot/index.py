import json
from pathlib import Path
from typing import List, Dict

import numpy as np
import faiss

from .embed import load_embedder, embed_texts


def build_faiss_index_from_chunks(
    chunks_jsonl: Path,
    faiss_out: Path,
    meta_out: Path,
    embed_model_name: str,
) -> int:
    if not chunks_jsonl.exists():
        raise FileNotFoundError(f"Missing chunks file: {chunks_jsonl}")

    # Load chunk records
    metas: List[Dict] = []
    texts: List[str] = []
    with chunks_jsonl.open("r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            metas.append({
                "chunk_id": rec["chunk_id"],
                "doc_id": rec["doc_id"],
                "file": rec["file"],
                "path": rec["path"],
                "page": rec["page"],
                "text": rec["text"],
            })
            texts.append(rec["text"])

    if not texts:
        raise ValueError("No chunk text found to index.")

    model = load_embedder(embed_model_name)
    X = embed_texts(model, texts)

    dim = X.shape[1]
    index = faiss.IndexFlatIP(dim)  # cosine sim if vectors normalized
    index.add(X)

    faiss_out.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(faiss_out))

    with meta_out.open("w", encoding="utf-8") as f:
        for m in metas:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")

    return len(metas)
