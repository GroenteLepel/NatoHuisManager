import telegram.ext as ext
import telegram as tg

import numpy as np

import config as conf
from shames import *
from misc_commands import *
from kitchen import *

import time

import collections


def main():
    updater = ext.Updater(conf.NATOHUISBOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # misc_commands
    dp.add_handler(ext.CommandHandler('bop', bop))
    dp.add_handler(ext.CommandHandler('start', start))
    dp.add_handler(ext.CommandHandler('git', git))
    # dp.add_handler(
    #     ext.MessageHandler(
    #         ext.Filters.text & (~ext.Filters.command),  # filters all commands
    #         echo
    #     )
    # )
    dp.add_handler(ext.CommandHandler('caps', caps))
    dp.add_handler(ext.InlineQueryHandler(inline_caps))

    # kitchen
    dp.add_handler(ext.CommandHandler('wie_is_de_lul', pick))
    dp.add_handler(ext.CommandHandler('add_restje', add_restje, pass_args=True))
    dp.add_handler(ext.CommandHandler('remove_restje', remove_restje, pass_args=True))
    dp.add_handler(ext.CommandHandler('dibs', dibs, pass_args=True))

    # shames
    dp.add_handler(ext.CommandHandler('shame', shame, pass_args=True))
    dp.add_handler(ext.CommandHandler('redeem', redeem, pass_args=True))
    dp.add_handler(ext.CommandHandler('set_shame_counter', set_shame_counter, pass_args=True))
    dp.add_handler(ext.CommandHandler('get_shame_list', get_shame_list))

    # running the bot
    updater.start_polling()  # starts the bot
    updater.idle()


if __name__ == '__main__':
    main()
