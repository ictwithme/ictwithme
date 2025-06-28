import os
import openai
from dotenv import load_dotenv

load_dotenv()

# گرفتن کلید API از محیط امن
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_gpt(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "شما یک تحلیلگر اقتصادی حرفه‌ای هستید."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"❌ خطا در دریافت پاسخ از GPT: {str(e)}"
