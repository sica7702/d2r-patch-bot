import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

URL = "https://news.blizzard.com/ko-kr/feed/diablo-2-resurrected"
STATE_FILE = "last_post.txt"

html = requests.get(URL, timeout=30).text
soup = BeautifulSoup(html, "html.parser")

links = []

for a in soup.find_all("a", href=True):
    href = a["href"]
    title = a.get_text(" ", strip=True)

    if not title:
        continue

    full_url = urljoin("https://news.blizzard.com", href)

    if "/diablo2/" in full_url or "/diablo-ii" in full_url or "diablo-2-resurrected" in full_url:
        links.append((title, full_url))

if not links:
    raise Exception("D2R 게시글을 찾지 못했습니다.")

current_title, current_url = links[0]
current_key = current_url

old_key = ""

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        old_key = f.read().strip()

if current_key != old_key:
    message = f"""📢 새 D2R 공지 감지!

**{current_title}**
{current_url}
"""

    requests.post(
        WEBHOOK,
        json={"content": message},
        timeout=30,
    )

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(current_key)

print("Done")
