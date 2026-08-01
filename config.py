"""
Система конфигурации серверов.
Хранит настройки каждого сервера в отдельном JSON-файле.
"""

import json
import os
from typing import Any, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "guilds")


def _guild_path(guild_id: int) -> str:
    os.makedirs(DATA_DIR, exist_ok=True)
    return os.path.join(DATA_DIR, f"{guild_id}.json")


# Настройки по умолчанию для нового сервера
DEFAULT_CONFIG = {
    # Каналы
    "log_channel": None,          # ID канала логов
    "ticket_category": None,      # ID категории для тикетов
    "ticket_log_channel": None,   # ID канала логов тикетов

    # Модерация
    "automod": {
        "enabled": True,
        "spam_threshold": 5,       # сообщений за интервал
        "spam_interval": 5,        # секунд
        "max_mentions": 5,         # максимум упоминаний в одном сообщении
        "banned_words": [],        # список запрещённых слов
        "log_channel": None,       # отдельный канал для авто-мода (если None → log_channel)
    },

    # Наказания (escalation по количеству предупреждений)
    "punishments": {
        "1": "warn",
        "2": "warn",
        "3": "mute_10",    # мут 10 минут
        "4": "mute_60",    # мут 60 минут
        "5": "kick",
        "6": "ban",
    },

    # Роли
    "mute_role": None,            # ID роли для мута
    "mod_roles": [],              # ID ролей модераторов
    "admin_roles": [],            # ID ролей администраторов

    # Счётчик тикетов
    "ticket_counter": 0,

    # Предупреждения пользователей: {user_id: [{"reason": ..., "time": ...}]}
    "warnings": {},
}


def load_config(guild_id: int) -> dict:
    """Загружает конфигурацию сервера. Создаёт дефолтную если не существует."""
    path = _guild_path(guild_id)
    if not os.path.exists(path):
        save_config(guild_id, DEFAULT_CONFIG.copy())
        return DEFAULT_CONFIG.copy()
      
