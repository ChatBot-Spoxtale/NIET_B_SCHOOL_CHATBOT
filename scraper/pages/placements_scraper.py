import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


URL = "https://www.nietbschool.ac.in/placement"

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "placements_page.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def ensure_output_dir():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)


def fetch_page():
    response = requests.get(URL, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.text


def scrape_statistics(soup):
    stats = []
    cards = soup.select("div.text-center")

    for card in cards:
        value_el = card.find("div", class_="text-3xl")
        label_el = card.find("div", class_="text-sm")

        if value_el and label_el:
            value = value_el.get_text(strip=True)
            label = label_el.get_text(strip=True)

            if value and label:
                stats.append({
                    "label": label,
                    "value": value
                })

    return stats


def scrape_placement_banner(soup):
    img = soup.find("img", alt=lambda x: x and "Placement Excellence" in x)
    if img and img.get("src"):
        return urljoin(URL, img["src"])
    return None


def compute_hash(data):
    hash_source = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(hash_source.encode("utf-8")).hexdigest()


def main():
    ensure_output_dir()

    html = fetch_page()
    soup = BeautifulSoup(html, "html.parser")

    statistics = scrape_statistics(soup)
    placement_banner = scrape_placement_banner(soup)

    data = {
        "page_type": "placements_page",
        "source_url": URL,
        "last_scraped": datetime.utcnow().isoformat(),
        "statistics": statistics,
        "placement_banner": placement_banner
    }

    data["content_hash"] = compute_hash(data)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("✅ placements_page.json generated successfully")


if __name__ == "__main__":
    main()
