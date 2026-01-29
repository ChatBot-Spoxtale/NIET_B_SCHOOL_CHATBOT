import json
import uuid
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "club_data.json"
CHUNK_PATH = BASE_DIR / "data_chunk" / "clubs_chunks.json"


def gen_id():
    return f"club_{uuid.uuid4().hex[:6]}"


def create_club_chunks():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)

    chunks = []

    for page in raw["clubs"]:
        # overview
        if page["page_type"] == "clubs_overview_page":
            chunks.append({
                "id": gen_id(),
                "question": "What clubs and societies are available at NIET Business School?",
                "answer": f"{page['overview']['title']}\n\n{page['overview']['description']}\n\nSource: {page['source_url']}",
                "keywords": ["clubs", "societies", "student life"]
            })

        # individual clubs
        if page["page_type"] == "club_detail_page":
            chunks.append({
                "id": gen_id(),
                "question": f"What is {page['club_name']} club at NIET Business School?",
                "answer": f"{page['club_name']} ({page['domain']})\n\n{page['description']}\n\nSource: {page['source_url']}",
                "keywords": [
                    page["club_name"].lower(),
                    page["domain"].lower()
                ]
            })

    CHUNK_PATH.parent.mkdir(exist_ok=True)
    with open(CHUNK_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4, ensure_ascii=False)

    print(f"Created {len(chunks)} club chunks")


if __name__ == "__main__":
    create_club_chunks()
