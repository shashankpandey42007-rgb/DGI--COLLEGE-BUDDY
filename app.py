import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

DGI_KNOWLEDGE = """
You are the official AI assistant for Dronacharya Group of Institutions (DGI), Greater Noida.
Answer every question in a friendly, helpful, concise manner.
If you don't know something specific, direct the student to: gnindia.dronacharya.info
Always respond in the same language the user writes in (Hindi or English).
Keep replies short and WhatsApp-friendly (use emojis naturally).

ABOUT DGI:
- Full Name: Dronacharya Group of Institutions (DGI)
- Location: #27, APJ Abdul Kalam Road, Knowledge Park-III, Greater Noida, UP - 201306
- Established: 2006
- Affiliation: AKTU, AICTE approved, NAAC & NBA Accredited
- Website: https://gnindia.dronacharya.info
- Phone: 0120-2322022, 2323851-56
- Email: registrar@gnindia.dronacharya.info
- Admission Helpline: +91-9910380115
- WhatsApp: https://api.whatsapp.com/send?phone=919910380115

COURSES:
B.Tech: CSE, CSIT, IT, CSE-AIML, ECE, ECS, EEE, ME
PG: MBA

FEES:
- B.Tech Total: Rs 2.43 Lakh to 3.75 Lakh (varies by branch)
- Exact fees: visit website or call admission office

ADMISSIONS:
- UG: JEE Main / UPTAC counselling
- PG: CAT / MAT / CUET
- Online Form: https://admission.dronacharya.info/gn/applyonline.aspx
- Admission Brochure: https://gnindia.dronacharya.info/Downloads/Admissions/dronacharya-group-of-institutions-admission-brochure-2026.pdf
- Education Loan: https://gnindia.dronacharya.info/Education-Loan.aspx
- Scholarships: https://gnindia.dronacharya.info/Financial-support.aspx

PLACEMENTS:
- Highest Package: 45 LPA (2023)
- Top Recruiters: TCS, Deloitte, HSBC, BYJU'S and many more
- Placement Details: https://gnindia.dronacharya.info/PlacementDesk.aspx

TRANSPORT / BUS SERVICE:
- DGI has 17+ dedicated bus routes covering Delhi, Noida, Greater Noida, Ghaziabad, Faridabad and all NCR regions
- Safe, reliable and punctual buses for students and staff
- Bus Route Schedule (Jan-June 2026): https://gnindia.dronacharya.info/Downloads/BusSchedule/BUS-ROUTE-JANUARY-TO-JUNE-2026.pdf
- For exact stop timings and route details, download the PDF above or contact college: 0120-2322022

CAMPUS FACILITIES:
- Library, Canteen, Cafeteria, Seminar Hall, Auditorium
- R&D Lab, Automation Lab, Conference Hall
- Sports, Clubs, IEEE & CSI Student Chapters
- Women Development Cell
- Transport facility across NCR

RANKINGS:
- ARIIA 2021: Excellent band by MHRD
- NIRF Innovation: Ranked 26-50 in India
- CSI Mumbai: Best Institute of the Year
- NAAC & NBA Accredited

CONTACT:
- Website: https://gnindia.dronacharya.info
- FAQ: https://gnindia.dronacharya.info/FAQ.aspx
- Events: https://gnindia.dronacharya.info/events/currentEvent.aspx
- Social: Instagram @dgi_dronacharya | Twitter @DronacharyaDgi
"""

conversations = {}

def get_ai_reply(user_phone, user_message):
    if user_phone not in conversations:
        conversations[user_phone] = model.start_chat(history=[])
    try:
        full_msg = DGI_KNOWLEDGE + "\n\nStudent says: " + user_message
        response = conversations[user_phone].send_message(full_msg)
        return response.text
    except Exception as e:
        print(f"Gemini error: {e}")
        return "Sorry, technical issue! Visit: gnindia.dronacharya.info or call 0120-2322022"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "unknown")
    print(f"Message from {sender}: {incoming_msg}")
    reply = get_ai_reply(sender, incoming_msg)
    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)

@app.route("/", methods=["GET"])
def home():
    return "DGI WhatsApp AI Bot is running! Powered by Gemini AI."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
