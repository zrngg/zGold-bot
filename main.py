import requests
from datetime import datetime
import pytz
import telebot
import time

# Credentials
TELEGRAM_TOKEN = "8084011114:AAGqCKTt-3HibbZU6ttBAg1PK9Xb3ZJHw7I"
CHANNEL_USERNAME = "@gold_dataaaa"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# APIs
GOLD_SILVER_API = 'https://data-asg.goldprice.org/dbXRates/USD'
CRYPTO_API = "https://api.coingecko.com/api/v3/simple/price"
FOREX_API = "https://open.er-api.com/v6/latest/USD"

def fetch_gold_silver_prices():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(GOLD_SILVER_API, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get('items', [None])[0]
    except Exception as e:
        print(f"Error fetching gold/silver prices: {e}")
        return None

def calculate_gold_prices(gold_oz, silver_oz):
    gold_g = gold_oz / 31.1
    silver_g = silver_oz / 31.1
    return {
        'Msqal 21K': gold_g * 0.875 * 5,
        'Msqal 18K': gold_g * 0.750 * 5,
        'Dubai Lira 7.2g': gold_g * 0.916 * 7.2,
        '250g 995': gold_g * 0.995 * 250,
        '500g 995': gold_g * 0.995 * 500,
        '1Kg 995': gold_g * 0.995 * 1000,
        'Silver 1Kg': silver_g * 1000,
    }

def fetch_crypto_prices():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        params = {'ids': 'bitcoin,ethereum,ripple', 'vs_currencies': 'usd'}
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
        response = requests.get(FOREX_API)
        response.raise_for_status()
        rates = response.json().get('rates', {})
        return {
            'EUR_to_USD': (1 / rates.get('EUR')) if rates.get('EUR') else None,
            'GBP_to_USD': (1 / rates.get('GBP')) if rates.get('GBP') else None
        }
    except Exception as e:
        print(f"Error fetching forex rates: {e}")
        return None

def generate_message():
    gold_data = fetch_gold_silver_prices()
    if not gold_data:
        return "❌ Couldn't fetch gold/silver prices."

    gold_oz = gold_data.get('xauPrice')
    silver_oz = gold_data.get('xagPrice')
    if not gold_oz or not silver_oz:
        return "❌ Missing ounce prices."

    prices = calculate_gold_prices(gold_oz, silver_oz)
    crypto = fetch_crypto_prices()
    forex = fetch_forex_rates()

    btc = f"${crypto['BTC']:,.2f}" if crypto and crypto['BTC'] else "N/A"
    eth = f"${crypto['ETH']:,.2f}" if crypto and crypto['ETH'] else "N/A"
    xrp = f"${crypto['XRP']:,.4f}" if crypto and crypto['XRP'] else "N/A"

    eur = f"{forex['EUR_to_USD'] * 100:.2f}" if forex and forex['EUR_to_USD'] else "N/A"
    gbp = f"{forex['GBP_to_USD'] * 100:.2f}" if forex and forex['GBP_to_USD'] else "N/A"

    tz = pytz.timezone("Etc/GMT-3")
    now = datetime.now(tz).strftime("%d %B %Y | %I:%M %p")

    return (
        f"{now} (GMT+3)\n"
        f"────────────────\n"
        f"Gold Ounce Price: ${gold_oz:,.2f}\n"
        f"Silver Ounce Price: ${silver_oz:,.2f}\n"
        f"Bitcoin Price: {btc}\n"
        f"Ethereum Price: {eth}\n"
        f"XRP Price: {xrp}\n"
        f"────────────────\n"
        f"Gold: 🟡\n"
        f"Msqal 21K = ${prices['Msqal 21K']:,.2f}\n"
        f"Msqal 18K = ${prices['Msqal 18K']:,.2f}\n"
        f"Dubai Lira 7.2g = ${prices['Dubai Lira 7.2g']:,.2f}\n"
        f"250g 995 = ${prices['250g 995']:,.2f}\n"
        f"500g 995 = ${prices['500g 995']:,.2f}\n"
        f"1Kg 995 = ${prices['1Kg 995']:,.2f}\n"
        f"────────────────\n"
        f"Silver: ⚪\n"
        f"1Kg Price: ${prices['Silver 1Kg']:,.2f}\n"
        f"────────────────\n"
        f"Forex: 💵\n"
        f"100 EUR in USD: {eur}\n"
        f"100 GBP in USD: {gbp}\n"
        f"────────────────\n"
        f"تێبینی ئەونرخانە نرخی بۆرسەن\n"
        f"بە سپۆنسەری پوری مچە\n"
        f"[Suli Borsa Whatsapp](https://chat.whatsapp.com/KFrg9RiQ7yg879MVTQGWlF)"
    )

def send_message():
    msg = generate_message()
    image_url = "https://i.imgur.com/NiKMpdF.jpeg"

    try:
        bot.send_photo(
            CHANNEL_USERNAME,
            image_url,
            caption=msg,
            parse_mode="Markdown"
        )
        print("✅ Message with image sent to Telegram.")
    except Exception as e:
        print(f"⚠️ Failed to send image: {e}")
        bot.send_message(CHANNEL_USERNAME, msg, parse_mode="Markdown")
        print("✅ Fallback: Message without image sent to Telegram.")

if __name__ == "__main__":
    while True:
        send_message()
        time.sleep(300)  # Refresh every 5 minutes
