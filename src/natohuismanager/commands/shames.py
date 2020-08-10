import json
import logging

import telegram as tg
from telegram import ext

from natohuismanager.database import Database
from config import Config


class Shames:
    def __init__(self, dp: ext.updater.Dispatcher, config: Config, db: Database):
        dp.add_handler(ext.CommandHandler('shame', self.shame, pass_args=True))
        dp.add_handler(ext.CommandHandler('redeem', self.redeem, pass_args=True))
        dp.add_handler(ext.CommandHandler('set_shame_counter', self.set_shame_counter, pass_args=True))
        dp.add_handler(ext.CommandHandler('get_shame_list', self.get_shame_list))

        self.logger = logging.getLogger(__name__)
        self.config = config
        self.db = db
        self.shames = {}
        self.load_shames()

    def load_shames(self):
        shame_data = self.db.load("shames.txt")
        try:
            self.shames = json.loads(shame_data)
        except json.JSONDecodeError:
            self.logger.info("No valid shame data obtained from database. Using all zeroes.")
            self.shames = {name: 0 for name in self.config["INHABITANTS"]}
    
    def save_shames(self):
        self.db.save('shames.txt', json.dumps(self.shames))

    def shame(self, update: tg.Update, context: ext.CallbackContext):
        """Increases provided user's shame counter by 1."""
        chat_id = update.effective_chat.id

        if len(context.args) == 0:
            context.bot.send_message(
                chat_id=chat_id,
                text="Please provide a person to shame."
            )
        elif context.args[0] in self.shames:
            self.shames[context.args[0]] += 1
            self.save_shames()
            shame_gif = "https://media.giphy.com/media/W81qSImkIxkNq/giphy.gif"

            context.bot.send_animation(
                chat_id=chat_id,
                animation=shame_gif,
                caption="Shame on you, {0:s}! Your"
                        " shame count is now {1:d}.".format(
                            context.args[0],
                            self.shames[context.args[0]]
                )
            )
        else:
            context.bot.send_message(
                chat_id=chat_id,
                text="User \"{0:s}\" not found in my shames-tab.".format(
                    context.args[0]
                )
            )


    def parse_name_and_amount(self, update: tg.Update, context: ext.CallbackContext):
        name = update.message.from_user.first_name 
        amount = 1
        used_args = [False] * len(context.args)
        
        if len(context.args) != 0 and context.args[0] in self.shames:
            name = context.args[0]
            used_args[0] = True

        try:
            amount = int(context.args[len(context.args) - 1])
            used_args[len(context.args) - 1] = True
        except:
            pass

        if not all(used_args):
            raise Exception('Message not formatted correctly')

        return name, amount



    def redeem(self, update: tg.Update, context: ext.CallbackContext):
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

        try:
            redeemed_soul, redeemed_count = self.parse_name_and_amount(update, context)
        except:
            context.bot.send_message(
                chat_id=chat_id,
                text="Please format your redeem correctly."
            )
            return

        self.shames[redeemed_soul] -= redeemed_count
        if self.shames[redeemed_soul] < 0:
            self.shames[redeemed_soul] = 0
        self.save_shames()

        context.bot.send_message(
            chat_id=chat_id,
            text="{0:d} shame(s) redeemed. Good job! Current shame count "
                "for {1:s} is now {2:d}.".format(
                    redeemed_count,
                    redeemed_soul,
                    self.shames[redeemed_soul]
            )
        )

    def set_shame_counter(self, update: tg.Update, context: ext.CallbackContext):
        """Sets shame counter

        /set_shame_counter [person_to_set] [shame_value]
        """
        chat_id = update.effective_chat.id

        # check if the person trying this command is the one and only
        if not update.message.from_user.username == self.config["ADMIN_USER"]:
            context.bot.send_message(
                chat_id=chat_id,
                text="You are not allowed to do that. Shame on you!"
            )
            return

        # check if the right syntax is used
        try:
            previous_count = self.shames[context.args[0]]
            self.shames[context.args[0]] = int(context.args[1])
            self.save_shames()
        except:
            context.bot.send_message(
                chat_id=chat_id,
                text="Please provide the right info, like this:\n"
                    "/set_shame_counter <person> <new_shame_value>"
            )

        context.bot.send_message(
            chat_id=chat_id,
            text="User {0:s}'s shame count set to {1:d}".format(
                context.args[0],
                int(context.args[1])
            )
        )
        
    def get_shame_list(self, update: tg.Update, context: ext.CallbackContext):
        """Sends the shame list in decreasing order as message."""
        chat_id = update.effective_chat.id
        shames_sorted = \
            sorted(self.shames.items(), key=lambda item: item[1], reverse=True)

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
