"""
Cog административных команд.
— /help        — список всех команд
— /serverinfo  — информация о сервере
— /userinfo    — информация о пользователе
— /botinfo     — информация о боте
— /ping        — задержка бота
— /config      — просмотр настроек сервера
— /setup       — быстрая настройка бота
— /roles       — управление ролями модераторов/администраторов
"""

import platform
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

import config
from utils.checks import is_admin
from utils.embeds import (
    info_embed, success_embed, error_embed, mod_embed,
    COLOR_INFO, COLOR_SUCCESS
)


class Admin(commands.Cog):
    """Административные команды."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="пинг", description="Показать задержку бота")
    async def ping(self, interaction: discord.Interaction):
        latency_ms = round(self.bot.latency * 1000)
        color = COLOR_SUCCESS if latency_ms < 100 else 0xF39C12 if latency_ms < 200 else 0xE74C3C
        e = discord.Embed(title="🏓 Понг!", color=color)
        e.add_field(name="WebSocket", value=f"**{latency_ms}ms**", inline=True)
        await interaction.response.send_message(embed=e)

    @app_commands.command(name="бот-инфо", description="Информация о боте")
    async def botinfo(self, interaction: discord.Interaction):
        bot = self.bot
        e = discord.Embed(title=f"ℹ️ {bot.user.name}", color=COLOR_INFO)
        e.set_thumbnail(url=bot.user.display_avatar.url)
        e.add_field(name="Серверов",   value=str(len(bot.guilds)),   inline=True)
        e.add_field(name="Пользователей", value=str(sum(g.member_count for g in bot.guilds)), inline=True)
        e.add_field(name="Задержка",   value=f"{round(bot.latency * 1000)}ms", inline=True)
        e.add_field(name="Python",     value=platform.python_version(), inline=True)
        e.add_field(name="discord.py", value=discord.__version__, inline=True)
        e.add_field(name="Платформа",  value=platform.system(), inline=True)
        e.set_footer(text=f"ID: {bot.user.id}")
        e.timestamp = datetime.utcnow()
        await interaction.response.send_message(embed=e)
      
