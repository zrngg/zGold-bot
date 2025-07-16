import requests
import time
from datetime import datetime
import pytz
import telebot

# Telegram credentials
TELEGRAM_TOKEN = "8084011114:AAGqCKTt-3HibbZU6ttBAg1PK9Xb3ZJHw7I"
CHANNEL_USERNAME = "@gold_dataaaa"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

RATES_API_URL = 'https://data-asg.goldprice.org/dbXRates/USD'

def fetch_gold_prices():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    try:
        response = requests.get(RATES_API_URL, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        items = data.get('items', [])
        if not items:
            return None

        # Usually only one item for USD
        item = items[0]

        gold_ounce_price = item.get('xauPrice')  # gold ounce price

        msqal_21k = item.get('msq21K')
        msqal_18k = item.get('msq18K')
        dubai_lira_7_2g = item.get('dubaies')

        g995 = item.get('g995')  # price per gram of 995 purity gold

        return {
            'gold_ounce_price': gold_ounce_price,
            'msqal_21k': msqal_21k,
            'msqal_18k': msqal_18k,
            'dubai_lira_7_2g': dubai_lira_7_2g,
            'g995': g995,
        }

    except Exception as e:
        print(f"Error fetching gold prices: {e}")
        return None

def send_gold_prices():
    prices = fetch_gold_prices()
    if not prices:
        bot.send_message(CHANNEL_USERNAME, "❌ Couldn't fetch gold prices.")
        print("❌ Couldn't fetch gold prices.")
        return

    gold_ounce_price = prices['gold_ounce_price']
    msqal_21k = prices['msqal_21k']
    msqal_18k = prices['msqal_18k']
    dubai_lira_7_2g = prices['dubai_lira_7_2g']
    g995 = prices['g995']

    if None in [gold_ounce_price, msqal_21k, msqal_18k, dubai_lira_7_2g, g995]:
        bot.send_message(CHANNEL_USERNAME, "❌ Incomplete gold price data.")
        print("❌ Incomplete gold price data.")
        return

    # Calculate 250g, 500g, 1kg 995 purity prices
    price_250g = g995 * 250
    price_500g = g995 * 500
    price_1kg = g995 * 1000

    # Time in GMT+3
    tz = pytz.timezone("Etc/GMT-3")
    now = datetime.now(tz).strftime("%d %B %Y | %H:%M")

    message = (
        f"{now} (GMT+3)\n"
        "——————————————————\n"
        f"Gold Ounce Price: ${gold_ounce_price:,.2f}\n"
        "——————————————————\n"
        f"Msqal 21K = ${msqal_21k:,.2f}\n"
        f"Msqal 18K = ${msqal_18k:,.2f}\n"
        f"Dubai Lira 7.2g = ${dubai_lira_7_2g:,.2f}\n"
        "——————————————————\n"
        f"250g 995 = ${price_250g:,.2f}\n"
        f"500g 995 = ${price_500g:,.2f}\n"
        f"1Kg 995 = ${price_1kg:,.2f}\n"
        "—————————"
    )

    bot.send_message(CHANNEL_USERNAME, message)
    print("✅ Gold prices sent!")

if __name__ == "__main__":
    while True:
        send_gold_prices()
        time.sleep(1800)
