import telegram as tg
from telegram import ext
import requests

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


def echo(update: tg.Update, context: ext.CallbackContext):
    """Tutorial command to echo all messages send."""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
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


