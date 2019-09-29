import logging

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters)

from newsfeed import get_newsfeed, get_searchfeed, summarise


def main():
    """Start the bot."""

    # enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # create the Updater and pass it your bot's token.
    # make sure to set use_context=True to use the new context based callbacks.
    TOKEN = 'token'  # your telegram bot token

    updater = Updater(token=TOKEN, use_context=True)

    # get dispatcher to register handlers
    dp = updater.dispatcher

    # initiate the following handlers
    # command handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('search', news_search))
    dp.add_handler(CommandHandler('help', help_menu))

    # message handlers
    dp.add_handler(MessageHandler(Filters.command, fallback))
    dp.add_handler(MessageHandler(Filters.text, echo))

    # callback query handlers
    dp.add_handler(CallbackQueryHandler(news_bulletin, pattern='^\d$'))
    dp.add_handler(CallbackQueryHandler(news_bulletin, pattern='^main$'))

    # start the bot
    updater.start_polling()
    print('Bot is live.')
    updater.idle()


def start(update, context):
    """Usage: /start. Sends user their news bulletin."""

    # fetch news urls and news titles for news bulletin
    context.bot.send_message(chat_id=update.message.chat.id,
                             text='Fetching your news...')
    newsfeed = get_newsfeed()

    # store urls and titles for user
    user_data = context.user_data
    ids = [1, 2, 3, 4, 5]
    for i, news in zip(ids, newsfeed):
        user_data[i] = news

    # send news bulletin
    user_data = context.user_data
    titles = [title for (key, (num, url, title)) in user_data.items()]
    message = "*Here are today's top 5 stories 🤙 *\n"
    message += f"\n1️⃣ {titles[0]}\n\n2️⃣ {titles[1]}\n\n3️⃣ {titles[2]}\n\n4️⃣ {titles[3]}\n\n5️⃣ {titles[4]}"

    keyboard = [[InlineKeyboardButton('Read 1', callback_data='1'),
                 InlineKeyboardButton('Read 2', callback_data='2')],
                [InlineKeyboardButton('Read 3', callback_data='3'),
                 InlineKeyboardButton('Read 4', callback_data='4')],
                [InlineKeyboardButton('Read 5', callback_data='5'),
                 InlineKeyboardButton('About', url='https://github.com/ahthon/jolt-telegram-news-bot')]]

    context.bot.send_message(chat_id=update.message.chat.id,
                             text=message,
                             reply_markup=InlineKeyboardMarkup(keyboard),
                             parse_mode=ParseMode.MARKDOWN)


