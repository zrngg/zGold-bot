import requests
import telebot
import time

TOKEN = '8084011114:AAGqCKTt-3HibbZU6ttBAg1PK9Xb3ZJHw7I'
CHAT_ID = '-1234567890'  # Change to your group chat ID (with minus)

bot = telebot.TeleBot(TOKEN)

def get_gold_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=tether-gold&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        gold_price = data['tether-gold']['usd']
        return gold_price
    except:
        return "error"

while True:
    price = get_gold_price()
    if price != "error":
        bot.send_message(CHAT_ID, f"💰 Gold Price: ${price} per oz")
    else:
        bot.send_message(CHAT_ID, "❌ Couldn't fetch gold price")

    time.sleep(1800)  # 30 mins
