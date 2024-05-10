from telegram.ext import Application, MessageHandler, filters, CommandHandler, CallbackContext,ConversationHandler
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import uuid


# Dictionary to store group data
groups = {}


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Hi! I am a Secret Santa Bot. I will help you to organize a Secret Santa event. To know more about me, type /info')

async def info(update: Update, context: CallbackContext):
    await update.message.reply_text(
        'Welcome to the Secret Santa Bot!\n\n'
        'I will help you to organize a Secret Santa event. Here is how you can use me:\n\n'
        '/start - Start a new Secret Santa group\n'
        '/create_group <admin> - Create a new Secret Santa group\n'
        '/join_group <group_id> - Join an existing Secret Santa group using the provided group ID\n'
    )




ADMIN_NAME = 0
GROUP_NAME = 1
ADMIN_GIFT = 2

async def create_group(update: Update, context: CallbackContext):
    group_id = str(uuid.uuid4())
    admin_id = update.effective_user.id
    context.user_data["group_id"] = group_id
    groups[group_id] = {"admin": admin_id, "members": [admin_id], "admin_name": "", "group_name": "", "gift": []}
    await update.message.reply_text("Enter the your name as a Host:")
    return ADMIN_NAME

async def admin_name(update: Update, context: CallbackContext):
    admin_name = update.message.text
    group_id = context.user_data["group_id"]
    groups[group_id]["admin_name"] = admin_name
    await update.message.reply_text("Enter the group name:")
    return GROUP_NAME

async def group_name(update: Update, context: CallbackContext):
    group_name = update.message.text
    group_id = context.user_data["group_id"]
    groups[group_id]["group_name"] = group_name
    await update.message.reply_text("Enter the gift you want to recive ?")
    return ADMIN_GIFT

async def take_gift(update: Update, context: CallbackContext):
    gift = update.message.text
    user_id = update.effective_user.id
    group_id = context.user_data["group_id"]
    groups[group_id]["gift"].append(gift)
    print(groups)
    await update.message.reply_text(f'Group created successfully! Share the group ID: { group_id } with your friends to join the group.')
    return ConversationHandler.END


    
async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

create_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('create_group', create_group)],
    states={
        ADMIN_NAME : [MessageHandler(filters.TEXT, admin_name)],
        GROUP_NAME : [MessageHandler(filters.TEXT, group_name)],
        ADMIN_GIFT : [MessageHandler(filters.TEXT, take_gift)]

    },
    fallbacks=[CommandHandler('cancel', cancel)]
)


TAKE_ID = 0
TAKE_GIFT = 1


async def join_group(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    await update.message.reply_text("Enter the group ID:")
    return TAKE_ID
    
async def take_id(update: Update, context: CallbackContext):
    group_id = update.message.text
    if group_id in groups:
        if update.effective_user.id not in groups[group_id]["members"]:
            groups[group_id]["members"].append(update.effective_user.id)
            context.user_data["group_id"] = group_id
            await update.message.reply_text(f"What gift do you want to recive?")
        else:
            await update.message.reply_text("You are already a member of this group")
    else:
        await update.message.reply_text("Invalid group ID")
        
    print(groups)
    return TAKE_GIFT

async def take_gift_user(update: Update, context: CallbackContext):
    gift = update.message.text
    user_id = update.effective_user.id
    group_id = context.user_data["group_id"]
    groups[group_id]["gift"].append(gift)
    print(groups)
    await update.message.reply_text(f'Wait until the group admin assigns the gifts to the members')
    return ConversationHandler.END



join_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('join_group', join_group)],
    states={
        TAKE_ID : [MessageHandler(filters.TEXT, take_id)],
        TAKE_GIFT : [MessageHandler(filters.TEXT, take_gift_user)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)




def main():
    bot_token = '6459322939:AAGdDl0kK0RwWtQhun4HMqe2TNCajb8ASAQ'
    app = Application.builder().token(bot_token).build()
    app.add_handler(create_conv_handler)
    app.add_handler(join_conv_handler)

    # Configure the command handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('info', info))
    # app.add_handler(CommandHandler('create_group', create_group))
    # app.add_handler(CommandHandler('join_group', join_group))
    
    # Start the bot
    app.run_polling()

    

if __name__ == '__main__':
    main()
    print(groups)