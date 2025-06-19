import os
import random
import string
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# Récupérer le token et le mot de passe secret depuis les variables d'environnement
BOT_TOKEN = os.getenv("BOT_TOKEN")
SECRET_PASSWORD = os.getenv("SECRET_PASSWORD")

if not BOT_TOKEN or not SECRET_PASSWORD:
    raise ValueError("❌ BOT_TOKEN ou SECRET_PASSWORD non défini dans les variables d'environnement.")

# Liste des utilisateurs connectés (en mémoire)
authorized_users = set()

def generate_fake_identity():
    prenoms = ["Hery", "Fanja", "Tahina", "Lalao", "Mamy", "Soa"]
    noms = ["Ratsimbazafy", "Rakoto", "Andrianarivo", "Rasolofo", "Rakotomalala"]
    villes = ["Antananarivo", "Toamasina", "Fianarantsoa", "Mahajanga", "Toliara"]
    metiers = ["Mpampianatra", "Dokotera", "Mpivarotra", "Mpanamboatra", "Mpilalao baolina kitra"]

    age = random.randint(18, 50)
    prenom = random.choice(prenoms)
    nom = random.choice(noms)
    ville = random.choice(villes)
    metier = random.choice(metiers)

    email = f"{prenom.lower()}.{nom.lower()}@mail.mg"
    tel = f"034 {random.randint(10,99)} {random.randint(100,999)} {random.randint(100,999)}"
    mot_de_passe = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    return (f"👤 Anarana : {prenom} {nom}\n"
            f"🏙️ Tanàna : {ville}\n"
            f"🎂 Taona : {age} taona\n"
            f"💼 Asa : {metier}\n"
            f"📧 Email : {email}\n"
            f"📞 Téléphone : {tel}\n"
            f"🔑 Mot de passe : {mot_de_passe}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salama! Mba midira amin'ny alalan'ny /login <tenimiafina> mba hahazoana miditra."
    )

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Fampiasana: /login <tenimiafina>")
        return
    mdp = context.args[0]
    if mdp == SECRET_PASSWORD:
        authorized_users.add(update.effective_chat.id)
        await update.message.reply_text("✅ Vita ny fidirana! Afaka mampiasa /fakeid ianao izao.")
    else:
        await update.message.reply_text("❌ Diso ny tenimiafina.")

async def fakeid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id not in authorized_users:
        await update.message.reply_text("❌ Tsy maintsy miditra aloha amin'ny /login <tenimiafina> ianao.")
        return
    message = generate_fake_identity()
    photo_url = "https://thispersondoesnotexist.com/image"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("login", login))
    app.add_handler(CommandHandler("fakeid", fakeid))

    print("🤖 Bot en ligne.")
    app.run_polling()

if __name__ == "__main__":
    main()
