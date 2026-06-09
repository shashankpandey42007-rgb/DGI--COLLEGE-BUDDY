"""
╔══════════════════════════════════════════════════════════╗
║   DGI Greater Noida — AI WhatsApp Chatbot                ║
║   Powered by: Flask + Twilio + Claude AI                 ║
║   Website: gnindia.dronacharya.info                      ║
╚══════════════════════════════════════════════════════════╝
"""

import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import anthropic

app = Flask(__name__)

# ─── Anthropic client (reads ANTHROPIC_API_KEY from environment) ───
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# ─────────────────────────────────────────────────────────────────────
#  DGI KNOWLEDGE BASE  (scraped from gnindia.dronacharya.info)
#  Update this section whenever college info changes
# ─────────────────────────────────────────────────────────────────────

DGI_KNOWLEDGE = """
You are the official AI assistant for Dronacharya Group of Institutions (DGI), Greater Noida.
Answer every question in a friendly, helpful, concise manner using the facts below.
If you don't know something specific, direct the student to the official website or phone number.
Always respond in the same language the user writes in (Hindi or English).
Keep replies short and WhatsApp-friendly (no markdown headers, use emojis naturally).

=== ABOUT DGI ===
- Full Name: Dronacharya Group of Institutions (DGI)
- Location: Knowledge Park-III, Greater Noida, Uttar Pradesh, Delhi-NCR
- Established: 2006, by Smt. Anguri Devi Charitable Trust
- Affiliation: Dr. A.P.J. Abdul Kalam Technical University (AKTU), Lucknow
- Approval: AICTE approved, NAAC & NBA Accredited
- Website: https://gnindia.dronacharya.info
- Coordinates: 28.4744, 77.5040

=== COURSES OFFERED ===
B.Tech branches (8 departments):
1. CSE – Computer Science & Engineering
2. CSIT – Computer Science & Information Technology
3. IT – Information Technology
4. CSE (AIML) – AI & Machine Learning
5. ECE – Electronics & Communication Engineering
6. EEE – Electrical & Electronics Engineering
7. ECS – Electronics & Computer Science
8. ME – Mechanical Engineering

PG Programme:
- MBA (Master of Business Administration)

=== FEES ===
- B.Tech Total Fee: ₹2.43 Lakh – ₹3.75 Lakh (varies by branch)
- For exact fee details: https://gnindia.dronacharya.info or call admission office

=== ADMISSIONS ===
- UG Admission: Based on JEE Main / UPTAC (UP Technical Admission Counselling)
- PG Admission: Based on CAT / MAT / CUET scores
- 15% seats on merit basis, rest through UPTAC counselling
- Online Application: https://admission.dronacharya.info/gn/applyonline.aspx
- UPTAC Brochure 2026: Available on website
- Online Fee Payment: https://gnindia.dronacharya.info/Online-Fee-Payment.aspx
- Education Loan: Available, details at https://gnindia.dronacharya.info/Education-Loan.aspx
- Financial Support/Scholarships: https://gnindia.dronacharya.info/Financial-support.aspx
- JEE Mains 2026 info: https://gnindia.dronacharya.info/Jee-Mains-2026.aspx
- Admission Brochure 2026: https://gnindia.dronacharya.info/Downloads/Admissions/dronacharya-group-of-institutions-admission-brochure-2026.pdf

=== PLACEMENTS ===
- Highest Package: 45 LPA (2023)
- Top Recruiters: TCS, Deloitte, HSBC, BYJU'S, and many more
- Placement Desk: https://gnindia.dronacharya.info/PlacementDesk.aspx
- Placement Brochure: https://gnindia.dronacharya.info/Downloads/Placements/Placement-Brochure-DGI.pdf
- Batch-wise Placement Record: https://gnindia.dronacharya.info/PlacementStatistics/Batch-wise-record-2026.aspx
- Placement Notices: https://gnindia.dronacharya.info/Placement-Notice.aspx

=== RANKINGS & ACHIEVEMENTS ===
- ARIIA 2021: Recognised in 'Excellent' band by MHRD, Govt. of India
- NIRF Innovation Ranking 2020: Ranked 26–50 among top 50 colleges in India
- CSI Mumbai Award: 'Best Institute of the Year' for innovative pedagogical approaches
- NCAT Award: 'Best Performing Institute'
- IIT Collaborations: Academic initiatives with IITs
- NAAC & NBA Accredited

=== CAMPUS LIFE ===
- Facilities: State-of-the-art labs, modern infrastructure, library, sports, hostel
- Clubs: Multiple student clubs (see https://gnindia.dronacharya.info/Clubs.aspx)
- Student Chapters: IEEE, CSI, and others
- Women Development Cell: Active on campus
- Gallery: https://gnindia.dronacharya.info/gallery.aspx
- Safety & Security: Dedicated cell on campus
- Academic Calendar: https://gnindia.dronacharya.info/academiccalendar.aspx

=== RESEARCH & INNOVATION ===
- MoE's IIC (Innovation Cell): Active
- Patents & Copyrights: https://gnindia.dronacharya.info/Patents-Copyrights.aspx
- Centre of Excellence: https://gnindia.dronacharya.info/Centre-of-Excellence.aspx
- International Conferences hosted: https://gnindia.dronacharya.info/International-Conferences.aspx
- Summer Internship: https://gnindia.dronacharya.info/Summer-Internship.aspx
- GATE Qualifiers 2026: https://gnindia.dronacharya.info/Gate-Qualifiers/Gate-2026.aspx
- Startups from DGI: https://gnindia.dronacharya.info/Startups-Glimpse.aspx

=== CONTACT ===
- Website: https://gnindia.dronacharya.info
- Online Admission Form: https://admission.dronacharya.info/gn/applyonline.aspx
- Social Media: Twitter @DronacharyaDgi | Instagram @dgi_dronacharya
- Address: Knowledge Park-III, Greater Noida, Uttar Pradesh
- FAQ Page: https://gnindia.dronacharya.info/FAQ.aspx
- Events: https://gnindia.dronacharya.info/events/currentEvent.aspx

=== IMPORTANT INSTRUCTION ===
- Always be polite and supportive to students
- For fees / exact hostel / faculty contact not listed here, ask them to visit the website or contact the college directly
- End responses with a helpful tip or relevant link when possible
"""

