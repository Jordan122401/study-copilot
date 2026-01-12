import json
from pathlib import Path
import hashlib

import fitz  # PyMuPDF
from tqdm import tqdm


def _doc_id_for_file(path: Path) -> str:
    h = hashlib.sha1()
    h.update(str(path.resolve()).encode("utf-8"))
    h.update(str(path.stat().st_mtime_ns).encode("utf-8"))
    return h.hexdigest()[:12]


def ingest_pdfs_to_pages_jsonl(pdf_dir: Path, out_pages_jsonl: Path) -> int:
    pdfs = sorted([p for p in pdf_dir.glob("*.pdf") if p.is_file()])
    if not pdfs:
        raise FileNotFoundError(f"No PDFs found in: {pdf_dir}")

    out_pages_jsonl.parent.mkdir(parents=True, exist_ok=True)

    count_pages = 0
    with out_pages_jsonl.open("w", encoding="utf-8") as f:
        for pdf_path in tqdm(pdfs, desc="Ingesting PDFs"):
            doc_id = _doc_id_for_file(pdf_path)

            doc = fitz.open(pdf_path)
            try:
                for i in range(doc.page_count):
                    page = doc.load_page(i)
                    text = page.get_text("text") or ""
                    text = " ".join(text.split())  # collapse whitespace

                    rec = {
                        "doc_id": doc_id,
                        "file": pdf_path.name,
                        "path": str(pdf_path.resolve()),
                        "page": i + 1,  # 1-based pages
                        "text": text,
                    }
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    count_pages += 1
            finally:
                doc.close()

    return count_pages
