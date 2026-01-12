from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from study_copilot.config import load_config
from study_copilot.chunk import pages_jsonl_to_chunks_jsonl
from study_copilot.index import build_faiss_index_from_chunks


if __name__ == "__main__":
    cfg = load_config()

    c = pages_jsonl_to_chunks_jsonl(cfg.pages_path, cfg.chunks_path, cfg.chunk_size, cfg.chunk_overlap)
    print(f"✅ Built chunks: {c}")
    print(f"   -> {cfg.chunks_path}")

    n = build_faiss_index_from_chunks(cfg.chunks_path, cfg.faiss_path, cfg.meta_path, cfg.embed_model)
    print(f"✅ Indexed chunks: {n}")
    print(f"   -> {cfg.faiss_path}")
    print(f"   -> {cfg.meta_path}")
