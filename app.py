import os
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

DGI_KNOWLEDGE = """You are the official AI assistant for Dronacharya Group of Institutions (DGI), Greater Noida. Answer in Hindi or English based on user's language. Keep replies short and WhatsApp-friendly.

ABOUT: Location: Knowledge Park-III, Greater Noida UP. Est: 2006. AKTU affiliated, AICTE approved, NAAC & NBA Accredited. Web: gnindia.dronacharya.info. Phone: 0120-2322022. Helpline: +91-9910380115

COURSES: B.Tech: CSE, CSIT, IT, CSE-AIML, ECE, ECS, EEE, ME. PG: MBA

FEES: B.Tech: Rs 2.43L to 3.75L total

ADMISSIONS: JEE Main/UPTAC. Apply: admission.dronacharya.info/gn/applyonline.aspx

PLACEMENTS: Highest 45 LPA. Recruiters: TCS, Deloitte, HSBC, BYJU'S

TRANSPORT: 17+ bus routes - Delhi, Noida, Greater Noida, Ghaziabad, Faridabad. PDF: gnindia.dronacharya.info/Downloads/BusSchedule/BUS-ROUTE-JANUARY-TO-JUNE-2026.pdf

CAMPUS: Library, Canteen, Seminar Hall, Auditorium, R&D Lab, Clubs, IEEE, CSI"""

def get_ai_reply(user_message):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://dgi-bot.railway.app",
                "X-Title": "DGI College Bot"
            },
            json={
                "model": "deepseek/deepseek-chat:free",
                "messages": [
                    {"role": "system", "content": DGI_KNOWLEDGE},
                    {"role": "user", "content": user_message}
                ]
            },
            timeout=30
        )
        data = response.json()
        print("Response:", data)
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        elif "error" in data:
            print("API Error:", data["error"])
            return "Sorry, technical issue! Visit: gnindia.dronacharya.info"
        else:
            return "Sorry, technical issue! Visit: gnindia.dronacharya.info"
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, technical issue! Visit: gnindia.dronacharya.info or call 0120-2322022"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "unknown")
    print(f"Message from {sender}: {incoming_msg}")
    reply = get_ai_reply(incoming_msg)
    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)

@app.route("/", methods=["GET"])
def home():
    return "DGI WhatsApp AI Bot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
