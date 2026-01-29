import json
from pathlib import Path
from typing import List, Dict


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "all_about_program.json"
OUTPUT_PATH = BASE_DIR / "data_chunk" / "program_chunks.json"


def chunk_program_data() -> List[Dict]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    program_data = data.get("data", {})
    sources = data.get("sources", {})
    chunks = []

    # Key Features
    if "key_features" in program_data:
        for i, item in enumerate(program_data["key_features"]["key_features"]):
            chunks.append({
                "id": f"program_feature_{i+1}",
                "category": "program",
                "question": "What are the key features of the PGDM program?",
                "answer": f"{item['title']}: {item['description']}",
                "keywords": ["pgdm", "features", item["title"].lower()],
                "source_url": sources["key_features"]["source_url"]
            })

    # Objectives
    if "program_objectives" in program_data:
        for i, obj in enumerate(program_data["program_objectives"]["objectives"]):
            chunks.append({
                "id": f"program_objective_{i+1}",
                "category": "program",
                "question": "What are the objectives of the PGDM program?",
                "answer": f"{obj['title']}: {obj['description']}",
                "keywords": ["pgdm", "objective", obj["title"].lower()],
                "source_url": sources["program_objectives"]["source_url"]
            })

    # Fee Structure
    if "fee_structure" in program_data:
        fee = program_data["fee_structure"]
        fee_text = fee["description"] + "\n\n" + \
                   "\n".join(fee["fee_structure"]["amounts"])

        chunks.append({
            "id": "pgdm_fee_structure",
            "category": "program",
            "question": "What is the fee structure of the PGDM program?",
            "answer": fee_text,
            "keywords": ["pgdm", "fees", "fee structure"],
            "source_url": sources["fee_structure"]["source_url"]
        })

    return chunks


def save_chunks():
    chunks = chunk_program_data()
    OUTPUT_PATH.parent.mkdir(exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"✅ Program chunks saved ({len(chunks)})")


if __name__ == "__main__":
    save_chunks()
