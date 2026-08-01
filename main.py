import discord
from discord.ext import commands
import os

from config import TOKEN


# Все разрешения для функций бота
intents = discord.Intents.all()


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)
async def load_cogs():
    await bot.load_extension("cogs.admin")
    await bot.load_extension("cogs.logging")
    await bot.load_extension("cogs.moderation")
    await bot.load_extension("cogs.tickets")

@bot.event
async def on_ready():
    print("==============================")
    print(f"✅ Бот запущен: {bot.user}")
    print(f"🆔 ID: {bot.user.id}")
    print("==============================")

    await load_cogs()


    # Синхронизация Slash-команд
    try:
        synced = await bot.tree.sync()
        print(f"✅ Slash-команд загружено: {len(synced)}")
    except Exception as e:
        print(f"❌ Ошибка синхронизации команд: {e}")

@bot.event
async def on_command_error(ctx, error):
    print(f"Ошибка команды: {error}")


if TOKEN is None:
    print("❌ Токен не найден!")
    print("Добавь TOKEN в Replit Secrets")

else:
    bot.run(TOKEN)
         
