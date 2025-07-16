import requests
from datetime import datetime
import pytz
import telebot
import time

# Your credentials
TELEGRAM_TOKEN = "8084011114:AAGqCKTt-3HibbZU6ttBAg1PK9Xb3ZJHw7I"
CHANNEL_USERNAME = "@gold_dataaaa"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

GOLD_SILVER_API = 'https://data-asg.goldprice.org/dbXRates/USD'
CRYPTO_API = "https://api.coingecko.com/api/v3/simple/price"

def fetch_gold_silver_prices():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
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
        headers = {'User-Agent': 'Mozilla/5.0'}
        params = {
            'ids': 'bitcoin,ethereum,ripple',
            'vs_currencies': 'usd'
        }
        response = requests.get(CRYPTO_API, params=params, headers=headers)
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
        url = "https://open.er-api.com/v6/latest/USD"
        response = requests.get(url)
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

def generate_message():
    gs_data = fetch_gold_silver_prices()
    if not gs_data:
        return "❌ Couldn't fetch gold and silver prices."

    gold_ounce_price = gs_data.get('xauPrice')
    silver_ounce_price = gs_data.get('xagPrice')
    if gold_ounce_price is None or silver_ounce_price is None:
        return "❌ Gold or silver ounce price not available."

    gold_prices = calculate_gold_prices(gold_ounce_price, silver_ounce_price)
    if not gold_prices:
        return "❌ Error calculating gold prices."

    crypto_prices = fetch_crypto_prices()
    if not crypto_prices:
        return "❌ Couldn't fetch crypto prices."

    forex_rates = fetch_forex_rates()
    if not forex_rates:
        return "❌ Couldn't fetch forex rates."

    usd_eur = forex_rates['USD_EUR']
    usd_gbp = forex_rates['USD_GBP']

    eur_usd = (1 / usd_eur) if usd_eur else None
    gbp_usd = (1 / usd_gbp) if usd_gbp else None

    eur_usd_str = f"{eur_usd * 100:.2f}" if eur_usd is not None else "N/A"
    gbp_usd_str = f"{gbp_usd * 100:.2f}" if gbp_usd is not None else "N/A"

    tz = pytz.timezone("Etc/GMT-3")
    now = datetime.now(tz).strftime("%d %B %Y | %H:%M")

    message = (
        f"{now} (GMT+3)\n"
        "——————————————————\n"
        f"Gold Ounce Price: ${gold_ounce_price:,.2f}\n"
        f"Silver Ounce Price: ${silver_ounce_price:,.2f}\n"
        f"Bitcoin Price: ${crypto_prices['BTC'] if crypto_prices['BTC'] is not None else 'N/A':,.2f}\n"
        f"Ethereum Price: ${crypto_prices['ETH'] if crypto_prices['ETH'] is not None else 'N/A':,.2f}\n"
        f"XRP Price: ${crypto_prices['XRP'] if crypto_prices['XRP'] is not None else 'N/A':,.4f}\n"
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
        f"100 EUR in USD: {eur_usd_str}\n"
        f"100 GBP in USD: {gbp_usd_str}\n"
        "——————————————————"
    )
    return message

def send_message():
    message = generate_message()
    bot.send_message(CHANNEL_USERNAME, message)
    print("Message sent to channel!")

if __name__ == "__main__":
    while True:
        send_message()
        time.sleep(1800)  # wait 30 minutes before next update
