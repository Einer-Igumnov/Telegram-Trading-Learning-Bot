from account import Account
import telebot
from telebot import types
from text_styler import TextStyler
from api_keys import telegram_bot_key


class App:
    def __init__(self):
        self.accounts = {}
        self.bot = telebot.TeleBot(telegram_bot_key)
        self.styler = TextStyler()

        self.keyboard = types.InlineKeyboardMarkup()

        key_buy = types.InlineKeyboardButton(text='💳 Купить акции', callback_data='/buy')
        key_sell = types.InlineKeyboardButton(text='💸 Продать акции', callback_data='/sell')
        key_stats = types.InlineKeyboardButton(text='💼 Активы', callback_data='/stats')
        key_help = types.InlineKeyboardButton(text='📌 Помощь', callback_data='/help')

        self.keyboard.add(key_buy, key_sell)
        self.keyboard.add(key_stats, key_help)

    def buy(self, account: int, chat: int, message):
        def get_reply(msg):
            result = msg.text
            try:
                result = result.split()
                ticker = result[0]
                num = int(result[1])
                if num <= 0:
                    raise Exception("num not positive")
                self.bot.send_message(chat, self.accounts[account].buy(ticker, num), reply_markup=self.keyboard)
            except:
                self.bot.send_message(chat, "⛔️ Неверный формат ввода", reply_markup=self.keyboard)

        self.bot.send_message(chat, "💰 Введите тикер и количество акций:")
        self.bot.register_next_step_handler(message, get_reply)

    def sell(self, account: int, chat: int, message):
        def get_reply(msg):
            result = msg.text
            try:
                result = result.split()
                ticker = result[0]
                num = int(result[1])
                if num <= 0:
                    raise Exception("num not positive")
                self.bot.send_message(chat, self.accounts[account].sell(ticker, num), reply_markup=self.keyboard)
            except:
                self.bot.send_message(chat, "⛔️ Неверный формат ввода", reply_markup=self.keyboard)

        self.bot.send_message(chat, "💰 Введите тикер и количество акций:")
        self.bot.register_next_step_handler(message, get_reply)

    def stats(self, account: int, chat: int):
        message = "💰 Ваше состояние: " + str(round(self.accounts[account].value(), 2)) + "\n\n"

        message += "💼 Ваши активы: \n\n"
        message += "💵 Баланс: " + str(round(self.accounts[account].money, 2)) + "\n\n"

        index = 1
        for ticker in self.accounts[account].wallet:
            message += self.styler.num_to_emoji(index) + "  " + ticker + " - " + str(
                self.accounts[account].wallet[ticker]) + " " + self.styler.count_style(
                self.accounts[account].wallet[ticker]) + " \n"
            index += 1

        self.bot.send_message(chat, message, reply_markup=self.keyboard)

    def register(self, account: int, chat: int):
        self.accounts[account] = Account()
        self.accounts[account].id = account
        self.bot.send_message(chat, "✅ Вы успешно зарегистрировались в игре! ✅", reply_markup=self.keyboard)

    def help(self, chat: int):
        self.bot.send_message(chat,
                              "✅ Этот бот поможет научиться инвестировать.\n"
                              "💸 Изначально у каждого есть 10000 виртуальных долларов\n"
                              "📈 Можно покупать и продавать акции\n"
                              "🥇 Стань самым богатым!",
                              reply_markup=self.keyboard)

    def run(self):
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_worker(call):
            if call.data == "/buy":
                self.buy(call.from_user.id, call.message.chat.id, call.message)
            elif call.data == "/sell":
                self.sell(call.from_user.id, call.message.chat.id, call.message)
            elif call.data == "/stats":
                self.stats(call.from_user.id, call.message.chat.id)
            elif call.data == "/start":
                self.register(call.from_user.id, call.message.chat.id)
            elif call.data == "/help":
                self.help(call.message.chat.id)

        @self.bot.message_handler(content_types=['text'])
        def start(message):
            if message.text == "/buy":
                self.buy(message.from_user.id, message.chat.id, message)
            elif message.text == "/sell":
                self.sell(message.from_user.id, message.chat.id, message)
            elif message.text == "/stats":
                self.stats(message.from_user.id, message.chat.id)
            elif message.text == "/start":
                self.register(message.from_user.id, message.chat.id)
            elif message.text == "/help":
                self.help(message.chat.id)
            else:
                self.bot.send_message(message.chat.id, "⛔️ Такой команды не существует", reply_markup=self.keyboard)

        self.bot.polling(none_stop=True, interval=0)
