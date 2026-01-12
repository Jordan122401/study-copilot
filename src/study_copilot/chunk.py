import json
from pathlib import Path
import hashlib
from typing import Iterable, Dict, List


def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    # Simple character-based chunker (good enough for MVP)
    text = text.strip()
    if not text:
        return []

    if overlap >= chunk_size:
        overlap = max(0, chunk_size // 5)

    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(n, start + chunk_size)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == n:
            break
        start = max(0, end - overlap)

    return chunks


def pages_jsonl_to_chunks_jsonl(pages_jsonl: Path, out_chunks_jsonl: Path, chunk_size: int, overlap: int) -> int:
    if not pages_jsonl.exists():
        raise FileNotFoundError(f"Missing pages file: {pages_jsonl}")

    out_chunks_jsonl.parent.mkdir(parents=True, exist_ok=True)

    count_chunks = 0
    with pages_jsonl.open("r", encoding="utf-8") as fin, out_chunks_jsonl.open("w", encoding="utf-8") as fout:
        for line in fin:
            rec = json.loads(line)
            text = rec.get("text", "") or ""
            pieces = chunk_text(text, chunk_size=chunk_size, overlap=overlap)

            for idx, piece in enumerate(pieces):
                # stable-ish chunk id
                h = hashlib.sha1()
                h.update((rec["doc_id"] + rec["file"] + str(rec["page"]) + str(idx)).encode("utf-8"))
                chunk_id = h.hexdigest()[:16]

                out = {
                    "chunk_id": chunk_id,
                    "doc_id": rec["doc_id"],
                    "file": rec["file"],
                    "path": rec["path"],
                    "page": rec["page"],
                    "text": piece,
                }
                fout.write(json.dumps(out, ensure_ascii=False) + "\n")
                count_chunks += 1

    return count_chunks
