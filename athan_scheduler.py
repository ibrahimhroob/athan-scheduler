import pandas as pd
import datetime
import time
import os
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from playsound import playsound
import tabula
import camelot

# === CONFIG ===
PDF_DIR = "./calendar"   # Folder containing monthly prayer timetable PDFs
LAT = 53.2307   # Example: Lincoln, UK
LON = -0.5406
METHOD = 2      # Islamic Society of North America (ISNA) calc method
SCHOOL = 1     # 0 = Shafi'i, 1 = Hanafi
PRAYERS = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]

scheduler = BackgroundScheduler()

# --- PDF functions ---
def get_pdf_filename():
    today = datetime.date.today()
    month_str = today.strftime("%m-%B-%Y")  # e.g. "09-September-2025"
    return os.path.join(PDF_DIR, f"{month_str}.pdf")

def find_begins_columns(df):
    begins_cols = [c for c in df.columns if "Begins" in str(c)]
    if len(begins_cols) < 5:
        raise RuntimeError(f"Expected ≥5 'Begins' columns, found {len(begins_cols)}: {begins_cols}")
    return begins_cols[:5]

def parse_time_str(t, today):
    h, m = map(int, str(t).split(":"))
    return datetime.datetime.combine(today, datetime.time(hour=h, minute=m))

# --- API fallback ---
def load_prayer_times_from_api():
    today = datetime.date.today()
    url = f"http://api.aladhan.com/v1/timings/{today.day}-{today.month}-{today.year}"
    params = {"latitude": LAT, "longitude": LON, "method": METHOD, "school": SCHOOL}
    r = requests.get(url, params=params)
    data = r.json()

    timings = data["data"]["timings"]
    prayer_times = {}
    for prayer in PRAYERS:
        time_str = timings[prayer]
        h, m = map(int, time_str.split(":"))
        prayer_times[prayer] = datetime.datetime.combine(today, datetime.time(hour=h, minute=m))
    return prayer_times

# --- Athan ---
def play_athan(prayer):
    print(f"⏰ Time for {prayer}! Playing Athan...")
    try:
        if prayer.lower() == "fajr":
            playsound("fajr_athan.mp3")
        else:
            playsound("athan.mp3")
    except Exception as e:
        print(f"⚠️ Could not play athan sound: {e}")

# --- Scheduling ---
def schedule_todays_prayers():
    global scheduler
    scheduler.remove_all_jobs()
    today = datetime.date.today()

    prayer_times = load_prayer_times_from_api()

    for prayer, dt in prayer_times.items():
        if dt < datetime.datetime.now():
            continue  # skip past prayers
        scheduler.add_job(play_athan, "date", run_date=dt, args=[prayer])
        print(f"   Scheduled {prayer} at {dt.strftime('%H:%M')}")

def daily_refresh():
    print("🔄 Refreshing prayer times for new day...")
    schedule_todays_prayers()

# --- Main ---
scheduler.start()
schedule_todays_prayers()
scheduler.add_job(daily_refresh, "cron", hour=0, minute=0)

print("📅 Prayer scheduler running (PDF + API fallback).")
try:
    while True:
        time.sleep(60)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
