from commands.shames import *
from commands.misc_commands import *
from commands.kitchen import *


def main():
    updater = ext.Updater(conf.NATOHUISBOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # misc_commands
    add_misc_commands(dp)

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
