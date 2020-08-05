import telegram as tg
import telegram.ext as ext

import database as db

import datetime
import ast

SILENCED = False


def louder(update: tg.Update, context: ext.CallbackContext):
    global SILENCED
    SILENCED = True
    context.bot.send_message(
        update.effective_chat.id,
        "HUZZAH I'M FREE 🗣"
    )


def ssh(update: tg.Update, context: ext.CallbackContext):
    global SILENCED
    SILENCED = False
    context.bot.send_message(
        update.effective_chat.id,
        "Fine, I'll be quiet 🤐"
    )


def init_roll_call():
    global SILENCED
    SILENCED = False
    roll_call = {}
    db.save("roll_call.txt", str(roll_call))
    return roll_call


def print_roll_call(roll_call):
    roll_call_str = ""
    if 'title' in roll_call:
        roll_call_str += f"{roll_call['title']}\n"

    if 'reasons' in roll_call:
        reasons = roll_call['reasons']
    else:
        reasons = None

    for in_out in ['in', 'out']:
        if in_out in roll_call:
            roll_call_str += f"{in_out.capitalize()}:\n"
            for person in roll_call[in_out]:
                if reasons and person in reasons:
                    reason = f" ({reasons[person]})"
                else:
                    reason = ""
                roll_call_str += f" - {person}{reason}"
            roll_call_str += "\n"
    return roll_call_str


def start_roll_call(update: tg.Update, context: ext.CallbackContext):
    roll_call = init_roll_call()
    if len(context.args) != 0:
        roll_call['title'] = ' '.join(context.args)

    context.bot.send_message(
        update.effective_chat.id,
        "Roll call started."
    )

    db.save("roll_call.txt", str(roll_call))


def end_roll_call(update: tg.Update, context: ext.CallbackContext):
    roll_call_str = db.load("roll_call.txt")
    if roll_call_str:
        chat_id = update.effective_chat.id
        roll_call = ast.literal_eval(roll_call_str)
        context.bot.send_message(
            chat_id,
            "Ended roll call, I'll send the results."
        )
        context.bot.send_message(
            chat_id,
            print_roll_call(roll_call)
        )
    init_roll_call()


def set_title(update: tg.Update, context: ext.CallbackContext):
    chat_id = update.effective_chat.id
    if len(context.args) == 0:
        context.bot.send_message(
            chat_id,
            "Please provide a title to set."
        )
    else:
        roll_call_str = db.load("roll_call.txt")
        if roll_call_str:
            roll_call = ast.literal_eval(roll_call_str)
            roll_call['title'] = ' '.join(context.args)
            if not SILENCED:
                context.bot.send_message(
                    chat_id,
                    f"Roll call title has been set to {roll_call['title']}."
                )
        else:
            context.bot.send_message(
                chat_id,
                "No roll call has been found."
            )


def set_in(update: tg.Update, context: ext.CallbackContext):
    chat_id = update.effective_chat.id
    # read in who's to enroll
    to_enroll = update.message.from_user.first_name
    # if a reason has been given, read this in.
    if len(context.args) != 0:
        reason = ' '.join(context.args)
    else:
        reason = None

    roll_call = ast.literal_eval(db.load("roll_call.txt"))

    # remove old reason if it exists
    if 'reasons' in roll_call:
        if to_enroll in roll_call['reasons']:
            roll_call['reasons'].remove(to_enroll)

    # if person was in the 'out' list before, remove them
    if 'out' in roll_call:
        if to_enroll in roll_call['out']:
            roll_call['out'].remove(to_enroll)

    # add person to 'in' list
    roll_call['in'].append(to_enroll)
    # add a reason if given
    if reason:
        if 'reasons' not in roll_call:
            # create reason dict if it does not exist yet
            roll_call['reasons'] = {}
        roll_call['reasons'][to_enroll] = reason

    if not SILENCED:
        context.bot.send_message(
            chat_id,
            f"{to_enroll} has been added to the list.\n"
            f"{print_roll_call(roll_call)}"
        )


def set_out(update: tg.Update, context: ext.CallbackContext):
    chat_id = update.effective_chat.id
    to_remove = update.message.from_user.first_name
    roll_call = ast.literal_eval(db.load("roll_call.txt"))
    if 'in' in roll_call:
        if to_remove in roll_call['in']:
            roll_call['out'].remove(to_remove)
    roll_call['out'].append(to_remove)

    if not SILENCED:
        context.bot.send_message(
            chat_id,
            f"{to_remove} has been removed from the list.\n"
            f"{print_roll_call(roll_call)}"
        )


def set_out_for(update: tg.Update, context: ext.CallbackContext):
    chat_id = update.effective_chat.id
    if len(context.args) == 0:
        context.bot.send_message(
            chat_id,
            "Please provide a person to set out, like so:\n"
            "/set_out_for [person] [reason (optional)]"
        )
    to_remove = update.message.from_user.first_name
    roll_call = ast.literal_eval(db.load("roll_call.txt"))
    if 'in' in roll_call:
        if to_remove in roll_call['in']:
            roll_call['out'].remove(to_remove)
    roll_call['out'].append(to_remove)

    if not SILENCED:
        context.bot.send_message(
            chat_id,
            f"{to_remove} has been removed from the list.\n"
            f"{print_roll_call(roll_call)}"
        )


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


def add_rollcall_commands(dp: ext.updater.Dispatcher):
    dp.add_handler(
        ext.CommandHandler('start_roll_call', start_roll_call, pass_args=True))
    dp.add_handler(ext.CommandHandler('set_title', set_title, pass_args=True))
    dp.add_handler(ext.CommandHandler('in', set_in))
    dp.add_handler(ext.CommandHandler('out', set_out))
    dp.add_handler(
        ext.CommandHandler('set_out_for', set_out_for, pass_args=True))
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
