"""
Cog системы логирования.
— Логи сообщений: удаление, редактирование
— Логи участников: вход, выход, бан, разбан
— Slash-команды: /setlogchannel /disablelog
"""

from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

import config
from utils.checks import is_admin
from utils.embeds import (
    log_embed, success_embed, error_embed, info_embed,
    COLOR_LOG, COLOR_ERROR, COLOR_SUCCESS, COLOR_WARNING
)


class Logging(commands.Cog):
    """Система логирования событий сервера."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _send_log(self, guild_id: int, embed: discord.Embed):
        """Отправляет embed в канал логов сервера."""
        channel_id = config.get_value(guild_id, "log_channel")
        if not channel_id:
            return
        channel = self.bot.get_channel(channel_id)
        if channel:
            try:
                await channel.send(embed=embed)
            except discord.Forbidden:
                pass

    # ─────────────────────── СОБЫТИЯ СООБЩЕНИЙ ──────────────────────────

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """Лог удалённого сообщения."""
        if not message.guild or message.author.bot:
            return
        if not message.content and not message.attachments:
            return

        e = discord.Embed(
            title="🗑️ Сообщение удалено",
            color=COLOR_ERROR
        )
        e.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
        e.add_field(name="Канал", value=message.channel.mention, inline=True)
        e.add_field(name="Автор", value=f"{message.author.mention} (`{message.author.id}`)", inline=True)
        if message.content:
            content = message.content[:1020] + "..." if len(message.content) > 1020 else message.content
            e.add_field(name="Содержимое", value=content, inline=False)
        if message.attachments:
            names = ", ".join(a.filename for a in message.attachments)
            e.add_field(name="Вложения", value=names, inline=False)
          
