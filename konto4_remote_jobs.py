#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Konto 4: Remote Jobs (Placeholder)"""

import os
from datetime import datetime
from dotenv import load_dotenv
import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

async def main():
    print("\n💼 REMOTE JOBS - Placeholder\n")
    
    bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    
    keyboard = [[InlineKeyboardButton("✅ OK", callback_data="approve_yt:placeholder")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await bot.send_message(
        chat_id=os.getenv("TELEGRAM_CHAT_ID"),
        text=f"💼 Remote Jobs for Swedes\n\n📹 Placeholder för video-kompilation\n\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        reply_markup=reply_markup
    )
    
    print("✅ Skickat till Telegram!\n")

if __name__ == "__main__":
    asyncio.run(main())