import requests
import os
from bs4 import BeautifulSoup

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

URL = "https://news.blizzard.com/ko-kr/diablo2"

TITLE_FILE = "last_title.txt"

html = requests.get(URL, timeout=30).text

soup = BeautifulSoup(html, "html.parser")

title = soup.title.text.strip()

old_title = ""

if os.path.exists(TITLE_FILE):
    with open(TITLE_FILE, "r", encoding="utf-8") as f:
        old_title = f.read().strip()

if title != old_title:

    requests.post(
        WEBHOOK,
        json={
            "content": f"📢 D2R 새 소식 감지!\n\n{title}\n{URL}"
        },
        timeout=30,
    )

    with open(TITLE_FILE, "w", encoding="utf-8") as f:
        f.write(title)

print("Done")
