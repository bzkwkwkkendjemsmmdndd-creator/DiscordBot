"""
Cog модерации.
— Авто-модерация: спам, массовые упоминания, запрещённые слова
— Slash-команды: /warn /mute /unmute /kick /ban /unban /clear /warnings
— Автоматические наказания по эскалации предупреждений
"""

import asyncio
import re
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

import config
from utils.checks import is_moderator, is_admin, send_mod_log
from utils.embeds import (
    success_embed, error_embed, warning_embed, mod_embed,
    punishment_embed, info_embed
)


class Moderation(commands.Cog):
    """Система модерации."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Хранилище для отслеживания спама: {guild_id: {user_id: deque[timestamp]}}
        self._message_times: dict = defaultdict(lambda: defaultdict(lambda: deque(maxlen=20)))
        # Кулдаун уведомлений об авто-моде: {guild_id: {user_id: last_notified}}
        self._notified: dict = defaultdict(dict)

    # ─────────────────────────── АВТО-МОДЕРАЦИЯ ────────────────────────────

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Проверяет каждое сообщение на нарушения авто-мода."""
        if not message.guild or message.author.bot:
            return
        # Администраторы не проверяются
        if message.author.guild_permissions.administrator:
            return

        cfg = config.load_config(message.guild.id)
        if not cfg["automod"]["enabled"]:
            return

        reasons = []

        # 1. Проверка запрещённых слов
        content_lower = message.content.lower()
        for word in cfg["automod"]["banned_words"]:
            pattern = r'\b' + re.escape(word.lower()) + r'\b'
            if re.search(pattern, content_lower):
                reasons.append(f"запрещённое слово: **{word}**")
                break

        # 2. Проверка массовых упоминаний
        total_mentions = len(message.mentions) + len(message.role_mentions)
        if total_mentions > cfg["automod"]["max_mentions"]:
            reasons.append(f"массовые упоминания ({total_mentions})")

        # 3. Проверка спама
        now = datetime.now(timezone.utc).timestamp()
      
