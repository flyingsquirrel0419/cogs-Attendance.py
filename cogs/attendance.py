import discord
from discord.ext import commands
from datetime import date
import json
import os

DATA_PATH = "./data/attendance.json"
WEEKDAY_KR = ["월", "화", "수", "목", "금", "토", "일"]

# -------------------------
# 데이터 처리
# -------------------------
def load_data():
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data: dict):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# -------------------------
# Cog
# -------------------------
class Attendance(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # -------------------------
    # 출석
    # -------------------------
    @commands.hybrid_command(name="출석", description="출석을 체크합니다.")
    async def attend(self, ctx: commands.Context):
        user_id = str(ctx.author.id)
        today = date.today()
        today_str = today.isoformat()
        weekday = WEEKDAY_KR[today.weekday()]

        data = load_data()

        if user_id not in data:
            data[user_id] = {
                "count": 0,
                "last_date": None
            }

        if data[user_id]["last_date"] == today_str:
            embed = discord.Embed(
                title="❌ 출석 실패",
                description="오늘은 이미 출석했습니다.",
                color=discord.Color.red()
            )
            await self._send(ctx, embed)
            return

        data[user_id]["count"] += 1
        data[user_id]["last_date"] = today_str
        save_data(data)

        embed = discord.Embed(
            title="✅ 출석 완료",
            color=discord.Color.green()
        )
        embed.add_field(
            name="유저",
            value=ctx.author.mention,
            inline=False
        )
        embed.add_field(
            name="누적 출석",
            value=f"{data[user_id]['count']}회",
            inline=False
        )
        embed.set_footer(text=f"{today_str} ({weekday}요일)")

        await self._send(ctx, embed)

    # -------------------------
    # 출석 랭킹
    # -------------------------
    @commands.hybrid_command(name="출석랭킹", description="출석 랭킹을 확인합니다.")
    async def ranking(self, ctx: commands.Context):
        data = load_data()

        if not data:
            await self._send(ctx, content="출석 데이터가 없습니다.")
            return

        ranking = sorted(
            data.items(),
            key=lambda x: x[1]["count"],
            reverse=True
        )[:10]

        embed = discord.Embed(
            title="🏆 출석 랭킹 TOP 10",
            color=discord.Color.gold()
        )

        for idx, (user_id, info) in enumerate(ranking, start=1):
            embed.add_field(
                name=f"{idx}위",
                value=f"<@{user_id}> — {info['count']}회",
                inline=False
            )

        await self._send(ctx, embed)

    # -------------------------
    # 공통 전송 로직
    # -------------------------
    async def _send(self, ctx: commands.Context, embed=None, content=None):
        # 텍스트 명령어(!) → 답장 + 무알람
        if ctx.interaction is None:
            await ctx.reply(
                content=content,
                embed=embed,
                mention_author=False,
                allowed_mentions=discord.AllowedMentions.none()
            )
        # 슬래시 명령어(/) → 일반 응답
        else:
            await ctx.send(
                content=content,
                embed=embed,
                allowed_mentions=discord.AllowedMentions.none()
            )

# -------------------------
# setup
# -------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(Attendance(bot))
