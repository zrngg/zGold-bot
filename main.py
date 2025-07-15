import requests
import telebot
import time

# ✅ Your bot token
TOKEN = '8084011114:AAGqCKTt-3HibbZU6ttBAg1PK9Xb3ZJHw7I'

# ✅ Public channel username
CHANNEL_USERNAME = '@gold_dataaaa'

# ✅ Create the bot instance
bot = telebot.TeleBot(TOKEN)

# ✅ Function to get gold price from CoinGecko API
def get_gold_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=tether-gold&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        gold_price = data['tether-gold']['usd']
        return gold_price
    except Exception as e:
        print("Error getting price:", e)
        return "error"

# ✅ Main loop - send gold price every 30 minutes
while True:
    price = get_gold_price()
    if price != "error":
        message = f"💰 Gold Price Update:\n\n1 oz = ${price} USD"
        bot.send_message(@gold_dataaaa, message)
    else:
        bot.send_message(@gold_dataaaa, "❌ Couldn't fetch gold price.")

    time.sleep(1800)  # Wait 1800 seconds (30 minutes)
