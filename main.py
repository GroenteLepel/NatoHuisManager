import telegram.ext as ext
import telegram as tg

import numpy as np

import config as conf
from shames import *
from tutorial_commands import *
from kitchen import *

import time

import collections


def main():
    updater = ext.Updater(conf.NATOHUISBOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # tutorial_commands
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

    # kitchen
    dp.add_handler(ext.CommandHandler('wie_is_de_lul', pick))

    # shames
    dp.add_handler(ext.CommandHandler('shame', shame, pass_args=True))
    dp.add_handler(ext.CommandHandler('set_shame_counter', set_shame_counter, pass_args=True))
    dp.add_handler(ext.CommandHandler('get_shame_list', get_shame_list))
    dp.add_handler(ext.CommandHandler('redeem', redeem))

    # running the bot
    updater.start_polling()  # starts the bot
    updater.idle()


if __name__ == '__main__':
    main()
