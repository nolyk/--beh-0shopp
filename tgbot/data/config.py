from tgbot.data.texts.ru import Language as RU

from tgbot.keyboards import users, admins


class BotConfig:
    BOT_TOKEN = "8529432318:AAGoXBZnti53wxlZJ7AomGoOXSC1YvOlAXM" # токен бота
    ADMINS = [5086997249] # 123456789, 9876554321...
    LOGS_CHANNEL = -1003831210272 # -100123456789, 0 если не хотим ставить
    BOT_VERSION = "1.0"
    CURRENCIES = {
        "uzs": {
            'txt': 'uzs',
            "text": 'UZS',
            'sign': 'сўм'
        }
    }
    LANGUAGES = [
        {
            "language": "ru",
            "name": "🇷🇺 Русский",
        },
    ]
    ######
    ######
    ######


class BotTexts:
    class Ru:
        ADMIN_TEXTS = RU.AdminTexts()
        TEXTS = RU.Texts()
        BUTTONS = RU.Buttons()


class BotButtons:
    USERS_REPLY = users.ReplyButtons()
    USERS_INLINE = users.InlineButtons()
    ADMIN_INLINE = admins.InlineButtons()


class BotImages:
    # Прямые ссылки на фото
    START_PHOTO = "https://i.postimg.cc/L5cdkXjj/image.png"
    TOPUP_BALANCE_PHOTO = "https://info.exmo.me/wp-content/uploads/2021/10/banner_uzs-1032x540.png"
    SUPPORT_PHOTO = "https://www.castcom.ru/netcat_files/114/157/castcom_support.png"
    BUY_PHOTO = "https://www.bobrlife.by/wp-content/uploads/2022/04/tovary-v-krizis_0.jpg"
    FAQ_PHOTO = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTX817aptpJsuxUeCzjOizmQyc2wwoPdR9CrrZ-a7KQvEdKNAFfnCp6-wwkZUSb5XAIP_U&usqp=CAU"
    CONTEST_PHOTO = "https://i.imgur.com/zlblPgk.jpg"


def main_db():
    from tgbot.utils.db import DataBase
    return DataBase()

DB = main_db()