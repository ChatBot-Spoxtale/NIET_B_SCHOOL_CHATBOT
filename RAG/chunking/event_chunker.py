import json
from pathlib import Path
from typing import List, Dict


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "event_data.json"
OUTPUT_PATH = BASE_DIR / "data_chunk" / "event_chunks.json"

def chunk_events_page(data: dict):
    """
    Convert Events page JSON into RAG chunks
    Format: id, question, answer, keywords
    """

    chunks = []

    events = data.get("data", {}).get("events", [])

    for idx, event in enumerate(events):
        title = event.get("title", "").strip()
        description = event.get("description", "").strip()
        date = event.get("date", "").strip()

        answer_parts = []
        if description:
            answer_parts.append(description)
        if date:
            answer_parts.append(f"Event Date: {date}")

        answer = " ".join(answer_parts)

        chunks.append({
            "id": f"event_{idx}",
            "question": f"What is the event '{title}' at NIET Business School?",
            "answer": answer,
            "keywords": [
                "event",
                "events",
                "niet business school",
                "campus event",
                "student activity",
                title.lower()
            ]
        })

    return chunks

def save_chunks():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = chunk_events_page(data)

    OUTPUT_PATH.parent.mkdir(exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"Program chunks saved ({len(chunks)})")

if __name__ == "__main__":
    save_chunks() 