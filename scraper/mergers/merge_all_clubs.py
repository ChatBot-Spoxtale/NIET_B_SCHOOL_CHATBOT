import json
import hashlib
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("output")
MERGED_FILE = OUTPUT_DIR / "all_clubs.json"

CLUB_FILES = [
    "clubs_overview_page.json",
    "club_prati_dhwani.json",
    "club_vitt_arth.json",
    "club_pravah.json",
    "club_anveshak.json",
    "club_vistar.json",
    "club_udyam.json",
    "club_karmik.json",
    "club_swavlamban.json",
    "club_adhvan.json",
    "club_tejas.json",
    "club_varnam.json",
]


def generate_hash(data: dict) -> str:
    clean = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(clean.encode("utf-8")).hexdigest()


def load_json(path: Path):
    if not path.exists():
        print(f"⚠ Missing file: {path.name}")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    merged = {
        "page_type": "all_clubs",
        "last_merged": datetime.utcnow().isoformat(),
        "clubs": []
    }

    for filename in CLUB_FILES:
        file_path = OUTPUT_DIR / filename
        data = load_json(file_path)

        if not data:
            continue

        data.pop("last_scraped", None)
        merged["clubs"].append(data)

    merged["content_hash"] = generate_hash(merged)

    if MERGED_FILE.exists():
        with open(MERGED_FILE, "r", encoding="utf-8") as f:
            old = json.load(f)

        if old.get("content_hash") == merged["content_hash"]:
            print("✅ No club changes detected. Merge skipped.")
            return

    with open(MERGED_FILE, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=4, ensure_ascii=False)

    print("✅ all_clubs.json updated successfully")


if __name__ == "__main__":
    main()
