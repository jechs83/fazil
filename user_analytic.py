import logging
import re
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId


# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the regular expression pattern to match URLs
URL_PATTERN = r'((https?://)|^)(www\.[^\s]+)'


#URL_PATTERN = r'(https?://[^\s]+)'
MONGO_DB = "mongodb+srv://spok:xzNMTKM0HgnL4oI1@cluster0.wkqej.mongodb.net/"
#MONGO_DB = "mongodb://superuser:Viper.2013@192.168.9.66:27017/?authMechanism=DEFAULT&tls=false"

# Connect to MongoDB
client = MongoClient(MONGO_DB)
db = client['data']
collection = db['data']

# Define the start command handler
# def start(update: Update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="se Grabo ptm.")

# start_handler = CommandHandler('start', start)

# Define the message handler
def record_url(update: Update, context):
    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    text = update.message.text

    # Extract URLs using the regular expression pattern

    urls = re.findall(URL_PATTERN, text)
    

    # Save the user, URLs, name, and date/time to the database
    for url in urls:
        document = {
            '_id':ObjectId(),
            'user_id': user_id,
            'url': url,
            'first_name': first_name,
            'last_name': last_name,
            'timestamp': datetime.now()
        }
        collection.insert_one(document)
    


    # # Send a confirmation message to the user
    # context.bot.send_message(chat_id=update.effective_chat.id, text="se grabo la url ptm!")

url_handler = MessageHandler(Filters.text & (~Filters.command), record_url)

# Define the top users command handler
def top_users(update: Update, context):
    # Calculate the date from a week ago
    week_ago = datetime.now() - timedelta(days=7)

    # Retrieve all users' URLs in the last week
    pipeline = [
        {
            '$match': {
                'timestamp': {'$gte': week_ago}
            }
        },
        {
            '$group': {
                '_id': '$user_id',
                'count': {'$sum': 1},
                'first_name': {'$first': '$first_name'}
            }
        },
        {
            '$sort': {'count': -1}
        },
        {
            '$limit': 10
        }
    ]
    result = collection.aggregate(pipeline)

    # Generate the message with the top users
    message = "aqui esta tu top 10 mierda:\n"
    for idx, entry in enumerate(result, start=1):
        user_id = entry['_id']
        count = entry['count']
        first_name = entry['first_name']
        user = f"User {idx}: {first_name} (Count: {count})\n"
        message += user

    # Send the message to the user
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

top_users_handler = CommandHandler('topusers', top_users)

def main():
    # Create an Updater and pass your bot's API token
    updater = Updater(token='6131243126:AAFvqYfb541Rt-kwQt1lPeaLVIqfaencQEs', use_context=True)
    dispatcher = updater.dispatcher

    # Add the handlers
    #dispatcher.add_handler(start_handler)
    dispatcher.add_handler(url_handler)
    dispatcher.add_handler (top_users_handler)


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()