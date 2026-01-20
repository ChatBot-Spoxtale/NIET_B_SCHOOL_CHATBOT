import requests
from bs4 import BeautifulSoup
import json
import hashlib
from datetime import datetime
from pathlib import Path

URL = "https://www.nietbschool.ac.in/contact"

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "contact_page.json"
def get_hash(data: dict) -> str:
    return hashlib.sha256(
        json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def scrape_contact_page():
    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    def extract_address(block_title):
        block = soup.find("h3", string=block_title)
        if not block:
            return []
        p = block.find_next("p")
        return [line.strip() for line in p.get_text("\n").split("\n") if line.strip()]

    main_campus_address = extract_address("Main Campus")
    remote_office_address = extract_address("Remote Admission Office")

    phones = [
        a.get_text(strip=True)
        for a in soup.select('a[href^="tel:"]')
    ]

    email_tag = soup.select_one('a[href^="mailto:"]')
    email = email_tag.get_text(strip=True) if email_tag else ""

    #MAP
    iframe = soup.find("iframe")
    map_url = iframe["src"] if iframe else ""

    map_address = ""
    map_caption = soup.find("p", class_="text-gray-600")
    if map_caption:
        map_address = map_caption.get_text(strip=True)

    data = {
        "page_type": "contact_page",
        "source_url": URL,
        "last_scraped": datetime.utcnow().isoformat(),
        "get_in_touch": {
            "main_campus": {
                "name": "Main Campus",
                "address": main_campus_address
            },
            "remote_admission_office": {
                "name": "Remote Admission Office",
                "address": remote_office_address
            },
            "admission_helpline": phones,
            "email": email
        },
        "map": {
            "embed_url": map_url,
            "location_name": "NIET Business School",
            "address_text": map_address
        }
    }

    data["content_hash"] = get_hash(data)
    return data


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = scrape_contact_page()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("✅ contact_page.json updated")


if __name__ == "__main__":
    main()
