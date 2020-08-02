import telegram as tg
from telegram import ext

import config as conf
import database as db

import ast


def is_int(s):
    """Checks if string is an int."""
    try:
        int(s)
        return True
    except ValueError:
        return False


def get_shames():
    """Gets the shame dict from shames.txt in INVENTORY folder (see config)."""
    s = db.load("shames.txt")
    shames = ast.literal_eval(s)
    return shames


def init_shames(update: tg.Update, context: ext.CallbackContext):
    shames = {'Margot': 0, 'Thijs': 0, 'Daniël': 0, 'Tom': 0}
    db.save("shames.txt", str(shames))
    context.bot.send_message(
        update.effective_chat.id,
        f"shames init to {str(shames)}."
    )


def write_shames(new_shames: dict):
    """Writes new_shames to shames.txt in INVENTORY folder (see config)."""
    db.save("shames.txt", str(new_shames))


def shame(update: tg.Update, context: ext.CallbackContext):
    """Increases provided user's shame counter by 1."""
    chat_id = update.effective_chat.id
    shames = get_shames()
    if len(context.args) == 0:
        context.bot.send_message(
            chat_id=chat_id,
            text="Please provide a person to shame."
        )
    elif context.args[0] in shames:
        shames[context.args[0]] += 1
        shame_gif = "https://media.giphy.com/media/W81qSImkIxkNq/giphy.gif"

        try:
            write_shames(shames)

            context.bot.send_animation(
                chat_id=chat_id,
                animation=shame_gif,
                caption="Shame on you, {0:s}! Your"
                        " shame count is now {1:d}.".format(
                            context.args[0],
                            shames[context.args[0]]
                )
            )
        except IOError:
            "Something went wrong finding the shames.txt."
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="User \"{0:s}\" not found in my shames-tab.".format(
                context.args[0]
            )
        )


def redeem(update: tg.Update, context: ext.CallbackContext):
    """Redeems provided number of shames.

    /redeem [person_to_redeem (optional)] [n_to_redeem (optional)]
    Notes:
        if no value is passed, one shame is redeemed for the user sending the
        command;
        if a value is passed, this value of shames is redeemed;
        the person calling this command can also give the name of another
        person to redeem, with an optional second value as the number of
        redeemed shames.
    """
    chat_id = update.effective_chat.id
    shames = get_shames()
    if len(context.args) == 0:
        # /redeem
        n_to_redeem = 1
        redeemed_soul = update.message.from_user.first_name
    elif is_int(context.args[0]):
        # /redeem [number_redeemed_shames]
        n_to_redeem = int(context.args[0])
        redeemed_soul = update.message.from_user.first_name
    elif context.args[0] in shames:
        # /redeem [person_to_redeem] [number_of_redeemed_shames (optional)]
        if len(context.args) == 1:
            # no number_of_redeemed_shames given
            n_to_redeem = 1
        elif is_int(context.args[1]):
            n_to_redeem = int(context.args[1])
        else:
            context.bot.send_message(
                chat_id=chat_id,
                text="Please provide a proper number of shames to redeem."
            )
            return

        redeemed_soul = context.args[0]
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="Please provide a proper number of shames to redeem."
        )
        return

    shames[redeemed_soul] -= n_to_redeem
    if shames[redeemed_soul] < 0:
        shames[redeemed_soul] = 0
    write_shames(shames)
    context.bot.send_message(
        chat_id=chat_id,
        text="{0:d} shame(s) redeemed. Good job! Current shame count "
             "for {1:s} is now {2:d}.".format(
                n_to_redeem,
                redeemed_soul,
                shames[redeemed_soul]
        )
    )


def set_shame_counter(update: tg.Update, context: ext.CallbackContext):
    """Sets shame counter

    /set_shame_counter [person_to_set] [shame_value]
    """
    chat_id = update.effective_chat.id
    shames = get_shames()
    # check if the person trying this command is the one and only
    if update.message.from_user.username == 'KoffieKopje':
        # check if the right syntax is used
        if len(context.args) <= 1:
            context.bot.send_message(
                chat_id=chat_id,
                text="Please provide the right info, like this:\n"
                     "/set_shame_counter <person> <new_shame_value>"
            )
        elif context.args[0] in shames:
            if not is_int(context.args[1]):
                context.bot.send_message(
                    chat_id=chat_id,
                    text="Please provide a valid number to set the"
                         " shame counter to."
                )
            else:
                shames[context.args[0]] = int(context.args[1])
                context.bot.send_message(
                    chat_id=chat_id,
                    text="User {0:s}'s shame count set to {1:d}".format(
                        context.args[0],
                        int(context.args[1])
                    )
                )
                write_shames(shames)
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
    """Sends the shame list in decreasing order as message."""
    chat_id = update.effective_chat.id
    shames = get_shames()
    shames_sorted = \
        sorted(shames.items(), key=lambda item: item[1], reverse=True)
    scoreboard = "<b>Shame scoreboard:</b>\n"
    for i, item in enumerate(shames_sorted):
        scoreboard += "{0:d}. {1:s}: {2:d} shame".format(
            i+1, item[0], item[1]
        )
        if item[1] == 1:
            scoreboard += "\n"
        else:
            scoreboard += "s\n"

    context.bot.send_message(
        chat_id=chat_id,
        text=scoreboard,
        parse_mode="html"
    )
