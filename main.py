import logging
import asyncio

from telegram.ext import Application, ContextTypes

from config import TOKEN
from jobs.scheduler import scheduler, start_scheduler


logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

# Configuration du logger principal
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Créer le logger global
logger = logging.getLogger(__name__)

async def _post_init(app: Application) -> None:
    try:
        loop = asyncio.get_running_loop()

        start_scheduler(app.bot, loop)
        logger.info("Scheduler démarré avec succès")
    except Exception as e:
        logger.warning(f"[Main] Failed to start scheduler: {e}")


def main() -> None:
    app = Application.builder().token(TOKEN).post_init(_post_init).build()

    print("Bot démarré... Appuie sur CTRL+C pour arrêter.")
    app.run_polling()


if __name__ == '__main__':
    main()