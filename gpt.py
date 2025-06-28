import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_analysis(title, impact, currency):
    prompt = f"""
یک خبر اقتصادی با مشخصات زیر وجود دارد:
عنوان: {title}  
اهمیت: {impact}  
کشور/واحد پول: {currency}
لطفاً یک تحلیل فاندامنتال مختصر و مفید برای این خبر بنویس که برای تریدرهای بازار فارکس مفید باشد:
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()
    except:
        return "⚠️ تحلیل با خطا مواجه شد."
