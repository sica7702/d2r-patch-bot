import os
import requests
from bs4 import BeautifulSoup

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

URL = "https://news.blizzard.com/ko-kr/diablo2"
STATE_FILE = "last_post.txt"

html = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30).text
soup = BeautifulSoup(html, "html.parser")

title = soup.title.get_text(strip=True)

old = ""
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        old = f.read().strip()

if title != old:
    requests.post(
        WEBHOOK,
        json={
            "content": f"📢 D2R 소식 페이지 변경 감지!\n\n**{title}**\n{URL}"
        },
        timeout=30,
    )

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(title)

print("Done")

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(current_url)

print("Done")
