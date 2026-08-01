"""
Cog системы тикетов.

Исправления:
- Добавлена CreateTicketView — кнопка «Создать тикет» для панели в канале
- Добавлена команда /ticket panel — размещает панель с кнопкой
- TicketView переработан: кнопки «Закрыть» + «Удалить» в одном view
- Все persistent views регистрируются через bot.add_view() в __init__
- Улучшена обработка ошибок (try/except + HTTP fallbacks)
- Создатель тикета может закрыть/удалить свой тикет
- Логирование всех действий
"""

import asyncio
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

import config
from utils.checks import is_admin, is_moderator
from utils.embeds import (
    ticket_embed, success_embed, error_embed, info_embed, log_embed
)


# ─────────────────────────────────────────────────────────────────────────────
#  Вспомогательные функции
# ─────────────────────────────────────────────────────────────────────────────

def _get_creator_id(channel: discord.TextChannel) -> int | None:
    """Извлекает ID создателя тикета из имени канала (ticket-{user_id})."""
    try:
        return int(channel.name.split("-", 1)[1])
    except (IndexError, ValueError):
        return None


async def _send_ticket_log(guild: discord.Guild, action: str, ticket_name: str,
                            actor: discord.Member | discord.User,
                            description: str = "") -> None:
    """Отправляет лог тикета в канал логов."""
    log_ch_id = (
        config.get_value(guild.id, "ticket_log_channel")
        or config.get_value(guild.id, "log_channel")
    )
    if not log_ch_id:
        return
    channel = guild.get_channel(log_ch_id)
    if not channel:
        return

    action_text = {
        "opened":  "🎫 Тикет открыт",
        "closed":  "🔒 Тикет закрыт",
        "deleted": "🗑️ Тикет удалён",
        "claimed": "👋 Тикет принят в работу",
    }.get(action, f"🎫 {action}")

    e = log_embed(
        action_text,
        description or f"**Канал:** `{ticket_name}`\n**Действие:** {actor.mention}"
    )
                              
