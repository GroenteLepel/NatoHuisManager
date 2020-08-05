import time
import random
import logging
import traceback

import telegram as tg
from telegram import ext

from natohuismanager.inventory import Koelkast
from natohuismanager.database import Database
from config import Config


class Kitchen:
    def __init__(self, dp: ext.updater.Dispatcher, config: Config, db: Database):
        dp.add_handler(ext.CommandHandler('wie_is_de_lul', self.pick))
        dp.add_handler(ext.CommandHandler('open_fridge', self.open_fridge))
        dp.add_handler(ext.CommandHandler('add_restje', self.add_restje, pass_args=True))
        dp.add_handler(ext.CommandHandler('remove_restje', self.remove_restje, pass_args=True))
        dp.add_handler(ext.CommandHandler('dibs', self.dibs, pass_args=True))

        self.logger = logging.getLogger(__name__)
        self.config = config
        self.koelkast = Koelkast(db)

    def open_fridge(self, update: tg.Update, context: ext.CallbackContext):
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id, "Opening fridge, please don't stare"
                                        f" too long... \n{self.koelkast.to_string()}")

    def pick(self, update: tg.Update, context: ext.CallbackContext):
        chat_id = update.effective_chat.id
        context.bot.send_message(
            chat_id=chat_id,
            text="Is even kijken wie er dit keer gaat koken..."
        )
        de_lul = random.choice(self.config["INHABITANTS"])
        rand = random.random()
        while rand < 0.5:
            think_msg = random.choice([
                "Even denken...",
                "Dit is een moeilijke...",
                "Zal ik gewoon weer Tom kiezen? Misschien wel... Misschien niet...",
                "Jaaaa ik heb 'm bijna..."
            ])
            context.bot.send_chat_action(chat_id, tg.ChatAction.TYPING)
            time.sleep(2 * random.random())
            context.bot.send_message(chat_id, think_msg)
            rand = random.random()
        context.bot.send_chat_action(chat_id, tg.ChatAction.TYPING)
        time.sleep(2 * random.random())
        context.bot.send_message(chat_id, de_lul)

    def add_restje(self, update: tg.Update, context: ext.CallbackContext):
        chat_id = update.effective_chat.id

        if len(context.args) == 0:
            context.bot.send_message(
                chat_id,
                "Please provide the restje which you want to add:\n"
                "like so: /add_restje [restje]"
            )
        else:
            try:
                self.koelkast.add(context.args[0])
            except:
                context.bot.send_message(
                    chat_id,
                    "Failed to add a restje to the koelkast, ask Daniël to look at the logs."
                )
                self.logger.error("Failed to add a restje to the koelkast: " + traceback.format_exc())
                return

            context.bot.send_message(
                chat_id,
                "Restje {0:s} added to the koelkast!\n"
                "{1:s}".format(
                    context.args[0],
                    self.koelkast.to_string()
                )
            )

    def remove_restje(self, update: tg.Update, context: ext.CallbackContext):
        chat_id = update.effective_chat.id

        if len(context.args) == 0:
            context.bot.send_message(
                chat_id,
                "Please provide the restje which you want to remove:\n"
                "like so: /remove_restje [restje]"
            )
        else:
            to_remove = context.args[0]
            msg = self.koelkast.remove(to_remove)
            context.bot.send_message(
                chat_id,
                f"{msg}\n"
                f"{self.koelkast.to_string()}"
            )


    def dibs(self, update: tg.Update, context: ext.CallbackContext):
        chat_id = update.effective_chat.id

        if len(context.args) == 0:
            context.bot.send_message(
                chat_id,
                "Please provide the restje which you want to dibs:\n"
                "like so: /dibse [restje] [person_to_dibs (optional)]"
            )
        else:
            restje = context.args[0]
            if len(context.args) > 1:
                dibsed_by = context.args[1]
            else:
                dibsed_by = update.message.from_user.first_name
            msg = self.koelkast.dibs(restje, dibsed_by)
            if not msg:
                context.bot.send_message(
                    chat_id,
                    "Dibsed restje {0:s} for {1:s}".format(
                        restje,
                        dibsed_by
                    )
                )
            else:
                context.bot.send_message(chat_id, msg)

            context.bot.send_message(chat_id, self.koelkast.to_string())
