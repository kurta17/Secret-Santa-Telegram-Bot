from telegram.ext import Application, MessageHandler, filters, CommandHandler, CallbackContext,ConversationHandler
from telegram import Update, ReplyKeyboardMarkup
import uuid

def assign_gifters_and_receivers(members):
    assignments = {}
    for i in range(len(members)):
        gifter = members[i]
        receiver = members[(i + 1) % len(members)]
        assignments[gifter] = receiver
    return assignments


# Dict to store group data
groups = {}


async def start(update: Update, context: CallbackContext):
    reply_keyboard = [['/start', '/create_group', '/join_group', '/info']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        'Hi! I am a Secret Santa Bot. I will help you to organize a Secret Santa event. '
        'To know more about me, type /info',
        reply_markup=markup
    )

async def info(update: Update, context: CallbackContext):
    await update.message.reply_text(
        'Welcome to the Secret Santa Bot!\n\n'
        'I will help you to organize a Secret Santa event. Here is how you can use me:\n\n'
        '/start - Start a new Secret Santa group\n'
        '/create_group - Create a new Secret Santa group\n'
        '/join_group - Join an existing Secret Santa group\n'
        '/info - Get information about the bot\n'
        '/assign_gift - Assign gifts to the members of the group\n'

)



ADMIN_NAME = 0
GROUP_NAME = 1
ADMIN_GIFT = 2

async def create_group(update: Update, context: CallbackContext):
    group_id = str(uuid.uuid4())
    admin_id = update.effective_user.id
    context.user_data["group_id"] = group_id
    groups[group_id] = {"admin": admin_id, "members": [admin_id], "admin_name": "", "group_name": "", "gift": [], "assignments": {} }
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
    await update.message.reply_text("Enter the group ID:")
    return TAKE_ID

async def take_id(update: Update, context: CallbackContext):
    group_id = update.message.text
    if group_id in groups:
        if update.effective_user.id not in groups[group_id]["members"]:
            groups[group_id]["members"].append(update.effective_user.id)
            context.user_data["group_id"] = group_id
            await update.message.reply_text("What gift do you want to receive?")
        else:
            await update.message.reply_text("You are already a member of this group")
    else:
        await update.message.reply_text("Invalid group ID")

    print(groups)
    return TAKE_GIFT

async def take_gift_user(update: Update, context: CallbackContext):
    gift = update.message.text
    group_id = context.user_data["group_id"]
    groups[group_id]["gift"].append(gift)
    print(groups)
    await update.message.reply_text('Wait until the group admin assigns the gifts to the members')
    return ConversationHandler.END



join_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('join_group', join_group)],
    states={
        TAKE_ID : [MessageHandler(filters.TEXT, take_id)],
        TAKE_GIFT : [MessageHandler(filters.TEXT, take_gift_user)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

async def assign_gift(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    group_id = context.user_data["group_id"]
    if user_id != groups[group_id]["admin"]:
        await update.message.reply_text("You are not a member of this group")
        return ConversationHandler.END
    members = groups[group_id]["members"]
    gifts = groups[group_id]["gift"]
    assignments = assign_gifters_and_receivers(members)
    groups[group_id]["assignments"] = assignments
    for gifter, receiver in assignments.items():
        receiver_index = members.index(receiver)
        receiver_gift = gifts[receiver_index]
        receiver_info = await context.bot.get_chat(receiver)
        receiver_name = receiver_info.first_name
        message = f"Hello, you are giving a gift to {receiver_name}. They would like to receive: {receiver_gift}."
        await context.bot.send_message(gifter, message)
    await update.message.reply_text("Gifts assigned successfully!")
    return ConversationHandler.END


def main():
    bot_token = '6459322939:AAGdDl0kK0RwWtQhun4HMqe2TNCajb8ASAQ'
    app = Application.builder().token(bot_token).build()
    app.add_handler(create_conv_handler)
    app.add_handler(join_conv_handler)

    # Configure the command handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('info', info))
    app.add_handler(CommandHandler('assign_gift', assign_gift))
    # app.add_handler(CommandHandler('create_group', create_group))
    # app.add_handler(CommandHandler('join_group', join_group))

    # Start the bot
    app.run_polling()



if __name__ == '__main__':
    main()
    print(groups)
