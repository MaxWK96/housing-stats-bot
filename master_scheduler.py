#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MASTER SCHEDULER"""

import schedule
import time
import subprocess
import sys
from datetime import datetime

PYTHON_EXE = sys.executable

def run_script(script_name):
    print(f"\n{'='*60}")
    print(f"🚀 Kör: {script_name}")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run([PYTHON_EXE, script_name], capture_output=True, text=True, timeout=600)
        print(result.stdout)
        if result.returncode == 0:
            print(f"✅ {script_name} lyckades")
        else:
            print(f"❌ {script_name} misslyckades")
    except Exception as e:
        print(f"❌ Fel: {e}")

# Schema
schedule.every().day.at("19:53").do(run_script, "konto1_housing_stats.py")
schedule.every().day.at("08:00").do(run_script, "konto2_freelance_finance.py")
schedule.every().day.at("18:00").do(run_script, "konto3_nordic_startups.py")
schedule.every().sunday.at("10:00").do(run_script, "konto4_remote_jobs.py")
schedule.every().monday.at("12:00").do(run_script, "konto5_hidden_sweden.py")

def main():
    print("\n⏰ MASTER SCHEDULER STARTAD")
    print("Tryck Ctrl+C för att stoppa\n")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()