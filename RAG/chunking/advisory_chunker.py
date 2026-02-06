import json
from pathlib import Path
from typing import List, Dict

# ---------------- Paths ----------------

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "advisory_board.json"
OUTPUT_PATH = BASE_DIR / "data_chunk" / "advisory_board_chunks.json"


# ---------------- Chunker ----------------

def chunk_advisory_board() -> List[Dict]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    board = data.get("advisory_board", {})
    title = board.get("title", "NIET Advisory Board")
    description = board.get("description", "")
    members = board.get("members", [])
    source_url = data.get("source_url")

    chunks = []

    # 1️⃣ Advisory Board Overview
    chunks.append({
        "id": "advisory_board_overview",
        "category": "advisory_board",
        "question": "What is the NIET Advisory Board?",
        "answer": description,
        "keywords": [
            "NIET advisory board",
            "advisory board",
            "governance",
            "leadership",
            "NIET"
        ],
        "source_url": source_url
    })

    # 2️⃣ Individual Members
    for idx, member in enumerate(members, start=1):
        name = member.get("name", "").strip()
        designation = member.get("designation", "").strip()

        chunks.append({
            "id": f"advisory_board_member_{idx}",
            "category": "advisory_board",
            "question": f"Who is {name} at NIET Business School?",
            "answer": f"{name} serves as {designation} on the NIET Advisory Board.",
            "keywords": [
                name.lower(),
                designation.lower(),
                "advisory board",
                "NIET leadership"
            ],
            "source_url": source_url
        })

    return chunks


# ---------------- Save ----------------

def save_chunks():
    chunks = chunk_advisory_board()
    OUTPUT_PATH.parent.mkdir(exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"✅ Advisory Board chunks saved ({len(chunks)})")


if __name__ == "__main__":
    save_chunks()