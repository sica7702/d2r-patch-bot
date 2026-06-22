import requests
import os

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

url = "https://news.blizzard.com/ko-kr/diablo2"

try:
    r = requests.get(url, timeout=30)

    requests.post(
        WEBHOOK,
        json={
            "content": f"📢 D2R 패치노트 확인 완료\n{url}\n상태코드: {r.status_code}"
        },
        timeout=30
    )

    print("Success")

except Exception as e:
    requests.post(
        WEBHOOK,
        json={
            "content": f"❌ 오류 발생\n{e}"
        },
        timeout=30
    )

    raise
