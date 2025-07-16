import requests
import telebot
import time
from datetime import datetime
import pytz

# Telegram bot token and channel
TOKEN = '8084011114:AAGqCKTt-3HibbZU6ttBAg1PK9Xb3ZJHw7I'
CHANNEL_USERNAME = "@gold_dataaaa"

bot = telebot.TeleBot(TOKEN)

# Get gold price
def get_gold_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=tether-gold&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        return float(data['tether-gold']['usd'])
    except:
        return 0

# Get silver price
def get_silver_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=silver&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        return float(data['silver']['usd'])
    except:
        return 0

# Main loop (every 30 minutes)
while True:
    gold_price = get_gold_price()
    silver_price = get_silver_price()

    if gold_price == 0:
        bot.send_message(CHANNEL_USERNAME, "❌ Couldn't fetch gold price.")
        time.sleep(60)
        continue

    # Current time (GMT+3)
    tz = pytz.timezone("Etc/GMT-3")
    now = datetime.now(tz).strftime("%d %B %Y | %H:%M")

    # Calculations
    oz_to_gram = 31.1
    g999 = gold_price / oz_to_gram
    g995 = g999 * 0.995
    m21 = g999 * 0.875 * 5
    m18 = g999 * 0.750 * 5
    lira_dubai = g999 * 0.916 * 7.2
    g250 = g999 * 0.995 * 250
    g500 = g999 * 0.995 * 500
    g1000 = g999 * 0.995 * 1000

    # Build the message
    message = (
        f"{now} (GMT+3)\n"
        f"——————————————————\n"
        f"Gold Ounce Price: ${gold_price:,.2f}\n"
        f"Silver Ounce Price: ${silver_price:,.2f}\n"
        f"——————————————————\n"
        f"Msqal 21K = ${m21:,.2f}\n"
        f"Msqal 18K = ${m18:,.2f}\n"
        f"Dubai Lira 7.2g = ${lira_dubai:,.2f}\n"
        f"——————————————————\n"
        f"250g 995 = ${g250:,.2f}\n"
        f"500g 995 = ${g500:,.2f}\n"
        f"1Kg 995 = ${g1000:,.2f}\n"
        f"—————————"
    )

    # Send to Telegram
    bot.send_message(CHANNEL_USERNAME, message)

    # Wait 30 minutes
    time.sleep(60)

