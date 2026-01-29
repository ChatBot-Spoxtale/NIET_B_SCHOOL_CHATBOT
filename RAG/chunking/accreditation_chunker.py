import json
from pathlib import Path
from typing import List, Dict


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "accreditation_page.json"
OUTPUT_PATH = BASE_DIR / "data_chunk" / "accreditation_chunks.json"

def chunk_accreditation_page(data: dict):
    """
    Convert accreditation page JSON into RAG chunks
    Format: id, question, answer, keywords
    """
    chunks = []

    page_type = data.get("page_type", "accreditations_page")
    accreditations = data.get("data", {}).get("accreditations", [])

    for idx, acc in enumerate(accreditations):
        code = acc.get("code", "").strip()
        title = acc.get("title", "").strip()
        description = acc.get("description", "").strip()

        chunk = {
            "id": f"{page_type}_{idx}",
            "question": f"What is {title} accreditation at NIET Business School?",
            "answer": f"{title} ({code}) means {description}.",
            "keywords": [
                "NIET",
                "NIET Business School",
                "accreditation",
                code,
                title,
                description.lower()
            ]
        }

        chunks.append(chunk)

    return chunks

def save_chunks():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = chunk_accreditation_page(data)

    OUTPUT_PATH.parent.mkdir(exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"Program chunks saved ({len(chunks)})")

if __name__ == "__main__":
    save_chunks()    