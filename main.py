# -*- coding: utf-8 -*-
"""Main module"""
from telegram import BotCommand
from telegram.ext import CommandHandler, MessageHandler, Filters , Dispatcher, Updater

from module.data import setup_db
from module.commands.start import start
from module.commands.help import help_cmd
from module.commands.report import report
from module.commands.ufficio_ersu import ufficio_ersu
from module.commands.menu import menu
from module.shared import config_map
from module.data.constants import CONTACT_ERSU, REPORT, HELP, MENU_MENSA

def add_commands(up: Updater) -> None:
    """Adds the list of commands with their description to the bot

    Args:
        up (Updater): supplied Updater
    """
    commands = [
        BotCommand("start", "messaggio di benvenuto"),
        BotCommand("help ", "ricevi aiuto sui comandi"),
        BotCommand("report", "segnala un problema"),
        BotCommand("ufficioersu", "ricevi i contatti dell'Ersu"),
        BotCommand("menu", "ricevi il menù del giorno")
    ]
    up.bot.set_my_commands(commands=commands)


def add_handlers(dp: Dispatcher) -> None:
    """Adds all the handlers the bot will react to

    Args:
        dp: supplied Dispatcher
    """

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('chatid', lambda u, c: u.message.reply_text(u.message.chat_id)))
    dp.add_handler(CommandHandler('help', help_cmd))
    dp.add_handler(MessageHandler(Filters.regex(HELP), help_cmd))
    dp.add_handler(CommandHandler('report', report))
    dp.add_handler(MessageHandler(Filters.regex(REPORT), report))
    dp.add_handler(CommandHandler('ufficioersu', ufficio_ersu))
    dp.add_handler(MessageHandler(Filters.regex(CONTACT_ERSU), ufficio_ersu))
    dp.add_handler(CommandHandler('menu', menu))
    dp.add_handler(MessageHandler(Filters.regex(MENU_MENSA), menu))

def main() -> None:
    """Main function"""
    updater = Updater(config_map['token'], request_kwargs={'read_timeout': 20, 'connect_timeout': 20}, use_context=True)
    add_commands(updater)
    add_handlers(updater.dispatcher)
    setup_db()

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()