# ─────────────────────────────────────────────────────────────────────
#  In-memory conversation store  {phone_number: [messages]}
#  For production use Redis or a database
# ─────────────────────────────────────────────────────────────────────
conversations = {}
MAX_HISTORY = 10   # keep last 10 message pairs to save tokens


def get_ai_reply(user_phone: str, user_message: str) -> str:
    """Send message to Claude AI with DGI context and conversation history."""

    # Initialise conversation history for new users
    if user_phone not in conversations:
        conversations[user_phone] = []

    # Add new user message
    conversations[user_phone].append({"role": "user", "content": user_message})

    # Keep only last MAX_HISTORY messages
    history = conversations[user_phone][-MAX_HISTORY:]

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            system=DGI_KNOWLEDGE,
            messages=history,
        )
        reply = response.content[0].text

        # Save assistant reply to history
        conversations[user_phone].append({"role": "assistant", "content": reply})

        return reply

    except Exception as e:
        print(f"Claude API error: {e}")
        return (
            "⚠️ Sorry, I'm having a technical issue right now.\n"
            "Please visit: gnindia.dronacharya.info\n"
            "or call the admission office directly for help!"
        )


# ─────────────────────────────────────────────────────────────────────
#  TWILIO WEBHOOK  — receives every incoming WhatsApp message
# ─────────────────────────────────────────────────────────────────────

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender       = request.values.get("From", "unknown")  # e.g. whatsapp:+919XXXXXXXXX

    print(f"📩 Message from {sender}: {incoming_msg}")

    # Get AI-generated reply
    reply = get_ai_reply(sender, incoming_msg)

    # Send back via Twilio
    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)


# ─────────────────────────────────────────────────────────────────────
#  HEALTH CHECK
# ─────────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def home():
    return "✅ DGI WhatsApp AI Bot is running! Powered by Claude AI."


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
