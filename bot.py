import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN n'est pas défini dans les variables d'environnement.")

def generate_fake_identity():
    prenoms = ["Lucas", "Emma", "Nathan", "Chloé", "Léo", "Inès"]
    noms = ["Martin", "Bernard", "Dubois", "Thomas", "Robert"]
    villes = ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"]
    age = random.randint(18, 50)

    return f"👤 Identité : {random.choice(prenoms)} {random.choice(noms)}\n🏙️ Ville : {random.choice(villes)}\n🎂 Âge : {age} ans"

async def fakeid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = generate_fake_identity()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("fakeid", fakeid))
    print("🤖 Bot en ligne.")
    app.run_polling()

if __name__ == '__main__':
    main()
