from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

BOT_TOKEN = '7888482179:AAHXGpLC-YUfMLRcC3ZK8eGnA0Wwx-SPsfI'  # Replace with your bot token
CHANNEL_USERNAME = '@Toshkentinvestuz'  # Replace with your channel username (without @)

def start(update: Update, context):
    user = update.effective_user
    chat_member = context.bot.get_chat_member(CHANNEL_USERNAME, user.id)

    # Check subscription status
    if chat_member.status in ['member', 'administrator', 'creator']:
        # Message for subscribed users
        update.message.reply_text(
            "Shu kanalda barcha videolar mavjud. Kanalga kirishingiz mumkin!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Kanalga o'tish", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]
            ])
        )
    else:
        # Message for non-subscribed users
        update.message.reply_text(
            "Ushbu kanalga obuna bo‘ling, shundan so‘ng kirish imkoniyatiga ega bo‘lasiz.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Kanalga obuna bo‘ling", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
                [InlineKeyboardButton("Kanalga o'tish", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]
            ])
        )

def main():
    # Create the Updater and pass it your bot's token
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add the handler for the /start command
    dispatcher.add_handler(CommandHandler('start', start))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
