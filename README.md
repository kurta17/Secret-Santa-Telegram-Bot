# Secret Santa Telegram Bot

Welcome to the Secret Santa Telegram Bot! This bot allows you to organize Secret Santa gift exchanges directly within your Telegram groups. Whether you want to create a new Secret Santa group or join an existing one, this bot has got you covered.

## Features

- **Group Creation**: Easily create a new Secret Santa group within Telegram.
- **Participant Management**: Add participants to your group and freeze adding new participants when needed.
- **Gift Assignment**: Automatically assign each participant a gift recipient.
- **Gift Preparation Tracking**: Participants can mark when they have prepared their gifts.
- **File System Persistence**: All group data is stored locally on the file system for easy retrieval.

## Installation

To get started with the Secret Santa Telegram Bot, follow these steps:

1. Clone the repository:
git clone https://github.com/your-username/Secret-Santa-Telegram-Bot.git


2. Install dependencies:
pip install -r requirements.txt


3. Set up your Telegram Bot API token:
- Create a new bot using [BotFather](https://core.telegram.org/bots#botfather).
- Copy the bot token provided by BotFather.
- Create a `.env` file in the project root directory.
- Add the following line to the `.env` file:
  ```
  TELEGRAM_TOKEN=your-bot-token
  ```

4. Run the bot:
python bot.py


## Usage

1. Start the bot by sending the `/start` command in a Telegram chat with the bot.
2. Follow the bot's instructions to create a new Secret Santa group or join an existing one.
3. Once the group is set up and participants have joined, the group administrator can manage the group and assign gift recipients.
4. Participants can mark when they have prepared their gifts using the provided commands.
