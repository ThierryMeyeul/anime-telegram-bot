import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from telegram import Bot

from config import CHANNEL_ID
from services.anime_service import get_random_quote, get_weekly_schedule

scheduler = AsyncIOScheduler()


async def post_quote(bot: Bot):
    quote_msg = get_random_quote()
    await bot.send_message(chat_id=CHANNEL_ID, text=quote_msg, parse_mode=ParseMode.MARKDOWN)


async def post_weekly_schedule(bot: Bot):
    schedule = get_weekly_schedule()
    message = "<b>📅 Programme des animés pour la semaine :</b>\n\n"

    for day, animes in schedule.items():
        message += f"✨<i>{day}</i>✨\n"
        if animes:
            message += "\n".join(animes) + "\n\n"
        else:
            message += "Aucun anime prévu.\n\n"

    if len(message) > 4000:
        message = message[:4000] + "\n\n⚠️ Message tronqué (trop long)."

    await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode=ParseMode.HTML)


def start_scheduler(bot, loop):
    def job_wrapper():
        # Exécute la coroutine dans la boucle existante
        asyncio.run_coroutine_threadsafe(post_quote(bot), loop)

    scheduler.add_job(
        job_wrapper,
        CronTrigger(hour='*/6', minute=0, second=0),
        id='quote_every_6h',
        replace_existing=True
    )

    def anime_weekly_wrapper():
        asyncio.run_coroutine_threadsafe(post_weekly_schedule(bot), loop)

    scheduler.add_job(
        anime_weekly_wrapper,
        CronTrigger(day_of_week='sun', hour=20, minute=0),
        id='weekly_anime_schedule',
        replace_existing=True
    )


    if not scheduler.running:
        scheduler.start()
