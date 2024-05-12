import logging
import re
import paramiko
import os
import psycopg2

from psycopg2 import Error
#from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler


TOKEN = os.getenv("TOKEN")

DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_USER = os.getenv("DB_USER")
DB_PORT = os.getenv("DB_PORT")
DB_DATABASE = os.getenv("DB_DATABASE")

RM_HOST = os.getenv("RM_HOST")
RM_PASSWORD = os.getenv("RM_PASSWORD")
RM_USER = os.getenv("RM_USER")
RM_PORT = os.getenv("RM_PORT")

host = RM_HOST
port = RM_PORT
username = RM_USER
password = RM_PASSWORD
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=username, password=password, port=port)

log_client = paramiko.SSHClient()
log_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
log_client.connect(hostname=DB_HOST, username='kykymana', password=123456, port=22)

# Подключаем логирование
logging.basicConfig(
    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

connection = None

try:
    connection = psycopg2.connect(user=DB_USER,
                                password=DB_PASSWORD,
                                host=DB_HOST,
                                port=DB_PORT,
                                database=DB_DATABASE)

    cursor = connection.cursor()
    logging.info("Подключение успешно выполнено")
except (Exception, Error) as error:
    logging.error("Ошибка при работе с PostgreSQL: %s", error)

phoneEmailList = []
phoneNumberList = []

def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')


def helpCommand(update: Update, context):
    update.message.reply_text('Commands:\n /find_email - поиск email адресов в тексте\n /find_phone_number - поиск телефонных номеров в тексте\n /verify_password - проверка сложности пароля\n /get_release - информация о релизе системы\n /get_uname - информация об архитектурe процессора, имени хоста системы и версии ядра\n /get_uptime - информация о времени работы\n /get_df - информация о состоянии файловой системы\n /get_free - информация о состоянии оперативной памяти\n /get_mpstat - информация о производительности системы\n /get_w - информация о работающих в данной системе пользователях\n /get_auths - последние 10 входов в систему\n /get_critical - последние 5 критических события\n /get_ps - информация о запущенных процессах\n /get_ss - информация об используемых портах\n /get_apt_list - информация об установленных пакетах\n /get_services - информация о запущенных сервисах')
    return ConversationHandler.END

def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'findPhoneNumbers'

def findEmailsCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска email-адресов: ')

    return 'findEmails'

def passwordVerifyCommand(update: Update, context):
    update.message.reply_text('Введите пароль:')

    return 'verifyPassword'

def getReleaseCommand(update: Update, context):
    stdin, stdout, stderr = client.exec_command('lsb_release -a')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getUnameCommand(update: Update, context):
    stdin, stdout, stderr = client.exec_command('uname -mrsn')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getUptimeCommand(update: Update, context):
    stdin, stdout, stderr = client.exec_command('uptime')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getDFCommand(update: Update, context):
    stdin, stdout, stderr = client.exec_command('df')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getFreeCommand(update: Update, context):
    stdin, stdout, stderr = client.exec_command('free')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getMPSTATCommand(update: Update, context):
    stdin, stdout, stderr = client.exec_command('mpstat')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getWCommand(update: Update, context):
    stdin, stdout, stderr = client.exec_command('w')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getAuthsCommand(update: Update, context):
    stdin, stdout, stderr = client.exec_command('last -10')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getCritCommand(update: Update, context):
    stdin, stdout, stderr = client.exec_command('journalctl -p crit -n 5')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getPSCommand(update: Update, context):
    stdin, stdout, stderr = client.exec_command('ps')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getSSCommand(update: Update, context):
    stdin, stdout, stderr = client.exec_command('ss -tuln')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getAPTCommand(update: Update, context):
    update.message.reply_text('Выберите действие:\n Вывод информации о всех установленных пакетах - 1\n Вывод информации о конкретном пакете - 2')
    return 'getAllAPT'

def getServiceCommand(update: Update, context):
    stdin, stdout, stderr = client.exec_command('service --status-all | grep \'+\'')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getLogsCommand(update: Update, context):
    stdin, stdout, stderr = log_client.exec_command('cat /var/log/postgresql/postgresql.log | tail -n 10')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    decoded_text = bytes(data, "utf-8").decode("unicode_escape").encode("latin1").decode("utf-8")
    update.message.reply_text(decoded_text)
    return ConversationHandler.END

def getEmailsCommand(update: Update, context):
    try:
        cursor.execute("SELECT email FROM emails;")
        data = cursor.fetchall()
        string = ''
        for row in data:
            string += str(row)[2:-3] + '\n' 
        decoded_text = bytes(string, "utf-8").decode("unicode_escape").encode("latin1").decode("utf-8")
        update.message.reply_text(decoded_text)
        return ConversationHandler.END
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
        return ConversationHandler.END


def getPhonesCommand(update: Update, context):
    try:
        cursor.execute("SELECT phone FROM numbers;")
        data = cursor.fetchall()
        string = ''
        for row in data:
            string += str(row)[2:-3] + '\n' 
        decoded_text = bytes(string, "utf-8").decode("unicode_escape").encode("latin1").decode("utf-8")
        update.message.reply_text(decoded_text)
        return ConversationHandler.END
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
        return ConversationHandler.END

def getAllAPT(update: Update, context):
    user_input = update.message.text
    if user_input == '1':
        stdin, stdout, stderr = client.exec_command('dpkg --get-selections | head -n 20')
        data = stdout.read() + stderr.read()
        data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
        lines = data.split('\n')
        for i in range(0, len(lines), 50):
            update.message.reply_text('\n'.join(lines[i:i+50]))
        return ConversationHandler.END
    elif user_input == '2':
        update.message.reply_text('Введите название пакета:')
        return 'getAPTPacket'
    else:
        update.message.reply_text('Неверный ввод') 
        return ConversationHandler.END

def getAPTPacket(update: Update, context):
    user_input = update.message.text
    stdin, stdout, stderr = client.exec_command('dpkg -l ' + user_input)
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END


def findPhoneNumbers (update: Update, context):
    user_input = update.message.text

    global phoneNumberList

    phoneNumRegex = re.compile(r'(?:\+7|8)[ -]?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}') # форматы номеров      

    phoneNumberList = phoneNumRegex.findall(user_input)

    if not phoneNumberList:
        update.message.reply_text('Телефонные номера не найдены')
        return ConversationHandler.END
    
    phoneNumbers = ''
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i+1}. {phoneNumberList[i]}\n'
        
    update.message.reply_text(phoneNumbers)
    update.message.reply_text('Записать найденные телефоны в базу данных?\nДа - 1\nНет - 2')
    return 'phoneChoice'


