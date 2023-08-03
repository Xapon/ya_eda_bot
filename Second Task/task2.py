from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials	
import logging


#По хорошему бота бы раскидать по разным файлам, да на вебхуках, но для наглядности тестового задания запакую всё в один файл



credential_file = 'test-394801-a9e602a1b9f5.json'  #Код я дам, токен я - не - дам
credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_file, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http()) 
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) 

spreadsheetId = '1EwGW1VxFhLnQjubuwScPSdO74CdMDHV8hux04cNF5K8' 


memory = MemoryStorage()
test_bot = Bot(token='1594278469:AAFbWmU1KmxeWpXrfLQ25J72DuL20uXAjd4')
dp = Dispatcher(test_bot, storage=memory)
#Токена тут быть не должно, по хорошему, но так как это мой тестовый бот исключительно тестов ради, то пусть будет
#https://t.me/ya_eda_test_bot




async def on_startup(_):
    logging.basicConfig(level=logging.ERROR,filename="log.log")

@dp.message_handler(commands=['start','help'])
async def send_message(message : types.Message):
    await message.answer('Привет! Это тестовый бот. Отправь мне что нибудь')

@dp.message_handler()
async def send_to_sheet(message : types.Message):
    #В идеальном мире лучше хранить последнюю заполненную ячейку где нибудь на постоянной основе, чтобы не душить API запросами, но в тз не было, так что
    print(message.from_user.username, message.text, message.date.strftime('%D %H:%M:%S'))
    
    i = 1
    while True:
        try:
            ranges = [f"List 1!A{i}"]
            results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                        ranges = ranges).execute() 
            print(results['valueRanges'][0]['values'])
            i=i+1
            print(i)
        except(KeyError):
            print('now')
            results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
                        "valueInputOption": "USER_ENTERED", 
                        "data": [
                            {
                                "range": f"List 1!A{i}:C{i}",
                                "values": [
                                        [message.from_user.username, message.text, message.date.strftime('%D %H:%M:%S')]
                                        ]
                            }
                                ]
                                                                                                        }).execute()
            break





def register_handler_client(dp : Dispatcher):
    dp.register_message_handler(send_message,commands='start')
    dp.register_message_handler(send_to_sheet)








executor.start_polling(dp, skip_updates=True, on_startup=on_startup)