import os
import re
import requests

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

URL = "https://news.blizzard.com/ko-kr/feed/diablo-2-resurrected"
STATE_FILE = "last_post.txt"

html = requests.get(URL, timeout=30).text

matches = re.findall(
    r'https://news\.blizzard\.com/en-us/article/\d+/[^"\s<>]+',
    html
)

if not matches:
    raise Exception("D2R 게시글 링크를 찾지 못했습니다.")

current_url = matches[0]

slug = current_url.rstrip("/").split("/")[-1]
current_title = slug.replace("-", " ").title()

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
