import telebot as t

import cfg

bot = t.TeleBot(cfg.TG_BOT_TOKEN, parse_mode="MarkdownV2")


def send_message(text, chat_id=cfg.TG_CHAT_ID):
    try:
        return bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        print(e)


def send_test_fail_message(path, name, msg, chat_id=cfg.TG_CHAT_ID, env=cfg.ENV):
    try:
        text = f"""[{env}] TEST FAILED!
               path: {path}
               name: {name}
               message: {msg}"""
        return bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        print(e)


def send_photo(file_path, chat_id=cfg.TG_CHAT_ID):
    try:
        with open(file_path, "rb") as f:
            bot.send_photo(chat_id=chat_id, photo=f)
    except Exception as e:
        print(e)


def send_sticker(sticker_id, chat_id=cfg.TG_CHAT_ID):
    try:
        return bot.send_sticker(chat_id=chat_id, sticker=sticker_id)
    except Exception as e:
        print(e)
