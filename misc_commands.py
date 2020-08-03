import telegram as tg
from telegram import ext
import requests
import numpy as np

import functools as ft


def get_url():
    contents = requests.get("https://random.dog/woof.json").json()
    image_url = contents['url']
    return image_url


def bop(update: tg.Update, context: ext.CallbackContext):
    """Send random dog picture."""
    url = get_url()
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=url)


def start(update: tg.Update, context: ext.CallbackContext):
    """Send welcome message."""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm the bot that manages all of Natohuis. Obey me."
    )


def git(update: tg.Update, context: ext.CallbackContext):
    """Send the git repo."""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="My brain is situated at: "
             "https://github.com/GroenteLepel/NatoHuisManager"
    )


def shame_xd(update: tg.Update, context: ext.CallbackContext):
    """Tutorial command to echo all messages send."""
    max_emojis = 4
    xd_gif = "https://media1.giphy.com/media/3glEquTzrYXVm/giphy.gif?cid=ecf05e473jsk3f9udz4v4jpooz94l6mc5x08l1zbriypyfwi&rid=giphy.gif"
    face_tears = np.random.randint(max_emojis) * "😂"
    rofl = np.random.randint(max_emojis) * "🤣"
    ok_hand = np.random.randint(max_emojis) * "👌"
    hundred = np.random.randint(max_emojis) * "💯"
    context.bot.send_animation(
        chat_id=update.effective_chat.id,
        animation=xd_gif,
        caption=f"omg XD XD XD {face_tears}{ok_hand}{rofl}{hundred}"
    )


def caps(update: tg.Update, context: ext.CallbackContext):
    """Echos the send text in caps."""
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def inline_caps(update: tg.Update, context: ext.CallbackContext):
    """Inline command to change text to all caps."""
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        tg.InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=tg.InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


