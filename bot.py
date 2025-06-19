import os
import random
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Charge les variables depuis le fichier .env (utile localement)
load_dotenv()

# Lit le token depuis l'environnement
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN non défini dans les variables d'environnement.")

def generate_fake_identity():
    prenoms = ["Lucas", "Emma", "Nathan", "Chloé", "Léo", "Inès"]
    noms = ["Martin", "Bernard", "Dubois", "Thomas", "Robert"]
    villes = ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"]
    age = random.randint(18, 50)

    return f"👤 Identité : {random.choice(prenoms)} {random.choice(noms)}\n🏙️ Ville : {random.choice(villes)}\n🎂 Âge : {age} ans"

async def fakeid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = generate_fake_identity()

    # URL d'une image de visage IA aléatoire
    photo_url = "https://thispersondoesnotexist.com/image"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("fakeid", fakeid))
    print("🤖 Bot en ligne.")
    app.run_polling()

if __name__ == '__main__':
    main()
