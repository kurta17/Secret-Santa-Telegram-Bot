from telegram.ext import Application, MessageHandler, filters, CommandHandler, CallbackContext
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import uuid


# Dictionary to store group data
groups = {}
async def pr():
    print(groups)



async def start(update: Update, context: CallbackContext):
    # Send a message when the command /start is issued
    await update.message.reply_text('Hi! I am a Secret Santa Bot. I will help you to organize a Secret Santa event. To know more about me, type /info')

async def info(update: Update, context: CallbackContext):
    # Send a message when the command /info is issued
    await update.message.reply_text(
        'Welcome to the Secret Santa Bot!\n\n'
        'I will help you to organize a Secret Santa event. Here is how you can use me:\n\n'
        '/start - Start a new Secret Santa group\n'
        '/create_group <admin> - Create a new Secret Santa group\n'
        '/join_group <group_id> - Join an existing Secret Santa group using the provided group ID\n'
    )

async def create_group(update: Update, context: CallbackContext):
    # Create a new Secret Santa group with a unique ID and save it in the groups dictionary
    group_id = str(uuid.uuid4())
    admin_id = update.effective_user.id
    groups[group_id] = {"admin": admin_id, "members": [admin_id]}
    await update.message.reply_text(f"Secret Santa group created!\n Group ID: {group_id}")

async def join_group(update: Update, context: CallbackContext):
    # Join an existing Secret Santa group using the provided group ID
    group_id = context.args[0]
    user_id = update.effective_user.id
    if group_id in groups:
        if user_id not in groups[group_id]["members"]:
            groups[group_id]["members"].append(user_id)
            await update.message.reply_text("You have joined the Secret Santa group!")
        else:
            await update.message.reply_text("You are already a member of this group.")
    else:
        await update.message.reply_text("This group does not exist.")

def main():
    bot_token = '6459322939:AAGdDl0kK0RwWtQhun4HMqe2TNCajb8ASAQ'
    app = Application.builder().token(bot_token).build()

    # Configure the command handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('info', info))
    app.add_handler(CommandHandler('create_group', create_group))
    app.add_handler(CommandHandler('join_group', join_group))
    

    # Start the bot
    app.run_polling()

if __name__ == '__main__':
    main()
    print(groups)