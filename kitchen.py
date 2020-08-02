import telegram as tg
from telegram import ext
import numpy as np

import config
import inventory.koelkast as kk

import time


def open_fridge(update: tg.Update, context: ext.CallbackContext):
    chat_id = update.effective_chat.id
    koelkast = kk.Koelkast.from_file("koelkast.txt")
    context.bot.send_message(chat_id, "Opening fridge, please don't stare"
                                      f" too long... \n{str(koelkast)}")


def pick(update: tg.Update, context: ext.CallbackContext):
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text="Is even kijken wie er dit keer gaat koken..."
    )
    de_lul = np.random.choice(['Margot', 'Tom', 'Thijs', 'Daniël'])
    rand = np.random.rand()
    while rand < 0.5:
        think_msg = np.random.choice([
            "Even denken...",
            "Dit is een moeilijke...",
            "Zal ik gewoon weer Tom kiezen? Misschien wel... Misschien niet...",
            "Jaaaa ik heb 'm bijna..."
        ])
        context.bot.send_chat_action(chat_id, tg.ChatAction.TYPING)
        time.sleep(2 * np.random.rand())
        context.bot.send_message(chat_id, think_msg)
        rand = np.random.rand()
    context.bot.send_chat_action(chat_id, tg.ChatAction.TYPING)
    time.sleep(2 * np.random.rand())
    context.bot.send_message(chat_id, de_lul)


def add_restje(update: tg.Update, context: ext.CallbackContext):
    chat_id = update.effective_chat.id
    koelkast = kk.Koelkast.from_file(config.INVENTORY + "koelkast.txt")
    new_restje = kk.Restje(context.args[0])
    koelkast.add(new_restje)
    context.bot.send_message(
        chat_id,
        "Restje {0:s} added to the koelkast!\n"
        "{1:s}".format(
            new_restje.restje,
            str(koelkast)
        )
    )
    koelkast.save(config.INVENTORY + "koelkast.txt")


def remove_restje(update: tg.Update, context: ext.CallbackContext):
    chat_id = update.effective_chat.id
    koelkast = kk.Koelkast.from_file(config.INVENTORY + "koelkast.txt")
    to_remove = context.args[0]
    msg = koelkast.remove(to_remove)
    context.bot.send_message(
        chat_id,
        f"{msg}\n"
        f"{str(koelkast)}"
    )
    koelkast.save(config.INVENTORY + "koelkast.txt")


def dibs(update: tg.Update, context: ext.CallbackContext):
    chat_id = update.effective_chat.id
    koelkast = kk.Koelkast.from_file(config.INVENTORY + "koelkast.txt")
    restje = context.args[0]
    dibsed_by = update.message.from_user.first_name
    msg = koelkast.dibs(restje, dibsed_by)
    if not msg:
        context.bot.send_message(
            chat_id,
            "Dibsed restje {0:s} for {1:s}".format(
                restje,
                dibsed_by
            )
        )
        koelkast.save(config.INVENTORY + "koelkast.txt")
    else:
        context.bot.send_message(chat_id, msg)

    context.bot.send_message(chat_id, str(koelkast))
