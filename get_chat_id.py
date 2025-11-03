import os
from dotenv import load_dotenv
import requests

load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN")

if not token:
    print("❌ TELEGRAM_BOT_TOKEN saknas i .env!")
else:
    print(f"📱 Använder token: {token[:10]}...")
    
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get('ok') and data.get('result'):
            # Hitta senaste meddelandet
            latest_update = data['result'][-1]
            chat_id = latest_update['message']['chat']['id']
            
            print(f"\n✅ DITT CHAT ID: {chat_id}")
            print(f"\nLägg in detta i .env:")
            print(f"TELEGRAM_CHAT_ID={chat_id}")
        else:
            print("\n⚠️ Inga meddelanden hittades!")
            print("📝 Skicka ett meddelande till din bot i Telegram först")
            print(f"🔍 Bot-användarnamn: Sök efter din bot i Telegram")
            
    except Exception as e:
        print(f"❌ Fel: {e}")