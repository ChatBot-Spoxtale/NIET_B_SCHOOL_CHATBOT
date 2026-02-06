import json
from pathlib import Path
from typing import List, Dict

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "placement_data.json"
OUTPUT_PATH = BASE_DIR / "data_chunk" / "placement_chunks.json"


def chunk_placement_page() -> List[Dict]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = []
    source_url = data.get("source_url")

    # Placement statistics chunks
    for i, stat in enumerate(data.get("statistics", []), 1):
        label = stat.get("label", "").strip()
        value = stat.get("value", "").strip()

        chunks.append({
            "id": f"placement_stat_{i}",
            "category": "placements",
            "question": f"What is the {label} at NIET Business School?",
            "answer": f"The {label} at NIET Business School is {value}.",
            "keywords": ["placements", label.lower(), "NIET"],
            "source_url": source_url
        })

    # Placed students (single compact chunk)
    placed_section = data.get("placed_students_section", {})
    students = placed_section.get("students", [])

    if students:
        student_text = ", ".join(
            f"{s['student_name']} ({s['company_name']})"
            for s in students
        )

        chunks.append({
            "id": "placed_students",
            "category": "placements",
            "question": "Which students have been placed from NIET Business School?",
            "answer": f"Some placed students include {student_text}.",
            "keywords": ["placed students", "placements", "companies"],
            "source_url": source_url
        })

    return chunks


def save_chunks():
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(chunk_placement_page(), f, indent=2, ensure_ascii=False)

    print("✅ Placement chunks saved")


if __name__ == "__main__":
    save_chunks()