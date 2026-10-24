import telebot
import subprocess
import re

# ЗАМЕНИ ТЕКСТ В КАВЫЧКАХ НА СВОЙ ТОКЕН ОТ BOTFATHER!
TOKEN = '8855465596:AAHoe9qFwdzBU9DGmusTy12A1d3REl0399A'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне никнейм, и я найду его профили на сайтах.")

@bot.message_handler(func=lambda message: True)
def search_username(message):
    username = message.text.strip()
    if username.startswith('@'):
        username = username[1:]
    if not re.match(r"^[a-zA-Z0-9._-]+$", username):
        bot.reply_to(message, "Некорректный ник. Используй латиницу, цифры и знаки . _ -")
        return
    bot.reply_to(message, f"Ищу профили для: {username}...\nЭто займет около минуты.")
    try:
        result = subprocess.run(
            ['sherlock', username, '--print-found'],
            capture_output=True, text=True, timeout=120
        )
        output = result.stdout.strip()
        clean_output = ""
        for line in output.split('\n'):
            if "Sorry, this username is invalid" not in line and "Error" not in line:
                clean_output += line + "\n"
        clean_output = clean_output.strip()
        if clean_output:
            if len(clean_output) > 4000:
                clean_output = clean_output[:4000] + "\n...список слишком длинный."
            bot.send_message(message.chat.id, f"Результаты:\n\n{clean_output}")
        else:
            bot.send_message(message.chat.id, "Ничего не найдено.")
    except subprocess.TimeoutExpired:
        bot.send_message(message.chat.id, "Время ожидания истекло.")
    except Exception:
        bot.send_message(message.chat.id, "Произошла ошибка при поиске.")

if __name__ == '__main__':
    bot.infinity_polling()
