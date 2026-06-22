import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

URL = "https://news.blizzard.com/ko-kr/feed/diablo-2-resurrected"
STATE_FILE = "last_post.txt"

headers = {
    "User-Agent": "Mozilla/5.0"
}

html = requests.get(URL, headers=headers, timeout=30).text

posts = []

# 1) a 태그에서 게시글 링크 찾기
soup = BeautifulSoup(html, "html.parser")

for a in soup.find_all("a", href=True):
    href = a["href"]

    if "/article/" in href:
        full_url = urljoin("https://news.blizzard.com", href)
        if "news.blizzard.com" in full_url:
            title = a.get_text(" ", strip=True)
            posts.append((title, full_url))

# 2) HTML/JSON 안에 숨어있는 article 링크 찾기
patterns = [
    r'https://news\.blizzard\.com/ko-kr/article/\d+/[a-z0-9-]+',
    r'/en-us/article/\d+/[a-z0-9-]+',
    r'\\/en-us\\/article\\/\d+\\/[a-z0-9-]+',
]

for pattern in patterns:
    for match in re.findall(pattern, html):
        url = match.replace("\\/", "/")

        if url.startswith("/"):
            url = "https://news.blizzard.com" + url

        slug = url.rstrip("/").split("/")[-1]
        title = slug.replace("-", " ").title()

        posts.append((title, url))

# 중복 제거
unique_posts = []
seen = set()

for title, url in posts:
    if url not in seen:
        seen.add(url)
        unique_posts.append((title, url))

if not unique_posts:
    raise Exception("D2R 게시글 링크를 찾지 못했습니다.")

current_title, current_url = unique_posts[0]

old_url = ""

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        old_url = f.read().strip()

if current_url != old_url:
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
        f.write(current_url)

print("Done")
