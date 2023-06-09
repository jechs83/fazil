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
#URL_PATTERN = r'((https?://[^\s]+)|^)(www\.[^\s]+)'
URL_PATTERN = r'(https?://[^\s]+)'




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
    urls = []
    if update.message.text:
        text = update.message.text
        urls.extend(re.findall(URL_PATTERN, text))

    if update.message.caption:
        caption = update.message.caption
        urls.extend(re.findall(URL_PATTERN, caption))

    if update.message.photo:
        for photo in update.message.photo:
            if photo.caption:
                urls.extend(re.findall(URL_PATTERN, photo.caption))

    if update.message.document:
        document = update.message.document
        if document.file_name.endswith(('.txt', '.doc', '.docx', '.pdf')):
            file_id = document.file_id
            file_url = context.bot.get_file(file_id).file_path
            urls.append(file_url)

    if update.message.video:
        video = update.message.video
        if video.caption:
            urls.extend(re.findall(URL_PATTERN, video.caption))

    if update.message.audio:
        audio = update.message.audio
        if audio.title:
            urls.extend(re.findall(URL_PATTERN, audio.title))
        if audio.performer:
            urls.extend(re.findall(URL_PATTERN, audio.performer))

    if update.message.voice:
        voice = update.message.voice
        if voice.caption:
            urls.extend(re.findall(URL_PATTERN, voice.caption))

    if update.message.sticker:
        sticker = update.message.sticker
        if sticker.emoji:
            urls.extend(re.findall(URL_PATTERN, sticker.emoji))

    if update.message.animation:
        animation = update.message.animation
        if animation.caption:
            urls.extend(re.findall(URL_PATTERN, animation.caption))

    if update.message.video_note:
        video_note = update.message.video_note
        if video_note.caption:
            urls.extend(re.findall(URL_PATTERN, video_note.caption))

    if update.message.contact:
        contact = update.message.contact
        urls.extend(re.findall(URL_PATTERN, contact.phone_number))
        urls.extend(re.findall(URL_PATTERN, contact.first_name))
        urls.extend(re.findall(URL_PATTERN, contact.last_name))
      
    

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

#url_handler = MessageHandler(Filters.text & (~Filters.command), record_url)
url_handler = MessageHandler(Filters.all, record_url)








# Define the top users command handler
def top_users(update: Update, context):


    allowed_user_id = 1160667522  # Replace with the desired user ID

    # Check if the command is executed by the allowed user
    if update.message.from_user.id != allowed_user_id:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No estas autorizado.")
        return
    
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
    message = "aqui esta tu top 10 usuarios que mas buscan:\n"
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