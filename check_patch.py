import os
import requests
from bs4 import BeautifulSoup

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

API_URL = "https://news.blizzard.com/ko-kr/api/news/blizzard?feedCxpProductIds[]=blt54fbd3787a705054"
STATE_FILE = "last_post.txt"

headers = {"User-Agent": "Mozilla/5.0"}

data = requests.get(API_URL, headers=headers, timeout=30).json()
items = data["feed"]["contentItems"]

latest = items[0]["properties"]

title = latest["title"]
url = latest["newsUrl"]
summary = latest.get("summary", "").strip()
raw_date = latest.get("lastUpdated", "")
date = raw_date[:10].replace("-", ".") if raw_date else ""

old_url = ""

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        old_url = f.read().strip()

if url != old_url:
    message = f"""🌙 루나봇이 새로운 소식을 들고왔어요!

**{title}**

{summary}

📅 {date}
🔗 {url}
"""

    requests.post(
        WEBHOOK,
        json={"content": message[:1900]},
        timeout=30,
    )

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(url)

print("Done")
