from commands.shames import *
from commands.misc_commands import *
from commands.kitchen import *


def main():
    updater = ext.Updater(conf.NATOHUISBOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # misc_commands
    add_misc_commands(dp)

    # kitchen
    add_kitchen_commands(dp)

    # shames
    add_shames_commands(dp)

    # running the bot
    updater.start_polling()  # starts the bot
    updater.idle()


if __name__ == '__main__':
    main()
