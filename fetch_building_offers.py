import imaplib
import email
import os
import re
import json
from email.header import decode_header
from datetime import datetime, timedelta
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

IMAP_SERVER = "outlook.office365.com"
IMAP_PORT = 993
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

BUILDING_KEYWORDS = [
    "offering memorandum", "om ", "for sale", "property offering",
    "acquisition opportunity", "investment opportunity", "asking price",
    "cap rate", "noi", "building for sale", "commercial property",
    "multifamily", "mixed use", "office building", "retail center",
    "industrial", "warehouse", "deal", "listing", "broker opinion",
    "bov", "loi", "letter of intent", "purchase price", "property at",
    "sq ft", "square feet", "units", "apartment", "plaza", "center",
]

def decode_str(s):
    if s is None:
        return ""
    parts = decode_header(s)
    decoded = []
    for part, charset in parts:
        if isinstance(part, bytes):
            decoded.append(part.decode(charset or "utf-8", errors="replace"))
        else:
            decoded.append(part)
    return " ".join(decoded)

def get_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == "text/plain":
                try:
                    body += part.get_payload(decode=True).decode("utf-8", errors="replace")
                except Exception:
                    pass
            elif ctype == "text/html" and not body:
                try:
                    html = part.get_payload(decode=True).decode("utf-8", errors="replace")
                    body += BeautifulSoup(html, "lxml").get_text(separator=" ")
                except Exception:
                    pass
    else:
        try:
            payload = msg.get_payload(decode=True)
            if payload:
                body = payload.decode("utf-8", errors="replace")
                if msg.get_content_type() == "text/html":
                    body = BeautifulSoup(body, "lxml").get_text(separator=" ")
        except Exception:
            pass
    return body

def is_building_offer(subject, body):
    text = (subject + " " + body).lower()
    return any(kw in text for kw in BUILDING_KEYWORDS)

def extract_address(text):
    pattern = r'\d+\s+[A-Z][a-zA-Z0-9\s,\.]+(?:Street|St|Avenue|Ave|Boulevard|Blvd|Road|Rd|Drive|Dr|Lane|Ln|Way|Place|Pl|Court|Ct|Highway|Hwy|Suite|Ste)\b[^,\n]*(?:,\s*[A-Z][a-zA-Z\s]+)?(?:,\s*[A-Z]{2})?(?:\s+\d{5})?'
    matches = re.findall(pattern, text)
    return matches[0].strip() if matches else None

def connect():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    return mail

def fetch_offers():
    print(f"Connecting to {IMAP_SERVER} as {EMAIL_ADDRESS}...")
    mail = connect()
    mail.select("INBOX")

    since_date = (datetime.now() - timedelta(days=730)).strftime("%d-%b-%Y")
    status, data = mail.search(None, f'(SINCE "{since_date}")')

    if status != "OK":
        print("Failed to search emails.")
        return []

    email_ids = data[0].split()
    print(f"Found {len(email_ids)} emails in the last 24 months. Scanning...")

    offers = []
    for i, eid in enumerate(email_ids):
        if i % 100 == 0:
            print(f"  Processing {i}/{len(email_ids)}...")
        try:
            status, msg_data = mail.fetch(eid, "(RFC822)")
            if status != "OK":
                continue
            raw = msg_data[0][1]
            msg = email.message_from_bytes(raw)

            subject = decode_str(msg.get("Subject", ""))
            sender = decode_str(msg.get("From", ""))
            date_str = msg.get("Date", "")

            body = get_body(msg)

            if not is_building_offer(subject, body):
                continue

            address = extract_address(subject) or extract_address(body[:2000])

            offers.append({
                "date": date_str,
                "subject": subject,
                "from": sender,
                "address": address or "See email",
                "snippet": body[:300].strip().replace("\n", " "),
            })
        except Exception as e:
            continue

    mail.logout()
    return offers

def save_results(offers):
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save JSON
    json_path = f"output/building_offers_{timestamp}.json"
    with open(json_path, "w") as f:
        json.dump(offers, f, indent=2)

    # Save readable text list
    txt_path = f"output/building_offers_{timestamp}.txt"
    with open(txt_path, "w") as f:
        f.write(f"BUILDING OFFERS - Last 24 Months\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Total found: {len(offers)}\n")
        f.write("=" * 70 + "\n\n")
        for i, offer in enumerate(offers, 1):
            f.write(f"{i}. {offer['subject']}\n")
            f.write(f"   Date:    {offer['date']}\n")
            f.write(f"   From:    {offer['from']}\n")
            f.write(f"   Address: {offer['address']}\n")
            f.write(f"   Preview: {offer['snippet'][:200]}\n")
            f.write("-" * 70 + "\n\n")

    print(f"\nSaved {len(offers)} offers to:")
    print(f"  {txt_path}")
    print(f"  {json_path}")
    return txt_path, json_path

if __name__ == "__main__":
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("ERROR: Set EMAIL_ADDRESS and EMAIL_PASSWORD in your .env file.")
        exit(1)

    offers = fetch_offers()
    print(f"\nFound {len(offers)} building offers.")

    if offers:
        save_results(offers)
    else:
        print("No building offers found matching the keywords.")