def getPhoneChoice(update: Update, context):
    user_input = update.message.text
    if user_input == '1':
        for i in range(len(phoneNumberList)):
           string = "('" + phoneNumberList[i] + "')"
           cursor.execute("INSERT INTO numbers (phone) VALUES " + string + ";")
        connection.commit()
        return ConversationHandler.END
    elif user_input == '2':
        return ConversationHandler.END
    else:
        update.message.reply_text('Неверный ввод') 
        return ConversationHandler.END

def findEmails(update: Update, context):
    user_input = update.message.text
    global phoneEmailList
    phoneEmailRegex = re.compile(r'[^\s\W][^\s@]+@\S+\.[a-zA-Z0-9-.]{1,254}[^.\s]') # форматы адресов     

    phoneEmailList = phoneEmailRegex.findall(user_input)

    if not phoneEmailList:
        update.message.reply_text('Адреса не найдены')
        return ConversationHandler.END
    
    Emails = ''
    for i in range(len(phoneEmailList)):
        Emails += f'{i+1}. {phoneEmailList[i]}\n'
        
    update.message.reply_text(Emails)
    update.message.reply_text('Записать найденные адреса в базу данных?\nДа - 1\nНет - 2')
    return 'emailChoice'

def getEmailChoice(update: Update, context):
    user_input = update.message.text
    if user_input == '1':
        for i in range(len(phoneEmailList)):
           string = "('" + phoneEmailList[i] + "')"
           cursor.execute("INSERT INTO emails (email) VALUES " + string + ";")
        connection.commit()
        return ConversationHandler.END
    elif user_input == '2':
        return ConversationHandler.END
    else:
        update.message.reply_text('Неверный ввод') 
        return ConversationHandler.END

