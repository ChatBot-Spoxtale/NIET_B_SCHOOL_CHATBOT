import requests
from bs4 import BeautifulSoup
import json
import hashlib
from datetime import datetime
from pathlib import Path

URL = "https://www.nietbschool.ac.in/clubs-societies"
BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "clubs_overview_page.json"


def generate_hash(data: dict) -> str:
    return hashlib.sha256(
        json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def scrape_clubs_overview():
    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    overview_section = soup.find("section", id="overview")

    if not overview_section:
        raise RuntimeError("Clubs overview section not found")
    title = overview_section.find("h2").get_text(strip=True)

    description_tag = overview_section.find("p")
    description_text = description_tag.get_text(" ", strip=True) if description_tag else ""

    clubs = []

    club_list = overview_section.find("ul")
    if club_list:
        for li in club_list.find_all("li"):
            text = li.get_text(" ", strip=True)

            if "–" in text:
                name, domain = [x.strip() for x in text.split("–", 1)]
            else:
                continue  

            clubs.append({
                "name": name,
                "domain": domain
            })

    data = {
        "page_type": "clubs_overview_page",
        "source_url": URL,
        "last_scraped": datetime.utcnow().isoformat(),
        "overview": {
            "title": title,
            "description": description_text
        },
        "clubs": clubs
    }

    data["content_hash"] = generate_hash(data)
    return data

def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    data = scrape_clubs_overview()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("✅ clubs_overview_page.json updated successfully.")


if __name__ == "__main__":
    main()
