import json
from pathlib import Path
from typing import List, Dict

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "peo_data.json"
OUTPUT_PATH = BASE_DIR / "data_chunk" / "peo_chunks.json"


def peo_chunker() -> List[Dict]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)

    peos = raw.get("data", {}).get("peos", [])
    source_url = raw.get("source_url", "")

    chunks = []

    for peo in peos:
        code = peo.get("code", "").strip()
        description = peo.get("description", "").strip()

        chunks.append({
            "id": f"peo_{code.lower()}",
            "category": "peo",
            "question": f"What is {code} of the program?",
            "answer": description,
            "keywords": [
                "peo",
                "program educational objectives",
                "objective",
                code.lower()
            ],
            "source_url": source_url
        })

    return chunks


def save_chunks():
    chunks = peo_chunker()

    OUTPUT_PATH.parent.mkdir(exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"✅ PEO chunks saved ({len(chunks)})")


if __name__ == "__main__":
    save_chunks()
