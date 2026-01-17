import requests
import hashlib
import json
import re
import os
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.nietbschool.ac.in/program#fee-structure"
OUTPUT_FILE = "../output/program_fee_structure.json"

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

def normalize(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def sha256_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def extract_fee_structure(soup):
    section = soup.find("section", id="fee-structure")
    if not section:
        return None

    description_tag = section.find("p")
    description = description_tag.get_text(strip=True) if description_tag else ""

    title_tag = section.find("h3")
    title = title_tag.get_text(strip=True) if title_tag else ""

    table = section.find("table")
    if not table:
        return None

    headers = [
        th.get_text(strip=True)
        for th in table.find("thead").find_all("th")
    ]

    rows = table.find("tbody").find_all("tr")

    amounts = [
        td.get_text(strip=True)
        for td in rows[0].find_all("td")
    ]

    payment_schedule = [
        td.get_text(strip=True)
        for td in rows[1].find_all("td")
    ]

    return {
        "description": description,
        "fee_structure": {
            "title": title,
            "columns": headers,
            "amounts": amounts,
            "payment_schedule": payment_schedule
        }
    }

# MAIN SCRAPER
def scrape_fee_structure():
    response = requests.get(URL, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    extracted = extract_fee_structure(soup)
    if not extracted:
        print("Fee structure section not found.")
        return

    combined_text = normalize(
        extracted["description"] +
        " ".join(extracted["fee_structure"]["columns"]) +
        " ".join(extracted["fee_structure"]["amounts"]) +
        " ".join(extracted["fee_structure"]["payment_schedule"])
    )

    result = {
        "page_type": "program_fee_structure",
        "source_url": URL,
        "last_scraped": datetime.utcnow().isoformat(),
        "content_hash": sha256_hash(combined_text),
        "data": extracted
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print("Fee structure scraped → program_fee_structure.json")

if __name__ == "__main__":
    scrape_fee_structure()
