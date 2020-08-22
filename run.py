from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import requests
import re
from pprint import pprint 
from settings import API_KEY
import cv2
import webbrowser
import pyzbar.pyzbar as pyzbar
messages=[]
def get_url():
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url
def get_quotes():
    contents = requests.get('https://quotes.rest/qod?language=en').json()
    quote = contents['contents']['qoutes'][0]['background']
    return quote

def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url
def bop(bot, update):
    url = get_image_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)
    messages.append(update.message)
def q(bot, update):
    url = get_quotes()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)
    messages.append(update.message)
def echo(bot, update):
    if update.message.text=="hello":
        bot.send_message(chat_id=update.effective_chat.id,text="hello back😊")
        messages.append(update.message)
    else:
        bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text)
        messages.append(update.message)

def check_qr(bot,update):
    pprint(update.message)
    chat_id = update.message.chat_id
    photo = update.message.photo[-1]
    id_img = update.message.photo[-1].file_id
    foto = bot.getFile(id_img)
    new_file = bot.get_file(foto.file_id)
    new_file.download('qrcode.png')
    img = cv2.imread("qrcode.png")
    decodeObject=pyzbar.decode(img)
    if decodeObject:
        data=decodeObject[0].data
        if data is not None:
            bot.send_message(chat_id=chat_id, text=data.decode('utf-8'))
            messages.append(update.message)
    else:
        bot.send_message(chat_id=chat_id, text="Not Valid Qr Code")
        messages.append(update.message)
        # bot.send_photo(chat_id=chat_id, photo=photo)
    # if update.message.photo:
    #     chat_id = update.message.chat_id
    #     bot.send_photo(chat_id=chat_id, photo=photo)
def clear(bot, update):
    chat_id = update.message.chat_id
    if messages:
        for i in messages:
            try:
                id=i.message_id
                bot.delete_message(chat_id=chat_id , message_id=id)
            except Exception as e:
                print(e)
            messages.remove(i)
    else:
        bot.sendMessage(chat_id=chat_id,text="messages all cleared or empty")
# def start(bot,update):
#     bot.setChatPhoto(chat_id=update.message.chat_id ,photo='qrcode.png')
def main():
    updater = Updater(API_KEY)
    
    dp = updater.dispatcher
    # dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('bop',bop))
    dp.add_handler(CommandHandler('q',q))
    dp.add_handler(CommandHandler('clear',clear))
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    qr_handler = MessageHandler(Filters.photo,check_qr)
    dp.add_handler(echo_handler)
    dp.add_handler(qr_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
