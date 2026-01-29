import json
from pathlib import Path
from typing import List, Dict


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "about_college.json"
OUTPUT_PATH = BASE_DIR / "data_chunk" / "about_college_chunks.json"


def chunk_about_college() -> List[Dict]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    college = data.get("college_name", "NIET Business School")
    sections = data.get("sections", {})
    chunks = []

    # Overview
    if "college_overview" in sections:
        chunks.append({
            "id": "college_overview",
            "category": "about_college",
            "question": f"What is {college}?",
            "answer": sections["college_overview"]["content"],
            "keywords": ["niet", "college", "overview"],
            "source_url": sections["college_overview"].get("source_url")
        })

    # Vision
    if "vision" in sections:
        chunks.append({
            "id": "college_vision",
            "category": "about_college",
            "question": f"What is the vision of {college}?",
            "answer": sections["vision"]["content"],
            "keywords": ["vision", "niet"],
            "source_url": sections["vision"].get("source_url")
        })

    # Mission
    if "mission" in sections:
        mission_text = "\n".join(sections["mission"]["points"])
        chunks.append({
            "id": "college_mission",
            "category": "about_college",
            "question": f"What is the mission of {college}?",
            "answer": mission_text,
            "keywords": ["mission", "niet"],
            "source_url": sections["mission"].get("source_url")
        })

    # Accreditations
    if "accreditations" in sections:
        acc = sections["accreditations"]
        acc_text = acc["description"] + "\n\n" + "\n".join(
            f"{a['title']} ({a['code']})" for a in acc["list"]
        )

        chunks.append({
            "id": "college_accreditations",
            "category": "about_college",
            "question": f"What accreditations does {college} have?",
            "answer": acc_text,
            "keywords": ["aicte", "nba", "aacsb", "accreditation"],
            "source_url": acc.get("source_url")
        })

    return chunks


def save_chunks():
    chunks = chunk_about_college()
    OUTPUT_PATH.parent.mkdir(exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"✅ About college chunks saved ({len(chunks)})")


if __name__ == "__main__":
    save_chunks()
