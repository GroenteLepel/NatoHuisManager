import telegram.ext as ext
import telegram as tg
import requests
import numpy as np

import time
import ast
import collections

NATOHUISBOT_TOKEN = '1156628740:AAFROcmqib7rdBQUY7NE2Zi2X85LEGpPRFw'
INV = "inventory/"

def get_url():
    contents = requests.get("https://random.dog/woof.json").json()
    image_url = contents['url']
    return image_url


def get_shames():
    with open(INV + 'shames.txt', 'r') as f:
        s = f.read()
        shames = ast.literal_eval(s)
    return shames


def bop(bot, update):
    url = get_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)


def start(update: tg.Update, context: ext.CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm the bot that manages all of Natohuis. Obey me."
    )


def echo(update: tg.Update, context: ext.CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
    )


def caps(update: tg.Update, context: ext.CallbackContext):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def inline_caps(update: tg.Update, context: ext.CallbackContext):
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


def pick(update: tg.Update, context: ext.CallbackContext):
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text="Is even kijken wie er dit keer gaat koken..."
    )
    time.sleep(2 * np.random.rand())
    de_lul = np.random.choice(['Margot', 'Tom', 'Thijs', 'Daniël'])
    rand = np.random.rand()
    while rand < 0.5:
        think_msg = np.random.choice([
            "Even denken...",
            "Dit is een moeilijke...",
            "Zal ik gewoon weer Tom kiezen? Misschien wel... Misschien niet...",
            "Jaaaa ik heb 'm bijna..."
        ])
        context.bot.send_message(chat_id, think_msg)
        time.sleep(2 * np.random.rand())
        rand = np.random.rand()
    context.bot.send_message(chat_id, de_lul)


def shame(update: tg.Update, context: ext.CallbackContext):
    chat_id = update.effective_chat.id
    shames = get_shames()
    if context.args[0] in shames:
        shames[context.args[0]] += 1
        context.bot.send_message(
            chat_id=chat_id,
            text="Shame on you, {0:s}. Your shame count is now {1:d}.".format(
                context.args[0],
                shames[context.args[0]]
            )
        )

        with open(INV + 'shames.txt', 'w') as f:
            f.write(str(shames))
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="User \"{0:s}\" not found in my shames-tab.".format(
                context.args[0]
            )
        )


def set_shame_counter(update: tg.Update, context: ext.CallbackContext):
    chat_id = update.effective_chat.id
    shames = get_shames()
    if update.message.from_user.username == 'KoffieKopje':
        if context.args[0] in shames:
            shames[context.args[0]] = int(context.args[1])
            context.bot.send_message(
                chat_id=chat_id,
                text="User {0:s}'s shame count set to {1:d}".format(
                    context.args[0],
                    int(context.args[1])
                )
            )
            with open(INV + 'shames.txt', 'w') as f:
                f.write(str(shames))
        else:
            context.bot.send_message(
                chat_id=chat_id,
                text="User \"{0:s}\" not found in my shames-tab".format(
                    context.args[0]
                )
            )

    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="You are not allowed to do that. Shame on you!"
        )


def get_shame_list(update: tg.Update, context: ext.CallbackContext):
    chat_id = update.effective_chat.id
    shames = get_shames()
    shames_sorted = \
        {k: v for k, v in sorted(shames.items(), key=lambda item: item[1])}
    context.bot.send_message(
        chat_id=chat_id,
        text=str(shames_sorted)
    )


def main():
    updater = ext.Updater(NATOHUISBOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(ext.CommandHandler('start', start))
    # dp.add_handler(
    #     ext.MessageHandler(
    #         ext.Filters.text & (~ext.Filters.command),  # filters all commands
    #         echo
    #     )
    # )
    dp.add_handler(ext.CommandHandler('caps', caps))
    dp.add_handler(ext.InlineQueryHandler(inline_caps))
    dp.add_handler(ext.CommandHandler('bop', bop))
    dp.add_handler(ext.CommandHandler('wie_is_de_lul', pick))
    dp.add_handler(ext.CommandHandler('shame', shame, pass_args=True))
    dp.add_handler(ext.CommandHandler('set_shame_counter', set_shame_counter, pass_args=True))
    dp.add_handler(ext.CommandHandler('get_shame_list', get_shame_list))
    updater.start_polling()  # starts the bot
    updater.idle()


if __name__ == '__main__':
    main()
