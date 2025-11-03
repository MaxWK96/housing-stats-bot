#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Konto 5: Hidden Sweden (Placeholder)"""

import os
from datetime import datetime
from dotenv import load_dotenv
import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

async def main():
    print("\n🗺️ HIDDEN SWEDEN - Placeholder\n")
    
    bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    
    keyboard = [[InlineKeyboardButton("✅ OK", callback_data="approve_tiktok:placeholder")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await bot.send_message(
        chat_id=os.getenv("TELEGRAM_CHAT_ID"),
        text=f"🗺️ Hidden Sweden\n\n🎬 Placeholder för 60-sek video\n\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        reply_markup=reply_markup
    )
    
    print("✅ Skickat till Telegram!\n")

if __name__ == "__main__":
    asyncio.run(main())