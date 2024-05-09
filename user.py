from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

async def send_invite(update: Update, context: CallbackContext):
    # Manually created group link
    group_link = "https://t.me/Secret_Santa_KK_bot"

    keyboard = [
        [
            InlineKeyboardButton("Join", callback_data='join'),
            InlineKeyboardButton("Reject", callback_data='reject'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Here is a Secret Santa group you are invited to by "admin".', reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext):
    query = update.callback_query

    # CallbackQueries need to be answered
    await query.answer()

    if query.data == "reject":
        await query.edit_message_text(text="You chose to reject the invitation.")
        print("Goodbye")
    elif query.data == "join":
        user_id = update.effective_user.id
        # Save the user ID or perform any other necessary action
        print(f"User {user_id} joined the group.")