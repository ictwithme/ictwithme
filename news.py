import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz

from gpt import ask_gpt
from config import NEW_YORK_TIMEZONE

def check_forexfactory():
    # دریافت اخبار از فارکس فکتوری
    url = "https://www.forexfactory.com/calendar"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # استخراج داده‌ها (نیاز به تنظیم دقیق‌تر بر اساس ساختار سایت)
    now = datetime.now(pytz.timezone(NEW_YORK_TIMEZONE))
    news_list = []

    for row in soup.select(".calendar__row"):
        time_tag = row.select_one(".calendar__time")
        title_tag = row.select_one(".calendar__event-title")
        impact_tag = row.select_one(".impact")

        if time_tag and title_tag:
            news_time_str = time_tag.get_text(strip=True)
            if news_time_str.lower() in ["all day", "" or None]:
                continue

            try:
                news_time = datetime.strptime(news_time_str, "%I:%M%p").replace(
                    year=now.year, month=now.month, day=now.day
                )
                news_time = pytz.timezone(NEW_YORK_TIMEZONE).localize(news_time)
            except ValueError:
                continue

            # ارسال ده دقیقه قبل از خبر
            if timedelta(minutes=0) < (news_time - now) <= timedelta(minutes=10):
                title = title_tag.get_text(strip=True)
                impact = impact_tag.get("class", [])[-1] if impact_tag else ""

                # دریافت تحلیل از GPT
                prompt = f"خبر اقتصادی: {title}\nاین خبر چه تاثیری بر بازار فارکس دارد؟"
                analysis = ask_gpt(prompt)

                news_list.append((title, impact, analysis))

    return news_list

def check_bloomberg():
    url = "https://www.bloomberg.com/markets/economics"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.select("article")[:5]
    results = []
    for article in articles:
        title_tag = article.find("a")
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = "https://www.bloomberg.com" + title_tag.get("href", "")
            prompt = f"لینک: {link}\nخبر اقتصادی: {title}\nاین خبر چه تاثیری بر بازار فارکس دارد؟"
            analysis = ask_gpt(prompt)
            results.append((title, link, analysis))
    return results

def check_investing():
    url = "https://www.investing.com/news/economy"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.select(".textDiv")[:5]
    results = []
    for article in articles:
        title_tag = article.find("a")
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = "https://www.investing.com" + title_tag.get("href", "")
            prompt = f"لینک: {link}\nخبر اقتصادی: {title}\nاین خبر چه تاثیری بر بازار فارکس دارد؟"
            analysis = ask_gpt(prompt)
            results.append((title, link, analysis))
    return results
