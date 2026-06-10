import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from google import genai

app = Flask(__name__)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

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
        full_msg = DGI_KNOWLEDGE + "\n\nStudent: " + user_message
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=full_msg
        )
        return response.text
    except Exception as e:
        print(f"Gemini error: {e}")
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
