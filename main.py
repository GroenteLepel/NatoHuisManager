from commands.shames import *
from commands.misc_commands import *
from commands.kitchen import *


def main():
    updater = ext.Updater(conf.NATOHUISBOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    xd_filter = ["XD", "Xd", "xd", "xD", "XXD", "XXXD", "XDD", "xxD"]

    # misc_commands
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
    dp.add_handler(ext.CommandHandler('set_out_till', set_out_till, pass_args=True))
    # dp.add_handler(
    #     ext.MessageHandler(
    #         ext.Filters.text(
    #             ['/start_roll_call', '/start_roll_call@WhosInBot']
    #         ),
    #         set_out_for_absents
    #     )
    # )
    dp.add_handler(ext.CommandHandler('im_back', im_back))

    # kitchen
    dp.add_handler(ext.CommandHandler('wie_is_de_lul', pick))
    dp.add_handler(ext.CommandHandler('open_fridge', open_fridge))
    dp.add_handler(ext.CommandHandler('add_restje', add_restje, pass_args=True))
    dp.add_handler(ext.CommandHandler('remove_restje', remove_restje, pass_args=True))
    dp.add_handler(ext.CommandHandler('dibs', dibs, pass_args=True))

    # shames
    dp.add_handler(ext.CommandHandler('init_shames', init_shames))
    dp.add_handler(ext.CommandHandler('shame', shame, pass_args=True))
    dp.add_handler(ext.CommandHandler('redeem', redeem, pass_args=True))
    dp.add_handler(ext.CommandHandler('set_shame_counter', set_shame_counter, pass_args=True))
    dp.add_handler(ext.CommandHandler('get_shame_list', get_shame_list))

    # running the bot
    updater.start_polling()  # starts the bot
    updater.idle()


if __name__ == '__main__':
    main()
