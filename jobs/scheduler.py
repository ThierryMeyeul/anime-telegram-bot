import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from telegram import Bot

from config import CHANNEL_ID
from services.anime_service import get_random_quote


scheduler = AsyncIOScheduler()


async def post_quote(bot: Bot):
    quote_msg = get_random_quote()
    await bot.send_message(chat_id=CHANNEL_ID, text=quote_msg, parse_mode=ParseMode.MARKDOWN)


def start_scheduler(bot, loop):
    def job_wrapper():
        # Exécute la coroutine dans la boucle existante
        asyncio.run_coroutine_threadsafe(post_quote(bot), loop)

    scheduler.add_job(
        job_wrapper,
        CronTrigger(second=0),
        # id='quote_every_6h',
        # replace_existing=True
    )

    if not scheduler.running:
        scheduler.start()