def news_bulletin(update, context):
    """Display news bulletin menu."""

    user_data = context.user_data
    query = update.callback_query
    callback = query.data

    if callback == 'main':  # user clicks 'back' button, go to main menu

        # construct main menu message
        titles = [title for (key, (num, url, title)) in user_data.items()]
        message = "*Here are today's top 5 stories 🤙 *\n"
        message += f"\n1️⃣ {titles[0]}\n\n2️⃣ {titles[1]}\n\n3️⃣ {titles[2]}\n\n4️⃣ {titles[3]}\n\n5️⃣ {titles[4]}"

        # main menu inline buttons
        keyboard = [[InlineKeyboardButton('Read 1', callback_data='1'),
                     InlineKeyboardButton('Read 2', callback_data='2')],
                    [InlineKeyboardButton('Read 3', callback_data='3'),
                     InlineKeyboardButton('Read 4', callback_data='4')],
                    [InlineKeyboardButton('Read 5', callback_data='5'),
                     InlineKeyboardButton('About', url='http://google.com')]]

        # send main menu
        query.edit_message_text(text=message,
                                reply_markup=InlineKeyboardMarkup(keyboard),
                                parse_mode=ParseMode.MARKDOWN)

    else:  # user clicks 'read' button, go to sub menu
        callback_num = int(query.data)

        # get specific story
        story = user_data[callback_num]
        (num, url, title) = story

        # construct message for specific story
        summary = summarise(url)
        message = '*{}*\n\n'.format(title.upper())
        message += summary
        message += '\n\nRead full story [here]({})'.format(url)

        # inline buttons for specific stories
        if callback_num == 1:  # first story
            keyboard_first = [[InlineKeyboardButton('—', callback_data='nil'),
                               InlineKeyboardButton('Next', callback_data='2')],
                              [InlineKeyboardButton('Return to stories', callback_data='main')]]
            query.edit_message_text(text=message,
                                    reply_markup=InlineKeyboardMarkup(keyboard_first),
                                    parse_mode=ParseMode.MARKDOWN,
                                    disable_web_page_preview=True)

        elif callback_num == 5:  # last (fifth) story
            keyboard_last = [[InlineKeyboardButton('Prev', callback_data='4'),
                              InlineKeyboardButton('—', callback_data='nil')],
                             [InlineKeyboardButton('Return to stories', callback_data='main')]]
            query.edit_message_text(text=message,
                                    reply_markup=InlineKeyboardMarkup(keyboard_last),
                                    parse_mode=ParseMode.MARKDOWN,
                                    disable_web_page_preview=True)

        else:  # second to fourth stories
            prev_story = callback_num - 1
            next_story = callback_num + 1
            keyboard_mid = [[InlineKeyboardButton('Prev', callback_data='{}'.format(prev_story)),
                             InlineKeyboardButton('Next', callback_data='{}'.format(next_story))],
                            [InlineKeyboardButton('Return to stories', callback_data='main')]]
            query.edit_message_text(text=message,
                                    reply_markup=InlineKeyboardMarkup(keyboard_mid),
                                    parse_mode=ParseMode.MARKDOWN,
                                    disable_web_page_preview=True)


def news_search(update, context):
    """Usage: /search."""

    user_input = update.message.text

    # prompt user to enter search query
    if user_input == '/search':
        update.message.reply_text(text='Please send me a search query using `/search <your search query>`',
                                  parse_mode=ParseMode.MARKDOWN)

    # elif user has already entered search query
    elif user_input.startswith('/search '):
        search_query = list(user_input.partition(' '))[2].strip()
        update.message.reply_text(text='Searching...')

        # conduct search, fetch results
        search = get_searchfeed(query=search_query)

        if search is not None:  # search was successful
            message = '*Results for "{}":*\n\n'.format(search_query)
            for result in search:
                (num, url, title) = result
                message += '{}. {} [Read]({})\n\n'.format(num, title, url)

            context.bot.send_message(chat_id=update.message.chat.id,
                                     text=message,
                                     parse_mode=ParseMode.MARKDOWN,
                                     disable_web_page_preview=True)

        else:  # search failed
            message = '0 results found for "{}".'.format(search_query)
            context.bot.send_message(chat_id=update.message.chat.id, text=message)


def help_menu(update, context):
    """Usage: /help."""

    # help menu message
    message = "I've got you. Here's what I can do:\n"
    message += "`/start`: send news bulletin\n"
    message += "`/search`: search for news"

    context.bot.send_message(chat_id=update.message.chat.id, text=message, parse_mode=ParseMode.MARKDOWN,)


def echo(update, context):
    """Bot echoes user input. 😛"""

    context.bot.send_message(chat_id=update.message.chat.id,
                             text=update.message.text+' 😛')


def fallback(update, context):
    """Fallback for input error. Usage: /unknown command."""

    context.bot.send_message(chat_id=update.message.chat.id, text="Sorry, I didn't quite understand what you said.")

    # prompt user to do something else
    keyboard = [[InlineKeyboardButton('/start'), InlineKeyboardButton('/search')]]
    message = "What can I do for you?\n`/start`: send news bulletin\n`/search`: search for news"
    context.bot.send_message(chat_id=update.message.chat.id, text=message, parse_mode=ParseMode.MARKDOWN,
                             reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))


if __name__ == '__main__':
    main()
