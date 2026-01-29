import json
from pathlib import Path
from typing import List, Dict

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "placement_data.json"
OUTPUT_PATH = BASE_DIR / "data_chunk" / "placement_chunks.json"


def placement_chunker() -> List[Dict]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)

    source_url = raw.get("source_url", "")
    stats = raw.get("statistics", [])

    chunks = []

    # 🔹 Overall placement summary chunk
    summary_text = "\n".join(
        f"{stat['label']}: {stat['value']}"
        for stat in stats
    )

    chunks.append({
        "id": "placement_summary",
        "category": "placement",
        "question": "What is the placement record at NIET Business School?",
        "answer": summary_text,
        "keywords": [
            "placement",
            "placement record",
            "placements",
            "package",
            "recruiters"
        ],
        "source_url": source_url
    })

    # 🔹 Individual statistic chunks
    for stat in stats:
        label = stat.get("label", "").strip()
        value = stat.get("value", "").strip()

        chunks.append({
            "id": f"placement_{label.lower().replace(' ', '_')}",
            "category": "placement",
            "question": f"What is the {label.lower()} at NIET Business School?",
            "answer": value,
            "keywords": [
                "placement",
                label.lower(),
                "package",
                "record"
            ],
            "source_url": source_url
        })

    return chunks


def save_chunks():
    chunks = placement_chunker()

    OUTPUT_PATH.parent.mkdir(exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"✅ Placement chunks saved ({len(chunks)})")


if __name__ == "__main__":
    save_chunks()
