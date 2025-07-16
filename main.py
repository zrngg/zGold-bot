import requests
import time
from datetime import datetime
import pytz
import telebot

TELEGRAM_TOKEN = "8084011114:AAGqCKTt-3HibbZU6ttBAg1PK9Xb3ZJHw7I"
CHANNEL_USERNAME = "@gold_dataaaa"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
GOLD_SILVER_API = 'https://data-asg.goldprice.org/dbXRates/USD'
CRYPTO_API = "https://api.coingecko.com/api/v3/simple/price"
FOREX_API = "https://api.exchangerate.host/latest"

def fetch_gold_silver_prices():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(GOLD_SILVER_API, headers=headers)
        response.raise_for_status()
        data = response.json()
        items = data.get('items', [])
        if not items:
            return None
        return items[0]
    except Exception as e:
        print(f"Error fetching gold/silver prices: {e}")
        return None

def calculate_gold_prices(gold_ounce_price, silver_ounce_price):
    if not gold_ounce_price or not silver_ounce_price:
        return None

    gram_gold_price = gold_ounce_price / 31.1
    gram_silver_price = silver_ounce_price / 31.1

    prices = {
        'Msqal 21K 875': gram_gold_price * 0.875 * 5,
        'Msqal 18K 875': gram_gold_price * 0.75 * 5,
        'Lira Dubai 22K 7.2g': gram_gold_price * 0.916 * 7.2,
        '250g 24K 995': gram_gold_price * 0.995 * 250,
        '500g 24K 995': gram_gold_price * 0.995 * 500,
        '1Kg 24K 995': gram_gold_price * 0.995 * 1000,
        'Silver 1Kg': gram_silver_price * 1000,
    }
    return prices

def fetch_crypto_prices():
    try:
        params = {
            'ids': 'bitcoin,ethereum,ripple',
            'vs_currencies': 'usd'
        }
        response = requests.get(CRYPTO_API, params=params)
        response.raise_for_status()
        data = response.json()
        return {
            'BTC': data.get('bitcoin', {}).get('usd'),
            'ETH': data.get('ethereum', {}).get('usd'),
            'XRP': data.get('ripple', {}).get('usd'),
        }
    except Exception as e:
        print(f"Error fetching crypto prices: {e}")
        return None

def fetch_forex_rates():
    try:
        params = {
            'base': 'USD',
            'symbols': 'EUR,GBP'
        }
        response = requests.get(FOREX_API, params=params)
        response.raise_for_status()
        data = response.json()
        rates = data.get('rates', {})
        return {
            'USD_EUR': rates.get('EUR'),
            'USD_GBP': rates.get('GBP')
        }
    except Exception as e:
        print(f"Error fetching forex rates: {e}")
        return None

def send_prices():
    gs_data = fetch_gold_silver_prices()
    if not gs_data:
        bot.send_message(CHANNEL_USERNAME, "❌ Couldn't fetch gold and silver prices.")
        print("❌ Couldn't fetch gold and silver prices.")
        return

    gold_ounce_price = gs_data.get('xauPrice')
    silver_ounce_price = gs_data.get('xagPrice')
    if gold_ounce_price is None or silver_ounce_price is None:
        bot.send_message(CHANNEL_USERNAME, "❌ Gold or silver ounce price not available.")
        print("❌ Gold or silver ounce price not available.")
        return

    gold_prices = calculate_gold_prices(gold_ounce_price, silver_ounce_price)
    if not gold_prices:
        bot.send_message(CHANNEL_USERNAME, "❌ Error calculating gold prices.")
        print("❌ Error calculating gold prices.")
        return

    crypto_prices = fetch_crypto_prices()
    if not crypto_prices:
        bot.send_message(CHANNEL_USERNAME, "❌ Couldn't fetch crypto prices.")
        print("❌ Couldn't fetch crypto prices.")
        return

    forex_rates = fetch_forex_rates()
    if not forex_rates:
        bot.send_message(CHANNEL_USERNAME, "❌ Couldn't fetch forex rates.")
        print("❌ Couldn't fetch forex rates.")
        return

    # Time in GMT+3
    tz = pytz.timezone("Etc/GMT-3")
    now = datetime.now(tz).strftime("%d %B %Y | %H:%M")

    message = (
        f"{now} (GMT+3)\n"
        "——————————————————\n"
        f"Gold Ounce Price: ${gold_ounce_price:,.2f}\n"
        f"Silver Ounce Price: ${silver_ounce_price:,.2f}\n"
        f"Bitcoin Price: ${crypto_prices['BTC']:,.2f}\n"
        f"Ethereum Price: ${crypto_prices['ETH']:,.2f}\n"
        f"XRP Price: ${crypto_prices['XRP']:,.4f}\n"
        "——————————————————\n"
        "Gold:\n"
        f"Msqal 21K = ${gold_prices['Msqal 21K 875']:,.2f}\n"
        f"Msqal 18K = ${gold_prices['Msqal 18K 875']:,.2f}\n"
        f"Dubai Lira 7.2g = ${gold_prices['Lira Dubai 22K 7.2g']:,.2f}\n"
        f"250g 995 = ${gold_prices['250g 24K 995']:,.2f}\n"
        f"500g 995 = ${gold_prices['500g 24K 995']:,.2f}\n"
        f"1Kg 995 = ${gold_prices['1Kg 24K 995']:,.2f}\n"
        "——————————————————\n"
        "Silver:\n"
        f"1Kg Price: ${gold_prices['Silver 1Kg']:,.2f}\n"
        "——————————————————\n"
        "Forex:\n"
        f"USD EUR: {forex_rates['USD_EUR']:.4f}\n"
        f"USD GBP: {forex_rates['USD_GBP']:.4f}\n"
        "——————————————————"
    )

    bot.send_message(CHANNEL_USERNAME, message)
    print("✅ All prices sent!")

if __name__ == "__main__":
    while True:
        send_prices()
        time.sleep(1800)  # 30 minutes
