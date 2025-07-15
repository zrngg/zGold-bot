import requests
import telebot
import time

# ✅ Your bot token
TOKEN = '8084011114:AAGqCKTt-3HibbZU6ttBAg1PK9Xb3ZJHw7I'

# ✅ Public channel username in quotes
CHANNEL_USERNAME = "@gold_dataaaa"

bot = telebot.TeleBot(TOKEN)

def get_gold_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=tether-gold&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        gold_price = data['tether-gold']['usd']
        return gold_price
    except Exception as e:
        print("Error getting gold price:", e)
        return "error"

while True:
    price = get_gold_price()
    if price != "error":
        message = f"💰 Gold Price Update:\n\n1 oz = ${price} USD"
        bot.send_message(CHANNEL_USERNAME, message)
    else:
        bot.send_message(CHANNEL_USERNAME, "❌ Couldn't fetch gold price.")

    time.sleep(120)  # Wait 30 minutes
