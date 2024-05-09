from telegram.ext import Application, MessageHandler, filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import uuid
from group import Group

groups = []

async def start(update: Update):
    # Send a message when the command /start is issued
    await update.message.reply_text('Hi! I am a Secret Santa Bot. I will help you to organize a Secret Santa event. To know more about me, type /info')

async def create_group(update: Update):
    # Send a message when the command /create_group is issued
    await update.message.reply_text('To create a group, type /create_group <group_name>')
    # Get the group name
    group_name = update.message.text.split(' ')[1]
    # Generate a unique group ID
    group_id = str(uuid.uuid4())
    # Generate a group link
    group_link = f"https://t.me/joinchat/{group_id}"
    # Create a group
    group = Group(group_name, group_id, group_link)
    # Add the group to the list of groups
    groups.append(group)
    # Send a message with the group ID and link
    await update.message.reply_text(f'Group created successfully!\nGroup ID: {group_id}\nGroup Link: {group_link}')

async def info(update: Update):
    # Send a message when the command /info is issued
    update.message.reply_text(
        'Welcome to the Secret Santa Bot!\n\n'
        'I will help you to organize a Secret Santa event. Here is how you can use me:\n\n'
        '/start - Start a new Secret Santa group\n'
        '/join <group_id> - Join an existing Secret Santa group using the provided group ID\n'
        '/freeze - Freeze the Secret Santa group to prevent new participants from joining\n'
        '/assign - Assign gift recipients for each participant\n\n'
        'Once the group is frozen and recipients are assigned, participants can mark when they have prepared their gifts.'
    )



def main():
    # Create the bot with token
    bot_token = '7070275115:6459322939:AAGdDl0kK0RwWtQhun4HMqe2TNCajb8ASAQ'
    app = Application.builder().token(bot_token).build()

    #Configure the command handler
    # start command
    app.add_handler(CommandHandler('start', start))
    # create group command
    app.add_handler(CommandHandler('create_group', create_group))
    # info command
    app.add_handler(CommandHandler('info', info))






if __name__ == '__main__':
    main()

    

