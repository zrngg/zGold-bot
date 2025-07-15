import requests
import telebot
import time

# Your bot's token
TOKEN = '8084011114:AAGqCKTt-3HibbZU6ttBAg1PK9Xb3ZJHw7I'

# ✅ Replace with your CHANNEL username, NOT the bot username
CHANNEL_USERNAME = '@your_channel_username'  # e.g. '@goldupdateschannel'

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

# 🔁 Loop to send price every 30 minutes
while True:
    price = get_gold_price()
    if price != "error":
        bot.send_message(CHANNEL_USERNAME, f"💰 Gold Price: ${price} per oz")
    else:
        bot.send_message(CHANNEL_USERNAME, "❌ Couldn't fetch gold price")

    time.sleep(1800)  # Wait 30 minutes
