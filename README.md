# Athan Scheduler

A Python script that automatically plays the Athan (call to prayer) at the correct prayer times.  
It supports **local mosque PDF timetables** (preferred) and falls back to the **AlAdhan API** if the timetable is missing or unreadable.  
Fajr uses a dedicated Fajr Athan, while all other prayers use the standard Athan.

## ✨ Features
- Reads monthly prayer timetable PDFs (e.g. `09-September-2025.pdf`).
- Automatically schedules Athan for **Fajr, Dhuhr, Asr, Maghrib, Isha**.
- Refreshes daily at midnight for the new day.
- Falls back to **AlAdhan API** if PDF parsing fails.
- Plays separate audio for Fajr (`fajr_athan.mp3`) and other prayers (`athan.mp3`).

## 📦 Requirements
- Python 3.8+
- Java (for `tabula-py` PDF extraction)
- Libraries:
  ```bash
  pip install pandas tabula-py apscheduler playsound requests JPype1 camelot-py[cv] ghostscript
  ```

## 📂 Setup

1. Clone the repo:

   ```bash
   git clone https://github.com/your-username/athan-scheduler.git
   cd athan-scheduler
   ```
2. Add your monthly mosque timetables as PDF files in the format:

   ```
   09-September-2025.pdf
   10-October-2025.pdf
   ```
3. Place your audio files in the repo root:

   * `fajr_athan.mp3`
   * `athan.mp3`
4. Edit **latitude/longitude** in the script if you want API fallback to match your city.

## ▶️ Usage

Run the script:

```bash
python athan_scheduler.py
```

The script will:

* Load today's prayer times from the current month’s PDF.
* Schedule Athan playback.
* Refresh automatically at midnight for the next day.

## 🕌 Example

```
✅ Loaded prayer times from PDF
   Scheduled Fajr at 04:28
   Scheduled Dhuhr at 13:02
   Scheduled Asr at 17:29
   Scheduled Maghrib at 19:37
   Scheduled Isha at 21:16
📅 Prayer scheduler running (PDF + API fallback).
```

## 📜 License

MIT License
