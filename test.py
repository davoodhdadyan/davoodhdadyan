from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import random
import logging

# API Token key
API_TOKEN = "7822653049:AAHU7E8R6oVUJCMLcnZaCEsY6a-jutBAfMQ"  # Please enter your API token here.

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(name)

# Create a dictionary to store users
users = {}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am the anonymous chat bot. Please send your message to start.')

def anonymous_chat(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # If the user has been in anonymous chat before, connect them to a new chat
    if user_id in users:
        peer_user_id = users[user_id]
        context.bot.send_message(peer_user_id, update.message.text)
        update.message.reply_text('Your message has been sent!')
    else:
        # Find another random user
        other_user_id = get_random_user(user_id)
        if other_user_id:
            users[user_id] = other_user_id
            users[other_user_id] = user_id
            context.bot.send_message(other_user_id, "An anonymous user has been connected to you.")
            context.bot.send_message(user_id, "You have been connected to an anonymous user.")
        else:
            update.message.reply_text('Sorry, there is no other user available for chat.')

def get_random_user(current_user_id):
    available_users = [uid for uid in users if uid != current_user_id]
    return random.choice(available_users) if available_users else None

def main() -> None:
    updater = Updater(API_TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, anonymous_chat))

    updater.start_polling()
    updater.idle()

if name == 'main':
    main()
