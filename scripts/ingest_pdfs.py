from pathlib import Path
import sys

# Allow imports from src/ without installing package
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from study_copilot.config import load_config
from study_copilot.ingest import ingest_pdfs_to_pages_jsonl


if __name__ == "__main__":
    cfg = load_config()
    n = ingest_pdfs_to_pages_jsonl(cfg.pdf_dir, cfg.pages_path)
    print(f"✅ Ingested pages: {n}")
    print(f"   -> {cfg.pages_path}")
