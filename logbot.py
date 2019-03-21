# -*- coding: utf-8 -*-
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import sqlite3

update_id = None


def main():
    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot('')

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            log(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def log(bot):
    """Echo the message the user sent."""
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        print (update.message)
        if update.message:  # your bot can receive updates without messages
            line = update.message.text
            if line:
                if line.startswith("/gethistory "):
                    update.message.reply_text("http://logbot.ko-lab.space/hashtag/" + str(update.message.chat.id) + "/" + str(line.split()[1].replace("#","")))
                elif line.startswith("/gethistory"):
                    update.message.reply_text("Please specifiy the hashtag you want a history for. Example: '/gethistory example'")

                for j in [i[1:] for i in line.split() if i.startswith("#")]:
                    if j:
                        conn = sqlite3.connect('/home/warddr/logbot/db.sqlite3')
                        c = conn.cursor()
                        c.execute('''INSERT INTO hashtags(user_id, user_name, user_first, user_last, message, hashtag, chat_id, sqltime) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (update.message.from_user.id, update.message.from_user.username, update.message.from_user.first_name, update.message.from_user.last_name, update.message.text, j, update.message.chat.id, update.message.date))
                        conn.commit()
                        conn.close()


if __name__ == '__main__':
    main()

