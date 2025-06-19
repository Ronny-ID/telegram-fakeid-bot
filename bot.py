import random
import requests
from io import BytesIO
from faker import Faker
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

faker = Faker()

def generate_identity():
    sex = random.choice(['male', 'female'])
    name = faker.name_male() if sex == 'male' else faker.name_female()
    dob = faker.date_of_birth(minimum_age=18, maximum_age=60)
    job = faker.job()
    city = faker.city()
    country = faker.country()

    message = (
        f"👤 Identité générée :\n\n"
        f"Nom : {name}\n"
        f"Sexe : {sex}\n"
        f"Né(e) le : {dob}\n"
        f"Ville : {city}\n"
        f"Pays : {country}\n"
        f"Métier : {job}\n"
    )

    return message

async def fakeid_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    identity_message = generate_identity()
    try:
        response = requests.get("https://thispersondoesnotexist.com/", headers={"User-Agent": "Mozilla/5.0"})
        photo_bytes = BytesIO(response.content)
        photo_bytes.seek(0)

        await context.bot.send_message(chat_id=update.effective_chat.id, text=identity_message)
        await asyncio.sleep(1)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_bytes)

    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Erreur : " + str(e))

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("fakeid", fakeid_handler))
    print("🤖 Bot en ligne.")
    app.run_polling()

if __name__ == "__main__":
    main()