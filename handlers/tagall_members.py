from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

async def tag_all_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type not in ['group', 'supergroup']:
        await update.message.reply_text("❌ Cette commande doit être utilisée dans un groupe !")
        return

    group_id = update.message.chat.id
    admins = await context.bot.get_chat_administrators(group_id)
    mentions = []
    for admin in admins:
        user = admin.user
        if not user.is_bot:
            name = user.username if user.username else user.first_name
            if admin.status == "creator":
                emoji = "\n👑"  # Créateur
            else:
                emoji = "🛡️"  # Administrateur
            mentions.append(f"{emoji} [{name}](tg://user?id={user.id})")

    if mentions:
        message = (
            "✨ **Salut tout le monde ! Voici les administrateurs du groupe :**\n\n"
            + "\n".join(mentions)
        )
    else:
        message = "⚠️ Aucun administrateur humain trouvé dans ce groupe !"

    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
