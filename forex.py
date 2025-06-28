import requests
from bs4 import BeautifulSoup
import datetime
import pytz

TIMEZONE = pytz.timezone("America/New_York")

def get_forex_news():
    url = "https://www.forexfactory.com/calendar"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    events = []

    rows = soup.select("tr.calendar__row")
    now = datetime.datetime.now(TIMEZONE)

    for row in rows:
        try:
            time_str = row.select_one("td.time").get_text(strip=True)
            if time_str.lower() in ["all day", ""]:
                continue

            title = row.select_one("td.event").get_text(strip=True)
            impact_icon = row.select_one("td.impact span.icon")
            impact = impact_icon["title"] if impact_icon else "None"

            currency = row.select_one("td.currency").get_text(strip=True)

            # زمان تبدیل‌شده به datetime واقعی
            hour, minute = map(int, time_str.split(":"))
            am_pm = "AM" if "am" in time_str.lower() else "PM"
            event_time = now.replace(hour=hour % 12 + (12 if am_pm == "PM" else 0), minute=minute, second=0, microsecond=0)

            if event_time < now:
                continue

            events.append({
                "title": title,
                "impact": impact,
                "currency": currency,
                "time": event_time,
                "sent": False  # برای کنترل اینکه آیا ارسال شده یا نه
            })

        except Exception as e:
            continue

    return events
