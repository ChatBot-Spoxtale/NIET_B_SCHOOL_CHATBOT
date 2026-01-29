import json
from pathlib import Path
from typing import List, Dict


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "vision_data.json"
OUTPUT_PATH = BASE_DIR / "data_chunk" / "vision_chunks.json"


def chunk_vision_mission_page(data: dict):
    """
    Convert Vision & Mission page JSON into RAG chunks
    Format: id, question, answer, keywords
    """

    chunks = []

    vision = data.get("data", {}).get("vision")
    mission_list = data.get("data", {}).get("mission", [])

    # ---------- Vision ----------
    if vision:
        chunks.append({
            "id": "vision_mission_0",
            "question": "What is the vision of NIET Business School?",
            "answer": vision.strip(),
            "keywords": [
                "vision",
                "niet business school",
                "pgdm",
                "industry ready",
                "entrepreneurial",
                "socially responsible"
            ]
        })

    # ---------- Mission ----------
    for idx, mission in enumerate(mission_list, start=1):
        # Remove leading codes like "M1:"
        clean_mission = mission.split(":", 1)[-1].strip()

        chunks.append({
            "id": f"vision_mission_{idx}",
            "question": "What is the mission of NIET Business School?",
            "answer": clean_mission,
            "keywords": [
                "mission",
                "niet business school",
                "management education",
                "academic excellence",
                "industry ready",
                "ethics",
                "leadership"
            ]
        })

    return chunks

def save_chunks():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = chunk_vision_mission_page(data)

    OUTPUT_PATH.parent.mkdir(exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"Program chunks saved ({len(chunks)})")

if __name__ == "__main__":
    save_chunks() 