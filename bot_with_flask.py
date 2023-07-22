# Offical documentation: https://pypi.org/project/pyTelegramBotAPI
import telebot
import logging
from telebot import types
#from handle_drive import get_main_ids, get_sub_list, get_file DIABLED DUE TO MISSING CRED FILE
from flask import Flask, request
import time
app = Flask(__name__)
# logging
logging.basicConfig(filename="logs.log",
                    filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

# activity logging
activity_log = logging.getLogger('activity')
activity_handler = logging.FileHandler(
    'activity.log', mode='a', encoding='utf-8')
activity_formater = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s')
activity_handler.setFormatter(activity_formater)
activity_log.addHandler(activity_handler)
activity_log.setLevel(logging.INFO)
activity_log.propagate = False

API_KEY = ""
# Threaded is set to false to be compatible with pythonanywhere.com
bot = telebot.TeleBot(API_KEY, parse_mode=None, threaded=False)
SECRET = "*A secret string used for webhook security*"
bot.delete_webhook()
if bot.get_webhook_info().url == '':
    time.sleep(1)
    # Instructs telegram to send updates to this url
    bot.set_webhook(url=f"*Hosting service URL*/{SECRET}")

# Message handlers - these functions are called when a user sends a message to the bot


@bot.message_handler(commands=['עזרה', 'start', 'help'])
def get_help(message):
    reply = '''
        היי\\!
        בשביל לדבר איתי\\, נסה לכתוב את אחת הפקודות הבאות:
        *\\/טלפונים*
        *\\/אוטובוס*
        *\\/תפילות*
        *\\/דרייב \\(בשביל לקבל קובץ מהדרייב של סמסטר א\\)*
        *\\/מי\\_בנה\\_תבוט\\_המטורף\\_הזה*
        '''
    try:
        if message.chat.type == 'private':
            bot.reply_to(message, reply, parse_mode='MarkdownV2')
            activity_log.info(
                f"sent help message to {message.from_user.first_name+ ' ' + message.from_user.last_name}")
        else:
            bot.reply_to(message, reply, parse_mode='MarkdownV2')
            activity_log.info(
                f"Sent help to {message.from_user.first_name + ' ' + message.from_user.last_name} in {message.chat.title}")
    except Exception as e:
        logging.exception(
            f"Could not send the reply to {message.from_user.first_name + ' ' + message.from_user.last_name} at {message.from_user.id}")


@bot.message_handler(commands=['טלפונים', 'contact_info'])
def information(message):
    reply = '''
    *מזכירות מדעי המחשב*
    __שעות פעילות:__ ימים ראשון \\- חמישי, 8:30 עד 15:00
    __מספר טלפון:__ 03\\-5318866
    _מייל:_ bsc@cs\.biu\.ac\.il

    *אוניברסיטה  כללי*
    __מספר להודעות וואצפ:__ 052\\-6171988
    __מספר טלפון:__ 035317000 \(ימים א' \\- ה' 9:00 עד 17:00\)
    '''
    try:
        if message.chat.type == 'private':
            bot.reply_to(message, reply, parse_mode='MarkdownV2')
            activity_log.info(
                f"Sent contact info to {message.from_user.first_name + ' ' + message.from_user.last_name}")
        else:
            bot.reply_to(message, reply, parse_mode='MarkdownV2')
            activity_log.info(
                f"Sent contact info to {message.from_user.first_name + ' ' + message.from_user.last_name} in {message.chat.title}")
    except Exception as e:
        logging.exception(
            f"Could not send the reply to {message.from_user.first_name + ' ' + message.from_user.last_name} at {message.from_user.id}")


@bot.message_handler(commands=['תפילות', 'prayer'])
def prayer(message):
    reply = '''
    *מנחה*
    12:30\\, 13:35\\, 14:30\\, 15:35

    *ערבית*
    17:35\\, 19:35
    '''
    try:
        if message.chat.type == 'private':
            bot.reply_to(message, reply, parse_mode='MarkdownV2')
            activity_log.info(
                f"Sent prayer times to {message.from_user.first_name + ' ' + message.from_user.last_name}")
        else:
            bot.reply_to(message, reply, parse_mode='MarkdownV2')
            activity_log.info(
                f"Sent prayer times to {message.from_user.first_name + ' ' + message.from_user.last_name} in {message.chat.title}")
    except Exception as e:
        logging.exception(
            f"Could not send the reply to {message.from_user.first_name + ' ' + message.from_user.last_name} at {message.from_user.id}")


@bot.message_handler(commands=['אוטובוס', 'bus'])
def public_transport(message):
    reply = '''
    *אפליקציית מיקום תחנות ושאטלים בזמן אמת\\:*
    https\\:\\/\\/biu\\.tracer\\.co\\.il\\/

    *זמינות שאטלים\\:*
    ימים א\\' עד ה\\' בין השעות 7\\:30 עד 20\\:00
    '''
    try:
        if message.chat.type == 'private':
            bot.reply_to(message, reply, parse_mode='MarkdownV2')
            activity_log.info(
                f"Sent public transport info to {message.from_user.first_name + ' ' + message.from_user.last_name}")
        else:
            bot.reply_to(message, reply, parse_mode='MarkdownV2')
            activity_log.info(
                f"Sent public transport info to {message.from_user.first_name + ' ' + message.from_user.last_name} in {message.chat.title}")
    except Exception as e:
        logging.exception(
            f"Could not send the reply to {message.from_user.first_name + ' ' + message.from_user.last_name} at {message.from_user.id}")

#The drive function is written here. It is currently disabled due to missing CRED file

# def send_file(message, file_id: str):
#     request, file_name = get_file(file_id)
#     try:
#         bot.send_document(message.from_user.id, request,
#                           visible_file_name=f"{file_name['name']}")
#         activity_log.info(
#             f"Sent file: {file_name} to {message.from_user.first_name + ' ' + message.from_user.last_name}")
#     except Exception as e:
#         logging.exception(
#             f"Could not send the file: {file_name} to {message.from_user.first_name + ' ' + message.from_user.last_name} at {message.from_user.id}")


# @bot.message_handler(commands=['דרייב', 'drive'])
# def drive_1(message):
#     if message.from_user.type != 'private':
#         bot.reply_to(
#             message, "פקודה זו מיועדת לצ\'אט פרטי בלבד על מנת לא ללכלך את הקבוצה ;)")
#         return
#     current_drive = get_main_ids()  # gets ids of the main folder
#     folders = []
#     # creates a list of folder names for the markup
#     for folder in current_drive['name']:
#         folders.append(str(folder))
#     markup = types.ReplyKeyboardMarkup(row_width=2)
#     for i in range(len(folders)):
#         locals()[f"folderbtn_{i}"] = types.KeyboardButton(folders[i])
#         exec(f"markup.add(folderbtn_{i})")  # add markup buttons
#     sent = bot.reply_to(
#         message, 'איזה נושא תרצה לבחור?', reply_markup=markup)
#     # hands response to next function to handle
#     bot.register_next_step_handler(sent, drive_2, current_drive)


# def drive_2(message, current_drive):
#     trash = ['נושא: ', 'קובץ: ']  # these words are not relevent
#     answer = message.text  # user response
#     for word in trash:  # will delete 'trash' out of user response
#         answer = answer.replace(word, '')
#     print(f"debug: answer is {answer}")
#     ### next 6 lines are to make sure user didnt write something other then file name###
#     # stores data frame
#     test_empty = current_drive.loc[current_drive['name']
#                                    == answer, 'mimeType']
#     # .empty returns True if dataframe is empty (when no match has been found)
#     if not test_empty.empty:
#         # ifnot empty, everything goes as usual
#         file_type = str(
#             current_drive.loc[current_drive['name'] == answer, 'mimeType'])
#     else:
#         bot.reply_to(
#             message, 'הקובץ שנבחר לא נמצא (בבקשה נסה שוב ובחר קובץ מאחת האפשרויות)')
#         return  # terminates function
#     print(f"debug: filetype is {file_type}")
#     # test if selection is a folder, or something else
#     if 'application/vnd.google-apps.folder' not in file_type:
#         file_id = current_drive.loc[current_drive['name']
#                                     == answer, 'id'].values[0]
#         print(f"debug: fileId is {file_id}")
#         send_file(message, file_id)
#         markup = types.ReplyKeyboardRemove()  # removes the buttons
#         bot.reply_to(message, 'הקובץ נשלח בהצלחה (אני מקווה)',
#                      reply_markup=markup)
#     else:  # when selection is a folder, logic to get the files in the folder is launched
#         next_drive = current_drive.loc[current_drive['name']
#                                        == answer, 'id'].values[0]
#         print(f"debug: next drive is {next_drive}")
#         current_drive = get_sub_list(next_drive)
#         folders = []
#         files = []
#         # test if folder, and if so adds to the list
#         for folder in current_drive.loc[current_drive['mimeType'] == 'application/vnd.google-apps.folder', 'name']:
#             folders.append(f'נושא: {str(folder)}')
#         # tests if not folder, and adds to list
#         for file in current_drive.loc[current_drive['mimeType'] != 'application/vnd.google-apps.folder', 'name']:
#             files.append(f'קובץ: {str(file)}')
#         markup = types.ReplyKeyboardMarkup(
#             row_width=2)  # initializes button creation
#         for i in range(len(folders)):
#             locals()[f"folderbtn_{i}"] = types.KeyboardButton(
#                 folders[i])  # add list to markup buttons
#             exec(f"markup.add(folderbtn_{i})")
#         for i in range(len(files)):
#             locals()[f"filebtn_{i}"] = types.KeyboardButton(
#                 files[i])  # add list to markup buttons
#             exec(f"markup.add(filebtn_{i})")
#         sent = bot.reply_to(message, 'בחר קובץ/תת-נושא',
#                             reply_markup=markup)
#         # restarts the function with latest user answer
#         bot.register_next_step_handler(sent, drive_2, current_drive)


@bot.message_handler(commands=['מי_בנה_תבוט_המטורף_הזה', 'credits'])
def credits(message):
    reply = '''
    כרגע רק על ידי\\. *אבל אולי בקרוב גם על ידך\\!*
    יש לך ידע בסיסי\\+ בפייתון\\? רוצה להיות חלק מהפרוייקט\\? דברו איתי ואסביר לכם על הקוד\\, וגם אתם תוכלו ליצור פקודות לבוט שישמשו את כולם\\!\\
    '''
    try:
        bot.reply_to(message, reply, parse_mode='MarkdownV2')
        activity_log.info(
            f"Sent credits to {message.from_user.first_name + ' ' + message.from_user.last_name}")
    except Exception as e:
        logging.exception(
            f"Could not send the reply to {message.from_user.first_name + ' ' + message.from_user.last_name} at {message.from_user.id}")

# Anon questions feature - currently disabled
# @bot.message_handler(commands=['שאלה_אנונימית', 'anon_question'])
# def anon_question(message):
#     if message.from_user.type != 'private':
#         bot.reply_to(
#             message, 'שאלות אנונימיות אפשר לשאול אותי רק בפרטי, מסיבות ברורות...')
#         return
#     explanation = '''פקודה זו מאפשרת לכם לשלוח לבוט הודעה.
#     הבוט יעביר את ההודעה שלכם לקבוצה הראשית ללא פרטים מזהים.
#     הבוט לא ישמור לוגים בנוגע לבקשה שלכם.
#     אסור בשום פנים לשלוח הודעות שמיועדות לפגיעה באדם אחר בקבוצה.
#     הודעות פוגעניות יאלצו אותי לחסום את האופציה הזו.
#     האם תרצה להמשיך?'''
#     markup = types.ReplyKeyboardMarkup(row_width=2)
#     yesbtn = types.KeyboardButton('כן')
#     nobtn = types.KeyboardButton('לא')
#     markup.add(yesbtn, nobtn)
#     sent = bot.reply_to(message, explanation, reply_markup=markup)
#     bot.register_next_step_handler(sent, anon_question_2)


# def anon_question_2(message):
#     markup = types.ReplyKeyboardRemove()
#     if message.text == 'כן':
#         sent = bot.reply_to(
#             message, 'אנא כתוב את ההודעה שברצונך לשלוח.', reply_markup=markup)
#         bot.register_next_step_handler(sent, anon_question_3)
#     else:
#         markup = types.ReplyKeyboardRemove()
#         bot.reply_to(message, 'הפעולה בוטלה.', reply_markup=markup)


# def anon_question_3(message):
#     question = message.text
#     try:
#         bot.send_message(-1887058598,
#                          f"נשלחה הודעה אנונימית\\:\n{question}", parse_mode='MarkdownV2')
#         bot.reply_to(message, 'ההודעה נשלחה.')
#     except Exception as e:
#         logging.exception(
#             f"Could not send anonnymous question")

# Flask routes
@app.route('/')  # default route of the app, used for testing
def test():
    return "<h1>hello there</h1>"

# Webhooks route, telegram sends updates here
@app.route(f"/{SECRET}", methods=['POST'])
def main():  
    update = telebot.types.Update.de_json(  # creates update object from json provided by telegram
        request.stream.read().decode('utf-8'))
    # bot goes over update and reacts accordingly
    bot.process_new_updates([update])

    return "OK", 200