def verifyPassword(update: Update, context):
    user_input = update.message.text

    phonePasswordRegex = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()]).{8,}$') # формат пароля   

    phonePasswordVerify = phonePasswordRegex.search(user_input)

    if not phonePasswordVerify:
        update.message.reply_text('Пароль простой')
        return ConversationHandler.END
    else:
        update.message.reply_text('Пароль сложный')
        return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Обработчик диалога
    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumbersCommand)],
        states={
            'findPhoneNumbers': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbers)],
            'phoneChoice': [MessageHandler(Filters.text & ~Filters.command, getPhoneChoice)],
        },
        fallbacks=[]
    )

    convHandlerFindEmails = ConversationHandler(
        entry_points=[CommandHandler('find_email', findEmailsCommand)],
        states={
            'findEmails': [MessageHandler(Filters.text & ~Filters.command, findEmails)],
            'emailChoice': [MessageHandler(Filters.text & ~Filters.command, getEmailChoice)],
        },
        fallbacks=[]
    )

    convHandlerPasswordVerify = ConversationHandler(
        entry_points=[CommandHandler('verify_password', passwordVerifyCommand)],
        states={
            'verifyPassword': [MessageHandler(Filters.text & ~Filters.command, verifyPassword)],
        },
        fallbacks=[]
    )

    convHandlerGetRelease = ConversationHandler(
        entry_points=[CommandHandler('get_release', getReleaseCommand)],
        states={},fallbacks=[]
    )

    convHandlerGetUname = ConversationHandler(
        entry_points=[CommandHandler('get_uname', getUnameCommand)],
        states={},fallbacks=[]
    )

    convHandlerGetUptime = ConversationHandler(
        entry_points=[CommandHandler('get_uptime', getUptimeCommand)],
        states={},fallbacks=[]
    )
    convHandlerGetDF = ConversationHandler(
        entry_points=[CommandHandler('get_df', getDFCommand)],
        states={},fallbacks=[]
    )
    convHandlerGetFree = ConversationHandler(
        entry_points=[CommandHandler('get_free', getFreeCommand)],
        states={},fallbacks=[]
    )
    convHandlerGetMPSTAT = ConversationHandler(
        entry_points=[CommandHandler('get_mpstat', getMPSTATCommand)],
        states={},fallbacks=[]
    )
    convHandlerGetW = ConversationHandler(
        entry_points=[CommandHandler('get_w', getWCommand)],
        states={},fallbacks=[]
    )
    convHandlerGetAuths = ConversationHandler(
        entry_points=[CommandHandler('get_auths', getAuthsCommand)],
        states={},fallbacks=[]
    )
    convHandlerGetCritical = ConversationHandler(
        entry_points=[CommandHandler('get_critical', getCritCommand)],
        states={},fallbacks=[]
    )
    convHandlerGetPS = ConversationHandler(
        entry_points=[CommandHandler('get_ps', getPSCommand)],
        states={},fallbacks=[]
    )
    convHandlerGetSS = ConversationHandler(
        entry_points=[CommandHandler('get_ss', getSSCommand)],
        states={},fallbacks=[]
    )
    convHandlerGetAPT = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', getAPTCommand)],
        states={
            'getAllAPT': [MessageHandler(Filters.text & ~Filters.command, getAllAPT)],
            'getAPTPacket': [MessageHandler(Filters.text & ~Filters.command, getAPTPacket)],
        },
        fallbacks=[]
    )
    convHandlerGetService = ConversationHandler(
        entry_points=[CommandHandler('get_services', getServiceCommand)],
        states={},fallbacks=[]
    )
    convHandlerGetLogs = ConversationHandler(
        entry_points=[CommandHandler('get_repl_logs', getLogsCommand)],
        states={},fallbacks=[]
    )
    convHandlerGetEmails = ConversationHandler(
        entry_points=[CommandHandler('get_emails', getEmailsCommand)],
        states={},fallbacks=[]
    )
    convHandlerGetPhones = ConversationHandler(
        entry_points=[CommandHandler('get_phone_numbers', getPhonesCommand)],
        states={},fallbacks=[]
    )
		
	# Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmails)
    dp.add_handler(convHandlerPasswordVerify)
    dp.add_handler(convHandlerGetRelease)
    dp.add_handler(convHandlerGetUname)
    dp.add_handler(convHandlerGetUptime)
    dp.add_handler(convHandlerGetDF)
    dp.add_handler(convHandlerGetFree)
    dp.add_handler(convHandlerGetMPSTAT)
    dp.add_handler(convHandlerGetW)
    dp.add_handler(convHandlerGetAuths)
    dp.add_handler(convHandlerGetCritical)
    dp.add_handler(convHandlerGetPS)
    dp.add_handler(convHandlerGetSS)
    dp.add_handler(convHandlerGetAPT)
    dp.add_handler(convHandlerGetService)
    dp.add_handler(convHandlerGetLogs)
    dp.add_handler(convHandlerGetEmails)
    dp.add_handler(convHandlerGetPhones)

	# Запускаем бота
    updater.start_polling()

	# Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
