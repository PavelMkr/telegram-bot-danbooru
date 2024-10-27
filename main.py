import requests
import random
import datetime
import csv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import os

# Storage for chat_id and active chat list
active_chats = {}

# constants
TAGS = ''  # Set the tag to search for images
MAX_SENT_IMAGES = 48  # Maximum number of images to save. You can change it

# Function to download already sent images from file for specific chat
def load_sent_images(chat_id):
    filename = f'links_{chat_id}.csv' # path to the logs of chat pictures id. I use small count of chats, you can change path to a folder
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            return [row[0] for row in reader]
    except FileNotFoundError:
        return []

# Function to save new link to the sent image for a specific chat
def save_sent_image(chat_id, image_url):
    filename = f'links_{chat_id}.csv'
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([image_url])

# Function to get random picture with Danbooru on a certain tag
def get_random_image(tags, chat_id):
    base_url = "https://danbooru.donmai.us/posts.json"
    params = {"tags": tags, 'limit': 255}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        return None, f"Error while executing query: {e}"

    posts = response.json()

    if not posts:
        return None, "No images with tags"

    # Upload already sent images for this chat
    sent_images = load_sent_images(chat_id)

    # Get images that have not yet been sent to this chat
    available_posts = [post for post in posts if post.get("file_url") not in sent_images]

    if not available_posts:
        return None, "All available images have already been sent"

    # Select random image
    random_post = random.choice(available_posts)
    image_url = random_post.get("file_url")

    if image_url:
        # Save the URL of the image sent to a file for this chat
        save_sent_image(chat_id, image_url)

    return image_url, None

# Function to send a picture
async def send_image(bot, chat_id, tags):
    image_url, error = get_random_image(tags, chat_id)

    if error:
        await bot.send_message(chat_id=chat_id, text=error)
    else:
        await bot.send_photo(chat_id=chat_id, photo=image_url)

# Command handler /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id

    # Save chat_id to storage with its tags
    active_chats[chat_id] = TAGS

    # Remove old tasks for this chat only
    for job in scheduler.get_jobs():
        if job.kwargs.get('chat_id') == chat_id:
            scheduler.remove_job(job.id)

    # Image sent immediately
    scheduler.add_job(
        send_image,
        DateTrigger(run_date=datetime.datetime.now()),
        kwargs={'bot': context.bot, 'chat_id': chat_id, 'tags': TAGS}
    )

    # Re-shipping every interval
    scheduler.add_job(
        send_image,
        IntervalTrigger(hours=3), # You can set on your time interval. Now its 3 hours
        kwargs={'bot': context.bot, 'chat_id': chat_id, 'tags': TAGS}
    )

    await update.message.reply_text('Hi! I will send you pictures from Danbooru every 3 hours.')

# Command handler /stop
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id

    if chat_id in active_chats:
        del active_chats[chat_id]

        # Remove only tasks from this chat
        for job in scheduler.get_jobs():
            if job.kwargs.get('chat_id') == chat_id:
                scheduler.remove_job(job.id)

        await update.message.reply_text('You will no longer receive images')
    else:
        await update.message.reply_text('You have not signed up for the images')

# The /newimage command handler to get a new image immediately
async def newimage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id

    scheduler.add_job(
        send_image,
        DateTrigger(run_date=datetime.datetime.now()),
        kwargs={'bot': context.bot, 'chat_id': chat_id, 'tags': TAGS}
    )

# Basic function to run the bot
async def main():
    # Enter your token here
    token = 'YOUR_TG_TOKEN"

    global scheduler
    scheduler = AsyncIOScheduler()
    scheduler.start()

    application = ApplicationBuilder().token(token).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("newimage", newimage))

    # Launch bot
    await application.run_polling()

if __name__ == '__main__':
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())