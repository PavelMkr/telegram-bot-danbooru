# Telegram Image Bot

This project is a Telegram bot that periodically sends images from Danbooru based on specified tags to users or chats. It utilizes `apscheduler` to schedule periodic messages and saves sent images for each user or chat, ensuring no duplicates are sent in a single chat.

## Features

- **Automatic Scheduled Image Sending:** Sends images from Danbooru based on tags at specified intervals (default is every 3 hours).
- **On-Demand Images:** Users can request an image immediately.
- **Start/Stop Commands:** Users can start or stop receiving periodic images.
- **Image Deduplication:** Keeps track of sent images to prevent duplicates.

## Prerequisites

- **Python 3.8+**
- **Telegram Bot Token** from [BotFather](https://core.telegram.org/bots#botfather).
- **Danbooru API Access**

### Required Python Packages

Install the dependencies with:

```bash
pip install python-telegram-bot[ext] apscheduler nest_asyncio requests
```

## Setting Up and Deploying on PythonAnywhere

1. **Clone the repository:**

   ```bash
   git clone https://github.com/PavelMkr/telegram-bot-danbooru
   cd https://github.com/PavelMkr/telegram-bot-danbooru
   ```

2. **Set up Environment Variables**

   In the root directory of your project, create an `.env` file to store the bot token:

   ```env
   TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
   ```

3. **Deploy on PythonAnywhere (or simular service)**

   - Upload your project files to PythonAnywhere.
   - Go to the **Web** tab, set up a new web app, and configure it to run your bot script.
   - Under **Tasks**, add a **scheduled task** to run the bot script using `python3 <script_name>.py`.

4. **Run the Bot**

   Start the bot by running your script on PythonAnywhere, and it will begin listening for commands.

## Usage

### Commands

- **/start**: Starts receiving images periodically based on tags.
- **/stop**: Stops receiving images.
- **/newimage**: Requests a new image immediately.

## Configuration

- **Tags**: Set the `TAGS` variable in the script to specify Danbooru tags.
- **Interval**: Adjust the interval for sending images in the `IntervalTrigger(hours=3)` in the `/start` handler.

## Contributing

Feel free to contribute by creating issues, suggesting new features, or submitting pull requests.
