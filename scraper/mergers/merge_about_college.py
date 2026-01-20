import json
import os
from datetime import datetime

BASE_PATH = "output/"
STATE_FILE = BASE_PATH + ".merge_state.json"

FILES = {
    "about_page": "about_page.json",
    "vision_mission_page": "vision_mission_page.json",
    "peos_page": "peos_page.json",
    "accreditation_page": "accreditation_page.json"
}

def load_json(file):
    with open(BASE_PATH + file, "r", encoding="utf-8") as f:
        return json.load(f)

def load_state():
    if not os.path.exists(STATE_FILE):
        return {key: "" for key in FILES}
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)

def get_current_hashes():
    hashes = {}
    for key, file in FILES.items():
        data = load_json(file)
        hashes[key] = data.get("content_hash", "")
    return hashes

def has_changed(old, new):
    return any(old.get(k) != new.get(k) for k in FILES)

def merge_about_college():
    about = load_json(FILES["about_page"])
    vision_mission = load_json(FILES["vision_mission_page"])
    peos = load_json(FILES["peos_page"])
    accreditation = load_json(FILES["accreditation_page"])

    merged = {
        "college_name": "NIET Business School",
        "source": "https://www.nietbschool.ac.in",
        "last_merged": datetime.utcnow().isoformat(),
        "sections": {
            "college_overview": {
                "source_url": about["source_url"],
                "content": about["data"]["college_overview"]
            },
            "vision": {
                "source_url": vision_mission["source_url"],
                "content": vision_mission["data"]["vision"]
            },
            "mission": {
                "source_url": vision_mission["source_url"],
                "points": vision_mission["data"]["mission"]
            },
            "program_educational_objectives": {
                "source_url": peos["source_url"],
                "peos": peos["data"]["peos"]
            },
            "accreditations": {
                "source_url": accreditation["source_url"],
                "description": accreditation["data"]["description"],
                "list": accreditation["data"]["accreditations"]
            }
        }
    }

    with open(BASE_PATH + "about_college.json", "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=4, ensure_ascii=False)

    print("about_college.json updated")


def main():
    old_state = load_state()
    new_state = get_current_hashes()

    if has_changed(old_state, new_state):
        print("Change detected → re-merging")
        merge_about_college()
        save_state(new_state)
    else:
        print("No changes detected → merge skipped")


if __name__ == "__main__":
    main()
