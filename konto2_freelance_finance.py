#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Konto 2: Freelance Finance (Placeholder)"""

import os
import random
from datetime import datetime
from dotenv import load_dotenv
import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

TOPICS = [
    "ROT-avdrag för frilansare",
    "Moms och F-skatt",
    "Pension för frilansare",
]

async def main():
    print("\n💰 FREELANCE FINANCE - Placeholder\n")
    
    topic = random.choice(TOPICS)
    
    bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    
    keyboard = [[InlineKeyboardButton("✅ OK", callback_data="approve_tiktok:placeholder")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await bot.send_message(
        chat_id=os.getenv("TELEGRAM_CHAT_ID"),
        text=f"💰 Freelance Finance\n\n📋 {topic}\n\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        reply_markup=reply_markup
    )
    
    print("✅ Skickat till Telegram!\n")

if __name__ == "__main__":
    asyncio.run(main())