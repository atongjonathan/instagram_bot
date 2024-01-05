import telebot
import os
from instagram import download_post, get_caption, download_story
import subprocess
import pathlib

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, "HTML")



def send_items(is_successful, path, chat_id):
    caption,videos,photos = get_caption(is_successful,path)
    for media in photos:
        with open(media, "rb") as file:
            bot.send_photo(chat_id, file, caption)
    for media in videos:
        with open(media, "rb") as file:
            bot.send_video(chat_id, file, caption)
    this_path = pathlib.Path(__file__).resolve()
    parent_path = this_path.parent
    full_path = parent_path/path
    print(full_path)
    command = ["rmdir", "/s", "/q", f"{full_path}"]
    subprocess.run(command, shell=True)
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, f"Hello {message.from_user.first_name}")

@bot.message_handler(regexp="^@")
def story(message):
    delete = bot.reply_to(message, "Downloading story...")
    text = message.text
    username = text.split("@")[1]
    is_successful, path = download_story(username)
    send_items(is_successful,path, message.chat.id)  
    bot.delete_message(message.chat.id, delete.id)  
    


@bot.message_handler(regexp="(https?:\\/\\/)?(www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%_\\+.~#?&//=]*)?")
def instagram(message):
    check = bot.reply_to(message, "Checking link")
    link = message.text
    is_successful, path = download_post(link)
    send_items(is_successful,path, message.chat.id)
    bot.delete_message(message.chat.id,check.id)
    

        


if __name__ == "__main__":

    print("Bot is online")
    bot.polling()