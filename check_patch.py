import os
import re
import requests
from bs4 import BeautifulSoup

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

LIST_URL = "https://news.blizzard.com/ko-kr/diablo2"
STATE_FILE = "last_post.txt"

headers = {"User-Agent": "Mozilla/5.0"}

html = requests.get(LIST_URL, headers=headers, timeout=30).text

# Blizzard 페이지 안의 ko-kr article 링크 추출
matches = re.findall(
    r"https://news\.blizzard\.com/ko-kr/article/\d+/[^\"'\s<>]+",
    html
)

# 상대경로 형태도 추출
matches += [
    "https://news.blizzard.com" + m
    for m in re.findall(r"/ko-kr/article/\d+/[^\"'\s<>]+", html)
]

# 중복 제거
seen = []
for url in matches:
    url = url.split("?")[0].rstrip("/")
    if url not in seen:
        seen.append(url)

if not seen:
    raise Exception("게시글 링크를 찾지 못했습니다.")

latest_url = seen[0]

article_html = requests.get(latest_url, headers=headers, timeout=30).text
article_soup = BeautifulSoup(article_html, "html.parser")

title_tag = article_soup.find("h1")
title = title_tag.get_text(" ", strip=True) if title_tag else latest_url

body_text = article_soup.get_text("\n", strip=True)

lines = []
for line in body_text.splitlines():
    line = line.strip()
    if not line:
        continue
    if line in ["Blizzard Entertainment", "디아블로 II: 레저렉션"]:
        continue
    if line not in lines:
        lines.append(line)

summary = "\n".join(lines[:8])

old_url = ""
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        old_url = f.read().strip()

if latest_url != old_url:
    message = f"""📢 새 D2R 공지 감지!

**{title}**

{summary}

🔗 {latest_url}
"""

    requests.post(
        WEBHOOK,
        json={"content": message[:1900]},
        timeout=30,
    )

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(latest_url)

print("Done")
