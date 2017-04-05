# -*- coding: utf-8 -*-
__author__ = 'Rico'

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from app.message_types import MessageTypes
import logging


# BOT_TOKEN = <your-API-Token-here>

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher
# bot = updater.bot

chatting_users = []
searching_users = []
DEV_ID = 24421134
bot_sends = "\U0001F916 Bot: "
stranger_sends = "\U0001F464 Stranger: "

def get_partner_id(user_id):
    if len(chatting_users) > 0:
        for pair in chatting_users:
            if pair[0] == user_id:
                return int(pair[1])

    return None

# checks if user is already chatting with someone
def is_user_already_chatting(user_id):
    counter = 0
    if len(chatting_users) > 0:
        for pair in chatting_users:
            if pair[0] == user_id:
                return counter
            counter += 1

    return -1

def is_user_already_searching( user_id):
    counter = 0
    if len(searching_users) > 0:
        for user in searching_users:
            if user == user_id:
                return counter
            counter += 1

    return -1


def start(bot, update):
    user_id = update.message.from_user.id

    if (user_id not in searching_users) and (is_user_already_chatting(user_id) == -1):
        # search for another "searching" user in searching_users list
        if len(searching_users) > 0:
            # delete the other searching users from the list of searching_users
            print("Another user is searching now. There are 2 users. Matching them now!")
            partner_id = searching_users[0]
            del searching_users[0]

            # add both users to the list of chatting users with the user_id of the other user.
            chatting_users.append([user_id, partner_id])
            chatting_users.append([partner_id, user_id])

            bot.send_message(user_id, bot_sends + "You are connected to a stranger. Have fun and be nice!",
                                  parse_mode="Markdown")
            bot.send_message(partner_id, bot_sends + "You are connected to a stranger. Have fun and be nice!",
                                  parse_mode="Markdown")
        else:
            # if no user is searching, add him to the list of searching users.
            # TODO later when you can search for specific gender, this condition must be changed
            searching_users.append(user_id)
            bot.send_message(user_id, bot_sends + "Added you to the searching users!",
                                  parse_mode="Markdown")
    elif user_id in searching_users:
        bot.send_message(user_id, bot_sends + "You are already searching. Please wait!", parse_mode="Markdown")


def stop(bot, update):
    user_id = update.message.from_user.id

    if (user_id in searching_users) or (is_user_already_chatting(user_id) >= 0):

        if user_id in searching_users:
            # remove user from searching users
            index = is_user_already_searching(user_id)
            del searching_users[index]
            bot.send_message(user_id, bot_sends + "Stopped searching for users!", parse_mode="Markdown")

        elif is_user_already_chatting(user_id) >= 0:
            # remove both users from chatting users
            partner_id = get_partner_id(user_id)

            index = is_user_already_chatting(user_id)
            del chatting_users[index]

            partner_index = is_user_already_chatting(partner_id)
            del chatting_users[partner_index]

            # send message that other user left the chat
            bot.send_message(partner_id, bot_sends + "Your partner left the chat", parse_mode="Markdown")
            bot.send_message(user_id, bot_sends + "You left the chat!", parse_mode="Markdown")


def messages(bot, update):
    user_id = update.message.from_user.id
    text = update.message.text

    if text is not None and text is not "":
        # If message is text
        logger.debug("Update is text")
        text = str(update.message.text)
        message_type = MessageTypes.TYPE_TEXT
    elif update.message.photo is not None and update.message.photo != []:
        logger.debug("Update is photo")
        print(update.message.photo)
        message_type = MessageTypes.TYPE_PHOTO
    elif update.message.sticker is not None and update.message.sticker != []:
        logger.debug("Update is sticker")
        message_type = MessageTypes.TYPE_STICKER
    elif update.message.voice is not None and update.message.voice != []:
        logger.debug("Update is voice")
        message_type = MessageTypes.TYPE_VOICE
    elif update.message.audio is not None and update.message.audio != []:
        logger.debug("Update is audio")
        message_type = MessageTypes.TYPE_AUDIO
    elif update.message.video is not None and update.message.video != []:
        logger.debug("Update is video")
        message_type = MessageTypes.TYPE_VIDEO
    elif update.message.document is not None and update.message.document != []:
        logger.debug("Update is document")
        message_type = MessageTypes.TYPE_FILE
    else:
        # Setting type to "text", so that the partner get's notified of it
        print("* Someone sent some unsupported media*")
        message_type = MessageTypes.TYPE_TEXT

    if (user_id not in searching_users) and (is_user_already_chatting(user_id) >= 0):
        # send message directly to the other chat
        partner_id = get_partner_id(user_id)
        # additional check, that there is indeed a partner.
        if partner_id != -1:
            if message_type == MessageTypes.TYPE_TEXT:
                message = stranger_sends + text
                bot.send_message(partner_id, message)
            elif message_type == MessageTypes.TYPE_PHOTO:
                file_id = ""
                last_file_size = 0
                for photo in update.message.photo:
                    if photo.file_size >= last_file_size:
                        file_id = photo.file_id
                bot.send_photo(partner_id, file_id)
                print("sent file with size: " + str(last_file_size))
            elif message_type == MessageTypes.TYPE_STICKER:
                bot.send_sticker(partner_id, update.message.sticker.file_id)
            elif message_type == MessageTypes.TYPE_VOICE:
                bot.send_voice(partner_id, update.message.voice.file_id,
                                    duration=update.message.voice.duration)
            elif message_type == MessageTypes.TYPE_AUDIO:
                bot.send_audio(partner_id, update.message.audio.file_id)
            elif message_type == MessageTypes.TYPE_VIDEO:
                bot.send_video(partner_id, update.message.video.file_id)
            elif message_type == MessageTypes.TYPE_FILE:
                bot.send_document(partner_id, update.message.document.file_id)
        else:
            print("Something went wrong! There is no partner in the list, while there should be!")


start_handler = CommandHandler('start', start)
stop_handler = CommandHandler('stop', stop)
message_handler = MessageHandler(Filters.all, messages)

for handler in [start_handler, stop_handler, message_handler]:
    dispatcher.add_handler(handler)

updater.start_polling()
