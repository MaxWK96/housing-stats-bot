#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Posting Functions - Hanterar auto-posting till alla plattformar
"""

import os
import tweepy
from dotenv import load_dotenv

load_dotenv()


def post_to_twitter(image_path, caption):
    """
    Postar bild + text till Twitter/X
    """
    print(f"📤 Postar till Twitter...")
    
    try:
        # Kolla att API-nycklar finns
        if not all([
            os.getenv("TWITTER_API_KEY"),
            os.getenv("TWITTER_API_SECRET"),
            os.getenv("TWITTER_ACCESS_TOKEN"),
            os.getenv("TWITTER_ACCESS_SECRET")
        ]):
            print("⚠️ Twitter API-nycklar saknas i .env")
            return None
        
        # Twitter API v2
        client = tweepy.Client(
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
        )
        
        # API v1.1 för media upload
        auth = tweepy.OAuth1UserHandler(
            os.getenv("TWITTER_API_KEY"),
            os.getenv("TWITTER_API_SECRET"),
            os.getenv("TWITTER_ACCESS_TOKEN"),
            os.getenv("TWITTER_ACCESS_SECRET")
        )
        api = tweepy.API(auth)
        
        # Ladda upp media
        media = api.media_upload(filename=image_path)
        
        # Skapa tweet
        response = client.create_tweet(
            text=caption,
            media_ids=[media.media_id]
        )
        
        tweet_id = response.data['id']
        print(f"✅ Twitter: https://twitter.com/user/status/{tweet_id}")
        return tweet_id
        
    except Exception as e:
        print(f"❌ Twitter-fel: {e}")
        return None


def post_to_instagram(image_path, caption):
    """
    Postar till Instagram
    """
    print(f"📤 Instagram-posting...")
    print("⚠️ Instagram credentials saknas eller ej konfigurerat")
    return None


def post_to_linkedin(image_path, caption):
    """
    Postar till LinkedIn
    """
    print(f"📤 LinkedIn-posting...")
    print("⚠️ LinkedIn API ej konfigurerat")
    return None


def post_to_youtube(video_path, title, description):
    """
    Laddar upp till YouTube
    """
    print(f"📤 YouTube-uppladdning...")
    print("⚠️ YouTube API ej konfigurerat")
    return None


def post_to_tiktok(video_path, description):
    """
    Postar till TikTok
    """
    print(f"📤 TikTok-posting...")
    print("⚠️ TikTok API ej tillgängligt")
    return None