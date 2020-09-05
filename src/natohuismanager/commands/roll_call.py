import json
import logging
import datetime

import telegram as tg
from telegram import ext

from natohuismanager.database import Database
from config import Config


class RollCall:
    def __init__(self, dp: ext.updater.Dispatcher, config: Config, db: Database):
        dp.add_handler(ext.CommandHandler('ssh', self.ssh))
        dp.add_handler(ext.CommandHandler('loud', self.loud))
        dp.add_handler(ext.CommandHandler('start_roll_call', self.start_roll_call, pass_args=True))
        dp.add_handler(ext.CommandHandler('end_roll_call', self.end_roll_call))
        dp.add_handler(ext.CommandHandler('set_title', self.set_title, pass_args=True))
        dp.add_handler(ext.CommandHandler('in', self.set_in))
        dp.add_handler(ext.CommandHandler('out', self.set_out))
        dp.add_handler(ext.CommandHandler('set_in_for', self.set_in_for, pass_args=True))
        dp.add_handler(ext.CommandHandler('set_out_for', self.set_out_for, pass_args=True))
        dp.add_handler(ext.CommandHandler('absent', self.set_absent, pass_args=True))
        dp.add_handler(ext.CommandHandler('set_absent_for', self.set_absent_for, pass_args=True))
        dp.add_handler(ext.CommandHandler('im_back', self.im_back, pass_args=True))
        dp.add_handler(ext.CommandHandler('you_back', self.you_back, pass_args=True))

        self.logger = logging.getLogger(__name__)
        self.config = config
        self.db = db
        
        self.silenced = False
        self.running = False
        self.title = ""
        self.people_in = {}
        self.people_out = {}
        self.people_absent = {}

        self.load()

    def set_empty(self):
        self.running = False
        self.title = ""
        self.people_in = {}
        self.people_out = {}

    def load(self):
        try:
            data = json.loads(self.db.load('rollcall.txt'))
            self.title = data['title']
            self.running = data['running']
            self.silenced = data['silenced']
            self.people_in = data['people_in']
            self.people_out = data['people_out']
            self.people_absent = data['people_absent']
        except:
            self.logger.info("No rollcall data found, using default.")

    def save(self):
        data = json.dumps({
            'silenced': self.silenced, 
            'running': self.running,
            'title': self.title,
            'people_in': self.people_in,
            'people_out': self.people_out,
            'people_absent': self.people_absent
        })
        self.db.save('rollcall.txt', data)


    def loud(self, update: tg.Update, context: ext.CallbackContext):
        self.silenced = True
        self.save()

        context.bot.send_message(
            update.effective_chat.id,
            "HUZZAH I'M FREE 🗣"
        )

    def ssh(self, update: tg.Update, context: ext.CallbackContext):
        self.silenced = False
        self.save()

        context.bot.send_message(
            update.effective_chat.id,
            "Fine, I'll be quiet 🤐"
        )

    def format_roll_call(self):
        roll_call_str = self.title

        for in_out, persons in {"In": self.people_in, "Out": self.people_out, "Absent": self.people_absent}.items():
            if persons:
                roll_call_str += f"{in_out.capitalize()}:\n"

                for person, reason in persons.items():
                    roll_call_str += f" - {person} {reason}\n"
                roll_call_str += "\n"

        return roll_call_str


    def start_roll_call(self, update: tg.Update, context: ext.CallbackContext):
        if self.running:
            context.bot.send_message(
                update.effective_chat.id,
                "There is already a roll call running, ending that."
            )
            self.set_emtpy()

        self.title = ' '.join(context.args) + "\n" if context.args else ""
        self.running = True
        self.save()

        context.bot.send_message(
            update.effective_chat.id,
            "Roll call started."
        )


    def end_roll_call(self, update: tg.Update, context: ext.CallbackContext):
        if not self.running:
            context.bot.send_message(
                update.effective_chat.id,
                "There is no running roll call to end."
            )
            return

        chat_id = update.effective_chat.id
        context.bot.send_message(
            chat_id,
            "Ended roll call, I'll send the results."
        )
        context.bot.send_message(
            chat_id,
            self.format_roll_call()
        )

        self.set_empty()
        self.save()


    def set_title(self, update: tg.Update, context: ext.CallbackContext):
        if not self.running:
            context.bot.send_message(
                update.effective_chat.id,
                "There is no running roll call to set a title for."
            )
            return

        chat_id = update.effective_chat.id

        if len(context.args) == 0:
            context.bot.send_message(
                chat_id,
                "Please provide a title to set."
            )
            return

        self.title = ' '.join(context.args) + "\n"
        self.save()


    def set_in(self, update: tg.Update, context: ext.CallbackContext):
        if not self.running:
            context.bot.send_message(
                update.effective_chat.id,
                "There is no running roll call."
            )
            return

        chat_id = update.effective_chat.id
        # read in who's to enroll
        to_enroll = update.message.from_user.first_name
        reason = ' '.join(context.args)

        if to_enroll in self.people_absent:
            context.bot.send_message(
                chat_id,
                f"Hey {to_enroll} you were noted absent, but I got rid of that. Welcome back!"
            )
            del self.people_absent[to_enroll]
        
        self.people_in[to_enroll] = reason

        if to_enroll in self.people_out:
            del self.people_out[to_enroll]

        self.save()

        if not self.silenced:
            context.bot.send_message(
                chat_id,
                f"{to_enroll} is in!\n" + self.format_roll_call()
            )

    def set_in_for(self, update: tg.Update, context: ext.CallbackContext):
        if not self.running:
            context.bot.send_message(
                update.effective_chat.id,
                "There is no running roll call."
            )
            return

        chat_id = update.effective_chat.id
        # read in who's to enroll
        try:
            to_enroll = context.args[0]
        except:
            context.bot.send_message(
                chat_id,
                "Please provide a person to set out, like so:\n"
                "/set_out_for [person] [reason (optional)]"
            )
            return

        if to_enroll in self.people_absent:
            context.bot.send_message(
                chat_id,
                f"{to_enroll} is noted absent. Set them to be back with '/you_back {to_enroll}' first if you are sure they will be there."
            )
            return

        reason = ' '.join(context.args[1:])
        
        self.people_in[to_enroll] = reason

        if to_enroll in self.people_out:
            del self.people_out[to_enroll]

        self.save()

        if not self.silenced:
            context.bot.send_message(
                chat_id,
                f"{to_enroll} is in!\n" + self.format_roll_call()
            )


    def set_out(self, update: tg.Update, context: ext.CallbackContext):
        if not self.running:
            context.bot.send_message(
                update.effective_chat.id,
                "There is no running roll call."
            )
            return

        chat_id = update.effective_chat.id
        # read in who's to deroll
        to_deroll = update.message.from_user.first_name

        if to_deroll in self.people_absent:
            context.bot.send_message(
                chat_id,
                f"I already knew that, {to_enroll} is noted absent."
            )
            return

        reason = ' '.join(context.args)
        
        self.people_out[to_deroll] = reason

        if to_deroll in self.people_in:
            del self.people_in[to_deroll]

        self.save()

        if not self.silenced:
            context.bot.send_message(
                chat_id,
                f"{to_deroll} is out!\n" + self.format_roll_call()
            )


    def set_out_for(self, update: tg.Update, context: ext.CallbackContext):
        if not self.running:
            context.bot.send_message(
                update.effective_chat.id,
                "There is no running roll call."
            )
            return

        chat_id = update.effective_chat.id
        # read in who's to deroll
        try:
            to_deroll = context.args[0]
        except:
            context.bot.send_message(
                chat_id,
                "Please provide a person to set out, like so:\n"
                "/set_out_for [person] [reason (optional)]"
            )
            return

        if to_deroll in self.people_absent:
            context.bot.send_message(
                chat_id,
                f"I already knew that, {to_enroll} is noted absent."
            )
            return

        reason = ' '.join(context.args[1:])
        
        self.people_out[to_deroll] = reason

        if to_deroll in self.people_in:
            del self.people_in[to_deroll]

        self.save()

        if not self.silenced:
            context.bot.send_message(
                chat_id,
                f"{to_deroll} is out!\n" + self.format_roll_call()
            )


    def set_absent(self, update: tg.Update, context: ext.CallbackContext):
        """Note that you are absent"""
        chat_id = update.effective_chat.id
        # read in who's to deroll
        to_absent = update.message.from_user.first_name
        reason = ' '.join(context.args)
        
        self.people_absent[to_absent] = reason

        if self.running and to_absent in self.people_in:
            del self.people_in[to_absent]

        if self.running and to_absent in self.people_out:
            del self.people_out[to_absent]

        self.save()

        if not self.silenced:
            context.bot.send_message(
                chat_id,
                f"{to_absent} is absent!\n" + self.format_roll_call()
            )

    def set_absent_for(self, update: tg.Update, context: ext.CallbackContext):
        """Note that someone is absent"""
        chat_id = update.effective_chat.id

        try:
            to_absent = context.args[0]
        except:
            context.bot.send_message(
                chat_id,
                "Please provide a person to set absent, like so:\n"
                "/set_absent_for [person] [reason (optional)]"
            )
            return

        reason = ' '.join(context.args[1:])
        
        self.people_absent[to_absent] = reason

        if self.running and to_absent in self.people_in:
            del self.people_in[to_absent]

        if self.running and to_absent in self.people_out:
            del self.people_out[to_absent]

        self.save()

        if not self.silenced:
            context.bot.send_message(
                chat_id,
                f"{to_absent} is absent!\n" + self.format_roll_call()
            )

    def im_back(self, update: tg.Update, context: ext.CallbackContext):
        """Note that you are back"""
        chat_id = update.effective_chat.id
        to_unabsent = update.message.from_user.first_name
        
        if not to_unabsent in self.people_absent:
            context.bot.send_message(
                chat_id,
                "Lol you were not gone mate!"
            )
            return
            
        del self.people_absent[to_unabsent]

        self.save()

        if not self.silenced:
            context.bot.send_message(
                chat_id,
                f"{to_absent} is back!\n" + self.format_roll_call()
            )

    def you_back(self, update: tg.Update, context: ext.CallbackContext):
        """Note that someone is back"""
        chat_id = update.effective_chat.id
        try:
            to_unabsent = context.args[0]
        except:
            context.bot.send_message(
                chat_id,
                "Please provide a person to welcome back, like so:\n"
                "/you_back [person]"
            )
            return
        
        if not to_unabsent in self.people_absent:
            context.bot.send_message(
                chat_id,
                f"Lol {to_unabsent} is not gone mate!"
            )
            return
            
        del self.people_absent[to_unabsent]

        self.save()

        if not self.silenced:
            context.bot.send_message(
                chat_id,
                f"{to_absent} is back!\n" + self.format_roll_call()
            )


