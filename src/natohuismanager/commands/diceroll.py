import json
import logging
import traceback

import telegram as tg
from telegram import ext

from natohuismanager.database import Database
from config import Config

from dice import VarEnvProvider, calc, bake_distribution


class DiceRoll:
    def __init__(self, dp: ext.updater.Dispatcher, config: Config, db: Database):
        dp.add_handler(ext.CommandHandler('roll', self.roll, pass_args=True))
        dp.add_handler(ext.CommandHandler('distribution', self.distribution, pass_args=True))
        
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.db = db
        self.provider = VarEnvProvider(db)

    def roll(self, update: tg.Update, context: ext.CallbackContext):
        """Parse and roll somedice like this! 3d8+12"""
        chat_id = update.effective_chat.id
        user = update.message.from_user.first_name

        if not context.args:
            context.bot.send_message(
                chat_id=chat_id,
                text="Roll something like this: /roll d20+2"
            )
            return

        roll = ' '.join(context.args)

        try:
            result = calc(roll, self.provider.get(user))
            context.bot.send_message(
                chat_id=chat_id,
                text=result
            )
        except:
            context.bot.send_message(
                chat_id=chat_id,
                text="Your roll was invalid :("
            )
        return

    def distribution(self, update: tg.Update, context: ext.CallbackContext):
        """Calculate and plot the distribution of a dice roll"""
        chat_id = update.effective_chat.id
        user = update.message.from_user.first_name

        if not context.args:
            context.bot.send_message(
                chat_id=chat_id,
                text="Distribute something like this: /distribute d20+2"
            )
            return

        roll = ' '.join(context.args)

        try:
            with bake_distribution(roll, self.provider.get(user)) as f:
                context.bot.send_photo(
                    chat_id=chat_id,
                    photo=open(f, 'rb')
                )
        except:
            self.logger.error(traceback.format_exc())
            context.bot.send_message(
                chat_id=chat_id,
                text="Your roll was invalid :("
            )
        return