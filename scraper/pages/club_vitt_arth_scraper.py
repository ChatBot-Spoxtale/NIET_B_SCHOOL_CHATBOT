import requests
import json
import hashlib
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

URL = "https://www.nietbschool.ac.in/vitt-arth"
OUTPUT_FILE = Path("../output/club_vitt_arth.json")


def generate_hash(data: dict) -> str:
    clean = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(clean.encode("utf-8")).hexdigest()


def scrape_vitt_arth():
    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    main_section = soup.select_one("section.md\\:col-span-3 section")

    if not main_section:
        raise RuntimeError("Vitt Arth content section not found")

    name = main_section.find("h2").get_text(strip=True)

    domain_tag = main_section.find("p", class_="text-[#D6323A]")
    domain = domain_tag.get_text(strip=True) if domain_tag else ""

    img_tag = main_section.find("img")
    image_url = urljoin(URL, img_tag["src"]) if img_tag else ""

    description_parts = []
    text_container = main_section.find("div", class_="space-y-4")

    if text_container:
        for p in text_container.find_all("p"):
            description_parts.append(p.get_text(" ", strip=True))

    description = "\n\n".join(description_parts)

    data = {
        "page_type": "club_detail_page",
        "club_name": name,
        "domain": domain,
        "image_url": image_url,
        "description": description,
        "source_url": URL,
        "last_scraped": datetime.utcnow().isoformat()
    }

    data["content_hash"] = generate_hash(data)
    return data


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    data = scrape_vitt_arth()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("✅ Vitt Arth club data scraped successfully")


if __name__ == "__main__":
    main()
