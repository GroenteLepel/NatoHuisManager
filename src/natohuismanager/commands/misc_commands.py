import re
import ast
import random
import datetime
import functools as ft

import telegram as tg
from telegram import ext
import requests

from config import Config



class MiscCommands:
    def __init__(self, dp: ext.updater.Dispatcher, config: Config):
        dp.add_handler(ext.CommandHandler('bop', self.bop))
        dp.add_handler(ext.CommandHandler('start', self.start))
        dp.add_handler(ext.CommandHandler('git', self.git))
        dp.add_handler(
            ext.MessageHandler(
                ext.Filters.regex(re.compile(r'xd', re.IGNORECASE)),
                self.shame_xd
            )
        )

        self.config = config

    def get_url(self):
        contents = requests.get("https://random.dog/woof.json").json()
        image_url = contents['url']
        return image_url


    def bop(self, update: tg.Update, context: ext.CallbackContext):
        """Send random dog picture."""
        url = self.get_url()
        chat_id = update.effective_chat.id
        context.bot.send_photo(chat_id=chat_id, photo=url)


    def start(self, update: tg.Update, context: ext.CallbackContext):
        """Send welcome message."""
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I'm the bot that manages all of Natohuis. Obey me."
        )


    def git(self, update: tg.Update, context: ext.CallbackContext):
        """Send the git repo."""
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="My brain is situated at: "
                "https://github.com/GroenteLepel/NatoHuisManager"
        )


    def shame_xd(self, update: tg.Update, context: ext.CallbackContext):
        max_emojis = 4
        xd_gif = "https://media1.giphy.com/media/3glEquTzrYXVm/giphy.gif?cid=ecf05e473jsk3f9udz4v4jpooz94l6mc5x08l1zbriypyfwi&rid=giphy.gif"
        xd = random.randint(0, max_emojis) * "XD "
        face_tears = random.randint(0, max_emojis) * "😂"
        rofl = random.randint(0, max_emojis) * "🤣"
        ok_hand = random.randint(0, max_emojis) * "👌"
        hundred = random.randint(0, max_emojis) * "💯"
        context.bot.send_animation(
            chat_id=update.effective_chat.id,
            animation=xd_gif,
            caption=f"omg {xd}{face_tears}{ok_hand}{rofl}{hundred}"
        )

