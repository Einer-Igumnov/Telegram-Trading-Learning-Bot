class TextStyler:
    def __init__(self):
        pass

    def num_to_emoji(self, number: int):
        num = number
        emojis = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        result = ""
        while num != 0:
            result += emojis[num % 10][::-1]
            num //= 10
        result = result[::-1]
        return result

    def count_style(self, number: int):
        num = number % 100
        if num == 1:
            return "штука"
        elif num >= 2 and num <= 4:
            return "штуки"
        else:
            return "штук"
