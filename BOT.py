from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# ─────────────────────────────────────────────
#  COLLEGE DATA — Edit these with your college info
# ─────────────────────────────────────────────

COLLEGE_NAME = "ABC College of Technology"

ADMISSION_INFO = """
📋 *ADMISSION & FEES INFO*

🎓 Courses Offered:
• B.Tech (CSE, ECE, ME, CE)
• BCA, BBA, B.Com
• MBA, MCA

💰 Fee Structure (Per Year):
• B.Tech: ₹85,000
• BCA/BBA: ₹45,000
• MBA/MCA: ₹70,000

📅 Admission Dates:
• Form Release: April 1
• Last Date: June 30
• Merit List: July 10

📞 Admission Office: 011-XXXXXXXX
🌐 Website: www.abccollege.ac.in
"""

TIMETABLE_INFO = """
📅 *TIMETABLE & SCHEDULE*

⏰ College Timings:
• Morning Shift: 8:00 AM – 1:00 PM
• Evening Shift: 1:30 PM – 6:30 PM

🗓️ Class Schedule:
• Mon–Fri: Regular Classes
• Saturday: Labs & Practicals
• Sunday: Holiday

📲 For your branch timetable, contact:
• CSE: Room 101 | ECE: Room 205
• ME: Room 301  | CE: Room 401

📌 Tip: Full timetable PDF is on the college website under *Academics > Timetable*
"""

EXAM_INFO = """
📝 *EXAM & RESULTS*

📆 Upcoming Exam Dates:
• Mid-Term Exam: 15 July – 22 July
• End-Term Exam: 10 Nov – 25 Nov
• Practical Exams: 1 Dec – 10 Dec

📋 Exam Rules:
• Hall ticket required
• 75% attendance mandatory
• No electronic devices allowed

📊 Results:
• Declared within 30 days of exam
• Check: www.abccollege.ac.in/results
• OR SMS your Roll No to: 7XXXXXXXXX

🔁 Re-evaluation: Apply within 7 days of result
"""

EVENTS_INFO = """
🎉 *EVENTS & NOTICES*

📢 Upcoming Events:
• 15 Jun → Annual Tech Fest "TECHNO-2025"
• 20 Jun → Guest Lecture: AI & Future Jobs
• 1 Jul  → Sports Week Begins
• 10 Jul → Cultural Night

📌 Important Notices:
• Fee last date: 30 June (avoid ₹500 fine)
• Library cards renewal: Before 15 June
• Hostel allotment: 5 July

📲 Join official notice channel:
  wa.me/+91XXXXXXXXXX
"""

FACULTY_INFO = """
👨‍🏫 *FACULTY CONTACT INFO*

🏢 HODs:
• CSE Dept: Dr. Sharma → 9XXXXXXXXX
• ECE Dept: Dr. Verma  → 9XXXXXXXXX
• ME Dept:  Dr. Gupta  → 9XXXXXXXXX

📌 Key Offices:
• Principal Office: Ext. 101
• Exam Controller: Ext. 202
• Accounts (Fees): Ext. 303
• Library:         Ext. 404
• Hostel Warden:   Ext. 505

⏰ Office Hours: 9 AM – 5 PM (Mon–Sat)
📧 Email: info@abccollege.ac.in
"""

MAIN_MENU = f"""
👋 Welcome to *{COLLEGE_NAME}* Bot!

Please choose an option:

1️⃣  Admission & Fees
2️⃣  Timetable & Schedule
3️⃣  Exam & Results
4️⃣  Events & Notices
5️⃣  Faculty Contacts

_Type a number (1–5) to continue_
_Type *menu* anytime to return here_
"""

# ─────────────────────────────────────────────
#  WEBHOOK — Twilio sends all messages here
# ─────────────────────────────────────────────

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    # Route to correct response
    if incoming_msg in ["hi", "hello", "hey", "start", "menu", "help", ""]:
        reply = MAIN_MENU

    elif incoming_msg in ["1", "admission", "fees", "admission & fees"]:
        reply = ADMISSION_INFO

    elif incoming_msg in ["2", "timetable", "schedule", "time table"]:
        reply = TIMETABLE_INFO

    elif incoming_msg in ["3", "exam", "result", "results", "exams"]:
        reply = EXAM_INFO

    elif incoming_msg in ["4", "events", "notice", "notices", "event"]:
        reply = EVENTS_INFO

    elif incoming_msg in ["5", "faculty", "teacher", "contact", "staff"]:
        reply = FACULTY_INFO

    else:
        reply = (
            f"❓ Sorry, I didn't understand that.\n\n"
            f"Type *menu* to see all options, or choose:\n"
            f"1️⃣ Admission  2️⃣ Timetable  3️⃣ Exams\n"
            f"4️⃣ Events     5️⃣ Faculty"
        )

    msg.body(reply)
    return str(resp)


# ─────────────────────────────────────────────
#  HEALTH CHECK (for deployment platforms)
# ─────────────────────────────────────────────

@app.route("/", methods=["GET"])
def home():
    return f"✅ {COLLEGE_NAME} WhatsApp Bot is running!"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
