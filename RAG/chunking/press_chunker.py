import json
from pathlib import Path
from typing import List, Dict

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "press_page.json"
OUTPUT_PATH = BASE_DIR / "data_chunk" / "press_chunks.json"


def chunk_press_page() -> List[Dict]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = []
    source_url = data.get("source_url")

    for i, press in enumerate(data.get("press_releases", []), 1):
        headline = press.get("headline", "").strip()
        date = press.get("date", "").strip()
        url = press.get("url", "").strip()

        answer = f"{headline} ({date})."
        if url:
            answer += f" Read more: {url}"

        chunks.append({
            "id": f"press_{i}",
            "category": "press",
            "question": f"What is the press news '{headline}'?",
            "answer": answer,
            "keywords": ["press", "news", headline.lower()],
            "source_url": source_url
        })

    return chunks


def save_chunks():
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(chunk_press_page(), f, indent=2, ensure_ascii=False)

    print("✅ Press chunks saved")


if __name__ == "__main__":
    save_chunks()