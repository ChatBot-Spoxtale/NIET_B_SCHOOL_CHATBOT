import sys
import subprocess
from pathlib import Path
import json
import hashlib

sys.stdout.reconfigure(encoding="utf-8")
BASE_DIR = Path(__file__).resolve().parent

PAGES_DIR = BASE_DIR / "pages"
MERGERS_DIR = BASE_DIR / "mergers"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

STATE_FILE = OUTPUT_DIR / ".merge_state.json"

SCRAPERS = [
    "about_scraper.py",
    "vision_mission_scraper.py",
    "accreditation_scraper.py",
    "peos_scraper.py",

    "programs_scraper.py",
    "program_key_features_scraper.py",
    "program_objectives_scraper.py",
    "program_fee_structure_scraper.py",

    "club_overview_scraper.py",
    "club_prati_scraper.py",
    "club_vitt_arth_scraper.py",
    "club_pravah_scraper.py",
    "club_anveshak_scraper.py",
    "club_vistar_scraper.py",
    "club_udyam_scraper.py",
    "club_karmik_scraper.py",
    "club_swavlamban_scraper.py",
    "club_adhvan_scraper.py",
    "club_tejas_scraper.py",
    "club_varnam_scraper.py",

    "placements_scraper.py",
    "student_life_scraper.py",
    "contact_scraper.py",
]

MERGERS = [
    "merge_about_college.py",
    "merge_all_about_programs.py",
    "merge_all_clubs.py",
]

def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}

def save_state(state):
    STATE_FILE.write_text(
        json.dumps(state, indent=4),
        encoding="utf-8"
    )

def run_script(script_path: Path):
    if not script_path.exists():
        print(f"[SKIP] Missing file: {script_path.name}")
        return False

    print(f"▶ Running {script_path.name}")

    result = subprocess.run(
        [sys.executable, "-X", "utf8", script_path],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"[ERROR] {script_path.name}")
        print(result.stderr)
        return False

    return True

def main():
    print("\n🚀 MAIN CONTROLLER STARTED\n")

    state = load_state()
    changed = False

    for scraper in SCRAPERS:
        run_script(PAGES_DIR / scraper)

    for json_file in OUTPUT_DIR.glob("*.json"):
        h = file_hash(json_file)
        if state.get(json_file.name) != h:
            print(f"🔄 Change detected: {json_file.name}")
            state[json_file.name] = h
            changed = True

    if changed:
        print("\n🧩 Running mergers...\n")
        for merger in MERGERS:
            run_script(MERGERS_DIR / merger)
    else:
        print("\n✅ No changes detected. Mergers skipped.")

    save_state(state)

    print("\n✅ MAIN CONTROLLER COMPLETED SUCCESSFULLY\n")

if __name__ == "__main__":
    main()
