import telebot
import os
from instagram import download_post, get_caption
import shutil
import subprocess
import time

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, "HTML")

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, f"Hello {message.from_user.first_name}")


@bot.message_handler(regexp="(https?:\\/\\/)?(www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%_\\+.~#?&//=]*)?")
def instagram(message):
    link = message.text
    is_successful, path = download_post(link)
    caption,videos,photos = get_caption(is_successful,path)
    if len(videos)>0:
        media_group = [telebot.types.InputMediaVideo(open(file, 'rb')) for file in videos]
        media_group[0].caption = caption
        bot.send_media_group(message.chat.id, media_group)
    else:
        media_group = [telebot.types.InputMediaPhoto(open(file, 'rb')) for file in photos]
        media_group[0].caption = caption
        bot.send_media_group(message.chat.id, media_group)
    
    print(path)

    time.sleep(5)

    command = ["rmdir", "/s", "/q", f".\\{path}"]
    subprocess.run(command, shell=True)
        


if __name__ == "__main__":

    print("Bot is online")
    bot.polling()