#Offical documentation: https://pypi.org/project/pyTelegramBotAPI
import telebot
from telebot import types
from handle_drive import get_main_ids,get_sub_list,get_file
API_KEY="DEVELOPMENT ONLY"#This build is meant for development purposes
bot = telebot.TeleBot(API_KEY, parse_mode=None)
def main():
    @bot.message_handler(commands=['עזרה','start','help'])
    def get_help(possible_commands):
            reply='''
            היי\\!
            בשביל לדבר איתי\\, נסה לכתוב את אחת הפקודות הבאות:
            *\\/טלפונים*
            *\\/תפילות*
            *\\/תמונה \\(בשביל לקבל תמונה יפה\\)*
            *\\/דרייב \\(בשביל לקבל קובץ מהדרייב של סמסטר א\\)*
            
            '''
            bot.reply_to(possible_commands,reply,parse_mode='MarkdownV2')

    @bot.message_handler(commands=['טלפונים','contact_info'])
    def information(contact_info):
        reply='''
        *מזכירות מדעי המחשב*
        __שעות פעילות:__ ימים ראשון \\- חמישי, 8:30 עד 15:00
        __מספר טלפון:__ 03\\-5318866
        _מייל:_ bsc@cs\.biu\.ac\.il

        *אוניברסיטה  כללי*
        __מספר להודעות וואצפ:__ 052\\-6171988
        __מספר טלפון:__ 035317000 \(ימים א' \\- ה' 9:00 עד 17:00\)
        '''
        bot.reply_to(contact_info,reply,parse_mode='MarkdownV2')

    @bot.message_handler(commands=['תפילות','prayer'])
    def prayer(prayer_time):
        reply='''
        *מנחה*
        12:30\\, 13:35\\, 14:30\\, 15:35
        
        *ערבית*
        17:35\\, 19:35
        '''
        bot.reply_to(prayer_time,reply,parse_mode='MarkdownV2')


    @bot.message_handler(commands=['אוטובוס','bus'])
    def public_transport(message):
        reply='''
        *אפליקציית מיקום תחנות ושאטלים בזמן אמת\\:*
        https\\:\\/\\/biu\\.tracer\\.co\\.il\\/
        
        *זמינות שאטלים\\:*
        ימים א\\' עד ה\\' בין השעות 7\\:30 עד 20\\:00
        '''
        bot.reply_to(message,reply,parse_mode='MarkdownV2')

    @bot.message_handler(commands=['תמונה','pic'])
    def pic(message):
        photo=open('pexels-arnie-chou-1229042.jpg','rb')
        bot.send_photo(message.chat.id,photo)



    def send_file(message,file_id:str):
        request,file_name=get_file(file_id)
        bot.send_document(message.chat.id,request,visible_file_name=f"{file_name['name']}")

    @bot.message_handler(commands=['דרייב','drive'])
    def drive_1(message):
        current_drive=get_main_ids()#gets ids of the main folder
        folders=[]
        for folder in current_drive['name']:#creates a list of folder names for the markup
            folders.append(str(folder))
        markup=types.ReplyKeyboardMarkup(row_width=2)
        for i in range(len(folders)):
            locals()[f"folderbtn_{i}"]=types.KeyboardButton(folders[i])
            exec(f"markup.add(folderbtn_{i})")#add markup buttons
        sent=bot.reply_to(message,'איזה נושא תרצה לבחור?',reply_markup=markup)
        bot.register_next_step_handler(sent,drive_2,current_drive)#hands response to next function to handle
    def drive_2(message,current_drive):
        trash=['נושא: ','קובץ: '] #these words are not relevent
        answer=message.text#user response
        for word in trash: #will delete 'trash' out of user response
            answer=answer.replace(word,'')
        print(f"debug: answer is {answer}")
        ###next 6 lines are to make sure user didnt write something other then file name###
        test_empty=current_drive.loc[current_drive['name']==answer,'mimeType'] #stores data frame
        if not test_empty.empty: #.empty returns True if dataframe is empty (when no match has been found)
            file_type=str(current_drive.loc[current_drive['name']==answer,'mimeType']) #ifnot empty, everything goes as usual
        else:
            bot.reply_to(message,'הקובץ שנבחר לא נמצא (בבקשה נסה שוב ובחר קובץ מאחת האפשרויות)')
            return #terminates function
        print(f"debug: filetype is {file_type}")
        if 'application/vnd.google-apps.folder' not in file_type:#test if selection is a folder, or something else
            file_id=current_drive.loc[current_drive['name']==answer,'id'].values[0]
            print(f"debug: fileId is {file_id}")
            send_file(message,file_id)
            markup=types.ReplyKeyboardRemove()#removes the buttons
            bot.reply_to(message,'הקובץ נשלח בהצלחה (אני מקווה)',reply_markup=markup)
        else:#when selection is a folder, logic to get the files in the folder is launched
            next_drive=current_drive.loc[current_drive['name']==answer,'id'].values[0]
            print(f"debug: next drive is {next_drive}")
            current_drive=get_sub_list(next_drive)
            folders=[]
            files=[]
            for folder in current_drive.loc[current_drive['mimeType']=='application/vnd.google-apps.folder','name']:#test if folder, and if so adds to the list
                folders.append(f'נושא: {str(folder)}')
            for file in current_drive.loc[current_drive['mimeType']!='application/vnd.google-apps.folder','name']:#tests if not folder, and adds to list
                files.append(f'קובץ: {str(file)}')
            markup=types.ReplyKeyboardMarkup(row_width=2)#initializes button creation
            for i in range(len(folders)):
                locals()[f"folderbtn_{i}"]=types.KeyboardButton(folders[i])#add list to markup buttons
                exec(f"markup.add(folderbtn_{i})")
            for i in range(len(files)):
                locals()[f"filebtn_{i}"]=types.KeyboardButton(files[i])#add list to markup buttons
                exec(f"markup.add(filebtn_{i})")
            sent=bot.reply_to(message,'בחר קובץ/תת-נושא',reply_markup=markup)
            bot.register_next_step_handler(sent,drive_2,current_drive)#restarts the function with latest user answer
        
        

    #if a message has passed all the previous handlers, it is thus unknown to the bot. this handler takes any message.
    @bot.message_handler(func=lambda m: True)
    def unknown_message(message):
        reply='''מצטער, עוד לא למדתי את הפקודה הזאת.
        נסה לכתוב /עזרה בשביל לראות מה אני יודע!'''
        bot.reply_to(message,reply)

    bot.infinity_polling()#tells bot to listen for all incoming messages
main()