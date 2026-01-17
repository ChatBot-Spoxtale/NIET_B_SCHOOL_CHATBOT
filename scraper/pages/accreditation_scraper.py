import requests
import hashlib
import json
import re
import os
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.nietbschool.ac.in/accreditation"
OUTPUT_FILE = "../output/accreditation_page.json"

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def sha256_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def extract_accreditations(soup: BeautifulSoup):
    accreditations = []

    acc_section = soup.find("section", id="accreditation")
    if not acc_section:
        return "", accreditations

    description_p = acc_section.find("p")
    description = description_p.get_text(strip=True) if description_p else ""

    cards = acc_section.find_all("div", class_=lambda c: c and "rounded-2xl" in c)

    for card in cards:
        img = card.find("img")
        title_p = card.find("p", class_=lambda c: c and "font-semibold" in c)
        subtitle_p = card.find("p", class_=lambda c: c and "text-xs" in c)

        if not (img and title_p and subtitle_p):
            continue

        code = img.get("alt", "").strip()
        title = title_p.get_text(strip=True)
        subtitle = subtitle_p.get_text(strip=True)

        accreditations.append({
            "code": code,
            "title": title,
            "description": subtitle
        })

    return description, accreditations

# MAIN SCRAPER
def scrape_accreditation_page():
    response = requests.get(URL, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    description, accreditations = extract_accreditations(soup)

    combined_text = normalize(
        description + " ".join(a["title"] + a["description"] for a in accreditations)
    )
    content_hash = sha256_hash(combined_text)

    result = {
        "page_type": "accreditations_page",
        "source_url": URL,
        "last_scraped": datetime.utcnow().isoformat(),
        "content_hash": content_hash,
        "data": {
            "description": description,
            "accreditations": accreditations
        }
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print("Accreditations page scraped successfully → accreditation_page.json")

if __name__ == "__main__":
    scrape_accreditation_page()
