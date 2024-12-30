
import telebot
import requests
import random
from model import get_class

# Замени 'YOUR_TELEGRAM_BOT_TOKEN' на токен своего бота
bot = telebot.TeleBot('8194199463:AAEPqjzivtQ6Z6FNiJKpqy4zpQpuSVQUtk0')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Привет! Я бот для получения изображений отходов и анализа их опастности!")

@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    '''При отправке изображения, проводит его анализ'''
    # Проверяем, есть ли фотографии
    if not message.photo:
        return bot.send_message(message.chat.id, "Вы забыли загрузить картинку :(")

    # Получаем файл и сохраняем его
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]

    # Загружаем файл и сохраняем
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    # Анализируем изображение
    result = get_class(model_path="./keras_model.h5", labels_path="labels.txt", image_path=file_name)
    bot.send_message(message.chat.id, result)


facts = [
    "Все хранимые отходы должны быть помещены в специальные герметичные тары. На таре должен быть указан ФККО такого отхода; Отходы 1 класса опасности должны храниться раздельно!",
    "Срок хранения отходов в специально отведённых местах составляет не более 11 месяцев. Опасные отходы 2-го класса должны храниться в специальных помещениях, с надежной герметичностью в специальных тарах",
    "Отходы 3 класса опасности должны храниться раздельно в бумажных, полиэтиленовых или хлопчатобумажных тканевых мешках или в металлических контейнерах.",
    "Основное правило сбора отходов 4 класса опасности – необходимость проводить сбор мусора раздельно. Условия сбора определяются в зависимости от вида мусора. Допускается сбор в емкости, мешки, открытую тару, а также навалом, насыпью на отведенных для этого площадках.",
    "Деятельность, связанная с обращением отходов 5-го класса, лицензированию не подлежит. Неопасные отходы можно собирать, размещать, транспортировать без получения специального разрешения."
]


@bot.message_handler(commands=['fact'])
def start_message(message):
    bot.reply_to(message, random_fact = random.choice(facts))

# Запускаем бота
bot.polling()