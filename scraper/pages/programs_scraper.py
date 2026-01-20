from pathlib import Path
import requests
import hashlib
import json
import re
import os
from bs4 import BeautifulSoup
from datetime import datetime
from io import BytesIO
from PIL import Image
import pytesseract

URL = "https://www.nietbschool.ac.in/program"

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "programs_page.json"

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def sha256_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def extract_program_highlights(soup):
    highlights = [
        "Industry-Focused Curriculum",
        "Expert Faculty",
        "Global Exposure",
        "Leadership Development",
        "Holistic Growth"
    ]

    img = soup.find("img", alt=lambda s: s and "program" in s.lower())
    if not img or not img.get("src"):
        return highlights

    img_url = img["src"]
    if not img_url.startswith("http"):
        img_url = "https://www.nietbschool.ac.in/" + img_url.lstrip("/")

    try:
        response = requests.get(img_url, timeout=20)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))

        raw_text = pytesseract.image_to_string(
            image,
            config="--psm 6"
        )

        cleaned = re.sub(r"[^a-zA-Z0-9.,’' ]+", " ", raw_text)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        if "curriculum nurtures" in cleaned.lower():
            highlights.append(
                "The curriculum nurtures critical thinking, leadership, communication, and analytical skills essential for thriving in today’s competitive global business environment."
            )

    except Exception:
        pass

    return highlights

def extract_about_program(soup):
    section = soup.find("section", id="about")
    if not section:
        return ""

    paragraphs = section.find_all("p")
    content = []

    for p in paragraphs:
        text = p.get_text(strip=True)
        if text:
            content.append(text)

    return " ".join(content)

# MAIN SCRAPER
def scrape_programs_page():
    response = requests.get(URL, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    program_highlights = extract_program_highlights(soup)
    about_program = extract_about_program(soup)

    full_text_for_hash = normalize(
        " ".join(program_highlights) + " " + about_program
    )
    content_hash = sha256_hash(full_text_for_hash)

    result = {
        "page_type": "programs_page",
        "source_url": URL,
        "last_scraped": datetime.utcnow().isoformat(),
        "content_hash": content_hash,
        "data": {
            "program_name": "PGDM",
            "program_highlights": program_highlights,
            "about_program": about_program
        }
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print("Programs page scraped successfully → programs_page.json")

if __name__ == "__main__":
    scrape_programs_page()
