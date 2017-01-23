# -*- coding: utf-8 -*-
__author__ = 'Rico'


def get_updates(offset, bot):
    updates = bot.get_updates(offset + 1).wait()
    returnlist = []

    if bool(updates) and updates:
        print("\n--- Processing new updates: ---")
        for update in updates:
            if update is not None:
                try:
                    # templist = []
                    # user_id = update.message.sender.id
                    # first_name = update.message.sender.first_name
                    # last_name = update.message.sender.last_name
                    # username = update.message.sender.username
                    # chat_id = update.message.chat.id
                    # message_id = update.message.message_id
                    # update_id = update.update_id
                    # text = update.message.text
                    # upd_time = int(update.message.date)
                    # reply_message_text = ""

                    #not_saved = -1
                    #if check_if_user_saved(user_id) == not_saved:
                    #    sql_write(user_id, "en", first_name, last_name, username)  # add new user to db

                    #st = datetime.datetime.fromtimestamp(upd_time).strftime('%Y-%m-%d %H:%M:%S')
                    #print(st + "  -  First name: " + str(first_name) + " | Last name: " + str(last_name) + " | Username: " + str(username) + " | UserID: " + str(user_id) + " | ChatType: " + str(chat_type) + " | Message: " + str(text))
                    # templist.extend((user_id, update_id, first_name, last_name, text, chat_type, chat_id, message_id, username, reply_message_text))
                    returnlist.append(update)
                except AttributeError as attibuteError:
                    print("AttributeError happened!\n")
                    print(update)
                    print(attibuteError)
        return returnlist
    else:
        return None
