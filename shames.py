import telegram as tg
from telegram import ext

import config as conf

import ast


def get_shames():
    with open(conf.INVENTORY + 'shames.txt', 'r') as f:
        s = f.read()
        shames = ast.literal_eval(s)
    return shames


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