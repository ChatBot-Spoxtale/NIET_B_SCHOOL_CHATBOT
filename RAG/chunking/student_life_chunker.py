import json
from pathlib import Path
from typing import List, Dict


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "student_life.json"
OUTPUT_PATH = BASE_DIR / "data_chunk" / "student_life_chunks.json"


def chunk_student_life_page(data: dict):
    """
    Convert Student Life page JSON into RAG chunks
    Format: id, question, answer, keywords
    """

    chunks = []

    # ---------- Student Life Overview ----------
    student_life = data.get("student_life", {})

    if student_life:
        chunks.append({
            "id": "student_life_0",
            "question": "What is student life like at NIET Business School?",
            "answer": student_life.get("description", ""),
            "keywords": [
                "student life",
                "campus life",
                "niet business school",
                "clubs",
                "committees",
                "sports",
                "fests",
                "live projects",
                "industry interaction"
            ]
        })

    # ---------- Facilities ----------
    facilities = data.get("facilities", [])

    for idx, facility in enumerate(facilities, start=1):
        title = facility.get("title", "")
        description = facility.get("description", "")

        chunks.append({
            "id": f"student_life_{idx}",
            "question": f"What {title.lower()} facilities are available at NIET Business School?",
            "answer": description,
            "keywords": [
                title.lower(),
                "student facilities",
                "campus facilities",
                "student life",
                "niet business school"
            ]
        })

    return chunks

def save_chunks():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = chunk_student_life_page(data)

    OUTPUT_PATH.parent.mkdir(exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"Program chunks saved ({len(chunks)})")

if __name__ == "__main__":
    save_chunks() 