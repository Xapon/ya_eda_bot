import telebot
bot = telebot.TeleBot('TOKEN')

@bot.message_handler(commands=['start'])
def copy_past(message):
    s1 = message
    bot.reply_to(message.from_user.id, s1)
bot.polling(none_stop=True)
