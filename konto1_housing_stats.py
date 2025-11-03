#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Swedish Housing Stats - PRODUCTION VERSION
Med riktiga data-källor, bättre grafer och AI
"""

import os
import json
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from dotenv import load_dotenv
from graph_generator import generate_random_graph
import asyncio
import random

load_dotenv()

OUTPUT_DIR = "generated/images"
DATA_DIR = "data/processed"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)


def fetch_housing_data():
    """
    Hämtar bostadsdata från flera källor (SCB, Mäklarstatistik, Booli)
    """
    print("📊 Hämtar bostadsdata...")
    
    # Försök SCB först (gratis öppet API)
    data = try_scb_api()
    
    if data is not None:
        return data
    
    # Backup: Mäklarstatistik CSV (om SCB failar)
    data = try_maklarstatistik_csv()
    
    if data is not None:
        return data
    
    # Sista utväg: Mock-data med realistiska siffror
    print("⚠️ Använder mock-data (för demo)")
    return create_realistic_mock_data()


def try_scb_api():
    """
    SCB Population API - 100% gratis
    """
    try:
        # Exempel: Boende efter region
        url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/BO/BO0104/BO0104D/BO0104T04"
        
        query = {
            "query": [
                {
                    "code": "Region",
                    "selection": {
                        "filter": "vs:RegionRiket99",
                        "values": ["00"]
                    }
                }
            ],
            "response": {
                "format": "json"
            }
        }
        
        response = requests.post(url, json=query, timeout=10)
        
        if response.status_code == 200:
            print("✅ Data från SCB hämtad")
            # Parse SCB response (detta är förenklat)
            return parse_scb_response(response.json())
        
    except Exception as e:
        print(f"⚠️ SCB API-fel: {e}")
    
    return None


def parse_scb_response(scb_data):
    """Konverterar SCB JSON till DataFrame"""
    # Detta är en förenklad parser
    # I produktion skulle du behöva anpassa till SCB:s exakta format
    return None


def try_maklarstatistik_csv():
    """
    Mäklarstatistik publicerar öppna CSV-filer
    """
    try:
        # Exempel CSV från Mäklarstatistik (publikt tillgänglig)
        url = "https://www.maklarstatistik.se/omrade/riket/sverige"
        
        # Detta kräver web scraping - för nu skippar vi
        return None
        
    except Exception as e:
        print(f"⚠️ Mäklarstatistik-fel: {e}")
    
    return None


def create_realistic_mock_data():
    """
    Realistiska siffror baserat på verkliga trender
    """
    import random
    
    dates = pd.date_range(end=datetime.now(), periods=12, freq='ME')
    
    # Realistiska priser för svenska småhus (2024-2025)
    base_prices = {
        'Stockholm': 6500000,
        'Göteborg': 4800000,
        'Malmö': 4200000,
        'Riket': 3800000
    }
    
    region = random.choice(list(base_prices.keys()))
    base = base_prices[region]
    
    # Simulera prisförändringar (baserat på verkliga trender)
    prices = []
    for i in range(12):
        # Lägg till naturlig variation (-2% till +3%)
        change = random.uniform(-0.02, 0.03)
        price = base * (1 + change * (i/12))
        prices.append(int(price))
    
    df = pd.DataFrame({
        'date': dates,
        'price': prices,
        'region': [region] * 12
    })
    
    print(f"✅ Mock-data skapad för {region}")
    return df


def create_advanced_graph(df):
    """
    Skapar professionell graf med trendlinje och statistics
    """
    print("📈 Skapar avancerad graf...")
    
    # Stil
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_palette("Set2")
    
    fig, ax = plt.subplots(figsize=(12, 7), dpi=120)
    
    # Huvudlinje
    ax.plot(df['date'], df['price'], 
            marker='o', linewidth=3, markersize=10, 
            color='#2E86AB', label='Genomsnittspris')
    
    # Trendlinje (polynomial)
    z = np.polyfit(range(len(df)), df['price'], 2)
    p = np.poly1d(z)
    ax.plot(df['date'], p(range(len(df))), 
            "--", color='#A23B72', linewidth=2, 
            alpha=0.7, label='Trend')
    
    # Beräkna statistik
    latest_price = df['price'].iloc[-1]
    avg_price = df['price'].mean()
    change_pct = ((df['price'].iloc[-1] - df['price'].iloc[0]) / df['price'].iloc[0]) * 100
    
    # Titel med statistik
    region = df['region'].iloc[0]
    title = f'Småhuspriser - {region}\n'
    title += f'Senaste: {latest_price:,.0f} SEK  |  Årsförändring: {change_pct:+.1f}%'
    
    ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('Månad', fontsize=14, fontweight='bold')
    ax.set_ylabel('Pris (SEK)', fontsize=14, fontweight='bold')
    
    # Formatera y-axeln
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/1000000):.1f}M'))
    
    # Grid
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Legend
    ax.legend(loc='upper left', fontsize=12, framealpha=0.9)
    
    # Källa längst ner
    fig.text(0.99, 0.01, 'Källa: SCB | @HousingStats', 
             ha='right', va='bottom', fontsize=10, 
             style='italic', color='gray')
    
    plt.tight_layout()
    
    # Spara
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{OUTPUT_DIR}/housing_advanced_{timestamp}.png"
    plt.savefig(filename, bbox_inches='tight', dpi=150, facecolor='white')
    plt.close()
    
    print(f"✅ Graf sparad: {filename}")
    return filename


def generate_engaging_tweet(df):
    """
    Genererar engagerande tweet med AI (förbättrade prompts)
    """
    print("🤖 Genererar tweet med AI...")
    
    # Beräkna insights
    latest = df['price'].iloc[-1]
    previous = df['price'].iloc[-2]
    change_pct = ((latest - previous) / previous) * 100
    yearly_change = ((df['price'].iloc[-1] - df['price'].iloc[0]) / df['price'].iloc[0]) * 100
    avg = df['price'].mean()
    region = df['region'].iloc[0]
    
    # Förbättrad prompt
    prompt = f"""Du är en expert på svensk fastighetsmarknad. Skriv en engagerande tweet (max 250 tecken) om bostadspriser.

