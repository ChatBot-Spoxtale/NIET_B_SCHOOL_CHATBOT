import json
import os
from datetime import datetime

OUTPUT_DIR = "./output"
MERGED_FILE = os.path.join(OUTPUT_DIR, "all_about_programs.json")

PROGRAM_FILES = {
    "program_overview": "programs_page.json",
    "key_features": "program_key_features.json",
    "fee_structure": "program_fee_structure.json",
    "program_objectives": "program_objectives.json"
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def merge_all_programs():
    merged = {
        "page_type": "all_about_programs",
        "last_updated": datetime.utcnow().isoformat(),
        "sources": {},
        "data": {}
    }

    previous_hashes = {}
    if os.path.exists(MERGED_FILE):
        old_data = load_json(MERGED_FILE)
        previous_hashes = {
            key: value.get("content_hash")
            for key, value in old_data.get("sources", {}).items()
        }

    has_changed = False

    for section, filename in PROGRAM_FILES.items():
        file_path = os.path.join(OUTPUT_DIR, filename)

        if not os.path.exists(file_path):
            print(f"[WARNING] Missing file: {filename}")
            continue

        content = load_json(file_path)
        new_hash = content.get("content_hash")
        old_hash = previous_hashes.get(section)

        if new_hash != old_hash:
            has_changed = True

        merged["sources"][section] = {
            "source_url": content.get("source_url"),
            "content_hash": new_hash
        }

        merged["data"][section] = content.get("data")

    if not has_changed and os.path.exists(MERGED_FILE):
        print("No changes detected. all_about_programs.json not updated.")
        return

    with open(MERGED_FILE, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=4, ensure_ascii=False)

    print("✅ all_about_programs.json updated successfully")


if __name__ == "__main__":
    merge_all_programs()
