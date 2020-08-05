import telegram as tg
from telegram import ext
import requests
import numpy as np

import database as db

import datetime
import ast
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
    xd = np.random.randint(max_emojis) * "XD "
    face_tears = np.random.randint(max_emojis) * "😂"
    rofl = np.random.randint(max_emojis) * "🤣"
    ok_hand = np.random.randint(max_emojis) * "👌"
    hundred = np.random.randint(max_emojis) * "💯"
    context.bot.send_animation(
        chat_id=update.effective_chat.id,
        animation=xd_gif,
        caption=f"omg {xd}{face_tears}{ok_hand}{rofl}{hundred}"
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


def set_out_for_absents(update: tg.Update, context: ext.CallbackContext):
    """Sets out for all absents from set_out_till() once /start_roll_call
    has been called."""
    absents = ast.literal_eval(db.load("absents.txt"))
    if absents or len(absents) != 0:
        today = datetime.datetime.now()
        chat_id = update.effective_chat.id
        for absent, date_str in absents.items():
            date = datetime.datetime.strptime(date_str, "%d-%m")
            if today.month <= date.month and today.day < date.day:
                context.bot.send_message(
                    chat_id,
                    f"/set_out_for@WhosInBot {absent} weg tot {date_str}"
                )
            else:
                context.bot.send_message(
                    chat_id,
                    f"Removed {absent} from absent list, they should be"
                    f" returning today!"
                )
                del absents[absent]

        db.save("absents.txt", absents)
    else:
        pass


def im_back(update: tg.Update, context: ext.CallbackContext):
    chat_id = update.effective_chat.id
    absents = db.load("absents.txt")
    whos_back = update.message.from_user.first_name
    if whos_back in absents:
        context.bot.send_message(
            chat_id,
            "Alright, I'll remove you from the absent list."
        )
        del absents[whos_back]
        db.save("absents.txt", absents)
    else:
        context.bot.send_message(
            chat_id,
            "Uuhm, you weren't even on my absent list...?"
        )


def set_out_till(update: tg.Update, context: ext.CallbackContext):
    """Call /set_out_for yourself until a certain date when /start_roll_call
    is mentioned."""
    chat_id = update.effective_chat.id
    if len(context.args) < 1 or len(context.args) > 2:
        context.bot.send_message(
            chat_id,
            "Please provide the date and person (optional) to set out for, "
            "like so: \n"
            "/set_out_till [day]-[month] [person_to_set_out (optional)]"
        )
    else:
        # get date from input
        date_str = context.args[0]
        try:
            # try to assign date to datetime object
            date = datetime.datetime.strptime(date_str, "%d-%m")
        except:
            # return nothing if date provided was wrong
            context.bot.send_message(
                chat_id,
                "Date format provided wrong. Please provide it like so:\n"
                "/set_out_till [day]-[month]"
            )
            return

        # get absent person from input / message
        if len(context.args) == 2:
            absent = context.args[1]
        else:
            absent = update.message.from_user.first_name

        # get the current dict of absents
        absents = ast.literal_eval(db.load("absents.txt"))
        # check if there is a value in the file (db.load() returns an empty
        #  string if the file does not exist)
        if absents:
            absents[absent] = date_str
        else:
            absents = {absent: date_str}

        db.save("absents.txt", str(absents))
        context.bot.send_message(
            chat_id,
            f"{absent} has been send on absent until {date_str}. I will make"
            f" sure to set you out for all roll calls until then."
        )


def add_misc_commands(dp: ext.updater.Dispatcher):
    xd_filter = ["XD", "Xd", "xd", "xD", "XXD", "XXXD", "XDD", "xxD"]
    dp.add_handler(ext.CommandHandler('bop', bop))
    dp.add_handler(ext.CommandHandler('start', start))
    dp.add_handler(ext.CommandHandler('git', git))
    dp.add_handler(
        ext.MessageHandler(
            ext.Filters.text(xd_filter),  # filters all except given string
            shame_xd
        )
    )
    dp.add_handler(ext.CommandHandler('caps', caps))
    dp.add_handler(ext.InlineQueryHandler(inline_caps))
    dp.add_handler(
        ext.CommandHandler('set_out_till', set_out_till, pass_args=True))
    # dp.add_handler(
    #     ext.MessageHandler(
    #         ext.Filters.text(
    #             ['/start_roll_call', '/start_roll_call@WhosInBot']
    #         ),
    #         set_out_for_absents
    #     )
    # )
    dp.add_handler(ext.CommandHandler('im_back', im_back))