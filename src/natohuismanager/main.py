from .commands import Kitchen, MiscCommands, Shames, RollCall, DiceRoll
from telegram import ext

def main(config, db):
    updater = ext.Updater(config['NATOHUISBOT_TOKEN'], use_context=True)
    dp = updater.dispatcher

    Kitchen(dp, config, db)
    MiscCommands(dp, config)
    RollCall(dp, config, db)
    Shames(dp, config, db)
    DiceRoll(dp, config, db)

    # running the bot
    updater.start_polling()  # starts the bot
    updater.idle()

