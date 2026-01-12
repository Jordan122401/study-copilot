from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    pdf_dir: Path
    index_dir: Path
    embed_model: str
    chunk_size: int
    chunk_overlap: int
    top_k: int

    @property
    def pages_path(self) -> Path:
        return self.index_dir / "pages.jsonl"

    @property
    def chunks_path(self) -> Path:
        return self.index_dir / "chunks.jsonl"

    @property
    def faiss_path(self) -> Path:
        return self.index_dir / "faiss.index"

    @property
    def meta_path(self) -> Path:
        return self.index_dir / "meta.jsonl"


def load_config() -> Config:
    load_dotenv()  # loads .env if present

    pdf_dir = Path(os.getenv("PDF_DIR", "data/pdfs")).resolve()
    index_dir = Path(os.getenv("INDEX_DIR", "data/index")).resolve()

    embed_model = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    chunk_size = int(os.getenv("CHUNK_SIZE", "800"))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "150"))
    top_k = int(os.getenv("TOP_K", "5"))

    index_dir.mkdir(parents=True, exist_ok=True)

    return Config(
        pdf_dir=pdf_dir,
        index_dir=index_dir,
        embed_model=embed_model,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        top_k=top_k,
    )
