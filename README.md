`Attendance.py`는 Discord 봇용 출석 관리 Cog입니다.  
사용자 출석 체크, 누적 출석 기록, 출석 랭킹 확인 기능을 제공합니다.

## 🔗 참고
이 Cog를 사용하는 기본 봇 예시는 [app.py-for-discord-bot](https://github.com/flyingsquirrel0419/app.py-for-discord-bot) 를 참고하세요.

---

## ⚙️ 설치 방법

1. Python 3.10 이상 환경에서 Discord.py 설치
```bash
pip install -U discord.py
````

2. 프로젝트 디렉토리에 `cogs` 폴더 생성 후, `attendance.py` 파일 추가

3. `app.py`에서 Cog 로드

```python
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

async def load_cogs():
    await bot.load_extension("cogs.attendance")

bot.loop.run_until_complete(load_cogs())
bot.run("YOUR_BOT_TOKEN")
```

4. 데이터 파일 경로

* 기본: `./data/attendance.json`
* 없으면 자동 생성됨

---

## 📝 명령어

### `/출석` 또는 `!출석`

* 오늘 출석 체크
* 이미 출석했으면 실패 메시지 표시
* 성공 시 누적 출석 수 표시

**응답 예시**

```
✅ 출석 완료
유저: @username
누적 출석: 5회
2025-12-18 (목요일)
```

---

### `/출석랭킹` 또는 `!출석랭킹`

* 출석 누적 TOP 10 확인
* 데이터가 없으면 안내 메시지 표시

**응답 예시**

```
🏆 출석 랭킹 TOP 10
1위: @user1 — 15회
2위: @user2 — 12회
...
```

---

## 💾 데이터 구조

`attendance.json` 예시:

```json
{
    "123456789012345678": {
        "count": 5,
        "last_date": "2025-12-18"
    },
    "987654321098765432": {
        "count": 3,
        "last_date": "2025-12-17"
    }
}
```

* key: Discord 사용자 ID
* `count`: 누적 출석 횟수
* `last_date`: 마지막 출석 날짜 (ISO format)

---

## ⚠️ 주의사항

* 텍스트 명령어(`!출석`)는 봇이 답장으로 처리
* 슬래시 명령어(`/출석`)는 인터랙션으로 처리
* 데이터 파일이 없으면 자동 생성되지만, 디렉토리가 없으면 `os.makedirs`로 생성

