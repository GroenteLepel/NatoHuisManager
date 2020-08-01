import telegram as tg
from telegram import ext
import numpy as np

import time


def pick(update: tg.Update, context: ext.CallbackContext):
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text="Is even kijken wie er dit keer gaat koken..."
    )
    time.sleep(2 * np.random.rand())
    de_lul = np.random.choice(['Margot', 'Tom', 'Thijs', 'Daniël'])
    rand = np.random.rand()
    while rand < 0.5:
        think_msg = np.random.choice([
            "Even denken...",
            "Dit is een moeilijke...",
            "Zal ik gewoon weer Tom kiezen? Misschien wel... Misschien niet...",
            "Jaaaa ik heb 'm bijna..."
        ])
        context.bot.send_message(chat_id, think_msg)
        time.sleep(2 * np.random.rand())
        rand = np.random.rand()
    context.bot.send_message(chat_id, de_lul)