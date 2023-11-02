from stock_api import get_price


class Account:
    def __init__(self):
        self.money = 10000
        self.wallet = {}
        self.id = 0

    def num_of_ticker(self, ticker: str):
        if self.wallet.get(ticker) is None:
            return 0
        else:
            return self.wallet.get(ticker)

    def buy(self, ticker: str, num: int):
        ticker = ticker.upper()
        if get_price(ticker) == 0:
            return "❓ Такого тикера не существует"
        if num * get_price(ticker) > self.money:
            return "⛔️ Не хватает денег"
        else:
            self.money -= num * get_price(ticker)
            self.wallet[ticker] = self.num_of_ticker(ticker) + num
            return "✅ Успешно куплены акции"

    def sell(self, ticker: str, num: int):
        ticker = ticker.upper()
        if get_price(ticker) == 0:
            return "❓ Такого тикера не сушествует"
        if num > self.num_of_ticker(ticker):
            return "⛔️ У вас нет столько акций"
        else:
            self.money += num * get_price(ticker)
            self.wallet[ticker] = self.num_of_ticker(ticker) - num
            return "✅ Успешно проданы акции"

    def value(self):
        result = self.money
        for ticker in self.wallet:
            result += self.wallet[ticker] * get_price(ticker)

        return result
