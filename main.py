import requests
import telebot
import time
from datetime import datetime
import pytz

 # bot token 
TOKEN = '8084011114:AAGqCKTt-3HibbZU6ttBAg1PK9Xb3ZJHw7I'
CHANNEL_USERNAME = "@gold_dataaaa"

bot = telebot.TeleBot(TOKEN)

# gold price in USD
def get_gold_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=tether-gold&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        return float(data['tether-gold']['usd'])
    except:
        return 0

# silver price in USD
def get_silver_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=silver&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        return float(data['silver']['usd'])
    except:
        return 0


while True:
    gold_price = get_gold_price()
    silver_price = get_silver_price()

    if gold_price == 0:
        bot.send_message(CHANNEL_USERNAME, "❌ Couldn't fetch gold price.")
        time.sleep(1800)
        continue

    #  Time (GMT+3)
    tz = pytz.timezone("Etc/GMT-3")
    now = datetime.now(tz).strftime("%d %B %Y | %H:%M")

    # Hsabat
    oz_to_gram = 31.1
    gold_gram_999 = gold_price / oz_to_gram
    gold_gram_995 = gold_gram_999 * 0.995
    gold_misqal_21k = gold_gram_999 * 0.875 * 5
    gold_misqal_18k = gold_gram_999 * 0.750 * 5
    lira_dubai = gold_gram_999 * 0.916 * 7.2
    bar_250g = gold_gram_999 * 0.995 * 250
    bar_500g = gold_gram_999 * 0.995 * 500
    bar_1kg  = gold_gram_999 * 0.995 * 1000
    silver_1kg = silver_price / oz_to_gram * 1000 if silver_price > 0 else None

    #  Format message
    message = (
        f" {now} (GMT+3)\n"
        f"----------------------------------------\n\n"
        f"💰 Gold Price Oz: ${gold_price:,.2f}\n\n"
        f"1 Gram 24K 999   = ${gold_gram_999:,.2f}\n"
        f"1 Gram 24K 995   = ${gold_gram_995:,.2f}\n"
        f"1 Misqal 21K 875 = ${gold_misqal_21k:,.2f}\n"
        f"1 Misqal 18K 750 = ${gold_misqal_18k:,.2f}\n"
        f"Lira Dubai 22K (7.2g) = ${lira_dubai:,.2f}\n\n"
        f"250g 24K 995 = ${bar_250g:,.2f}\n"
        f"500g 24K 995 = ${bar_500g:,.2f}\n"
        f"1Kg  24K 995 = ${bar_1kg:,.2f}\n\n"
    )

    if silver_1kg:
        message += (
            f"------------------------------\n"
            f"🥈 1Kg Silver 999.9 = ${silver_1kg:,.2f}"
        )
    else:
        message += (
            f"------------------------------\n"
            f"🥈 Silver price unavailable"
        )

    
    bot.send_message(CHANNEL_USERNAME, message)

    # Rpeate time Wait 30 minutes
    time.sleep(1800)
