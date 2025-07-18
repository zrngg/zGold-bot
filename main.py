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
    now = datetime.now(tz).strftime("%d %B %Y | %I:%M %p")  # 12-hour format

   return (
        f"{now} (GMT+3)\n"
        "────────────────\n"
        f"Gold Ounce Price: ${gold_oz:,.2f}\n"
        f"Silver Ounce Price: ${silver_oz:,.2f}\n"
        f"Bitcoin Price: {btc}\n"
        f"Ethereum Price: {eth}\n"
        f"XRP Price: {xrp}\n"
        "────────────────\n"
        "Gold: 🟡\n"
        f"Msqal 21K = ${prices['Msqal 21K']:,.2f}\n"
        f"Msqal 18K = ${prices['Msqal 18K']:,.2f}\n"
        f"Dubai Lira 7.2g = ${prices['Dubai Lira 7.2g']:,.2f}\n"
        f"250g 995 = ${prices['250g 995']:,.2f}\n"
        f"500g 995 = ${prices['500g 995']:,.2f}\n"
        f"1Kg 995 = ${prices['1Kg 995']:,.2f}\n"
        "────────────────\n"
        "Silver: ⚪\n"
        f"1Kg Price: ${prices['Silver 1Kg']:,.2f}\n"
        "────────────────\n"
        "Forex: 💵\n"
        f"100 EUR in USD: {eur}\n"
        f"100 GBP in USD: {gbp}\n"
        "────────────────\n"
        "تێبینی ئەونرخانە نرخی بۆرسەن\n"
        "[Whatsapp Group](https://chat.whatsapp.com/KFrg9RiQ7yg879MVTQGWlF)"
    )

def send_message():
    msg = generate_message()
    bot.send_message(CHANNEL_USERNAME, msg, parse_mode='Markdown', disable_web_page_preview=True)
    print("✅ Message sent to Telegram.")