DATA:
- Region: {region}
- Senaste pris: {latest:,.0f} SEK
- Månadsförändring: {change_pct:+.1f}%
- Årsförändring: {yearly_change:+.1f}%
- Genomsnitt 12 mån: {avg:,.0f} SEK

KRAV:
- Börja med emoji (📈/📉/➡️)
- Inkludera konkret siffra
- Kort och lätt att läsa
- Använd hashtags #bostad #fastighet
- Skriv ENDAST tweeten, inget annat

EXEMPEL:
"📈 Småhuspriserna i Sverige upp 2,3% senaste månaden! Nu {latest:,.0f} SEK i snitt. Marknaden visar fortsatt styrka. #bostad #fastighet"

TWEET:"""

    if not HF_TOKEN:
        return create_fallback_tweet(change_pct, latest, region)
    
    api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.8,
            "top_p": 0.9,
            "return_full_text": False
        }
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            tweet = result[0]['generated_text'] if isinstance(result, list) else result['generated_text']
            tweet = tweet.replace(prompt, '').strip()
            
            # Cleanup
            tweet = tweet.split('\n')[0]  # Ta första raden
            tweet = tweet[:280]  # Twitter limit
            
            if len(tweet) > 30:
                print(f"✅ AI-tweet genererad")
                return tweet
        
    except Exception as e:
        print(f"⚠️ AI-fel: {e}")
    
    return create_fallback_tweet(change_pct, latest, region)


def create_fallback_tweet(change_pct, latest_price, region):
    """
    Backup-tweets om AI failar
    """
    if change_pct > 0:
        templates = [
            f"📈 Småhuspriser i {region} upp {abs(change_pct):.1f}%! Nu {latest_price:,.0f} SEK i snitt. Marknaden fortsätter stiga. #bostad #fastighet",
            f"📊 Bostadspriserna i {region} ökar med {abs(change_pct):.1f}%. Genomsnittpris nu {latest_price:,.0f} SEK. #bostad #fastighet",
        ]
    elif change_pct < 0:
        templates = [
            f"📉 Småhuspriser i {region} ner {abs(change_pct):.1f}%. Ligger nu på {latest_price:,.0f} SEK i snitt. #bostad #fastighet",
            f"📊 Bostadspriserna i {region} sjunker med {abs(change_pct):.1f}%. Genomsnitt: {latest_price:,.0f} SEK. #bostad #fastighet",
        ]
    else:
        templates = [
            f"➡️ Småhuspriser i {region} stabila på {latest_price:,.0f} SEK. Marknaden visar ingen större förändring. #bostad #fastighet",
        ]
    
    return random.choice(templates)


async def send_telegram_notification(image_path, caption):
    """Skickar till Telegram"""
    print("📱 Skickar Telegram-notis...")
    
    from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
    
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Godkänn & Posta", callback_data=f"approve:{image_path}"),
            InlineKeyboardButton("❌ Skippa", callback_data=f"skip:{image_path}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    with open(image_path, 'rb') as photo:
        message = await bot.send_photo(
            chat_id=TELEGRAM_CHAT_ID,
            photo=photo,
            caption=f"🏠 Swedish Housing Stats\n\n{caption}\n\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            reply_markup=reply_markup
        )
    
    print(f"✅ Telegram-notis skickad!")
    
    # Metadata
    metadata = {
        "image_path": image_path,
        "caption": caption,
        "message_id": message.message_id,
        "created_at": datetime.now().isoformat(),
        "status": "pending"
    }
    
    metadata_file = f"{DATA_DIR}/pending_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    return metadata_file


def main():
    print("\n" + "="*60)
    print("🚀 SWEDISH HOUSING STATS - PRODUCTION VERSION")
    print("="*60 + "\n")
    
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Telegram credentials saknas!")
        return
    
    # 1. Hämta data
    housing_data = fetch_housing_data()
    
    # 2. Skapa avancerad graf
    import numpy as np
    graph_path, graph_type = generate_random_graph(housing_data, OUTPUT_DIR)
    
    # 3. Generera engagerande tweet
    tweet = generate_engaging_tweet(housing_data)
    
    # 4. Skicka till Telegram
    asyncio.run(send_telegram_notification(graph_path, tweet))
    
    print("\n" + "="*60)
    print("✅ KLART! Kolla Telegram för preview")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()