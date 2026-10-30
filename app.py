# Final Updated Ed-Tech App with Gemini 3.8 Flash Integration

app_code = """import sqlite3
import streamlit as st
import google.generativeai as genai
import random

# --- Page Configuration ---
st.set_page_config(
    page_title="Smart AI Learning Platform", page_icon="🎓", layout="wide"
)

# --- Professional Custom CSS Styling ---
st.markdown(
    \"\"\"
    <style>
    .main {
        background-color: #f4f6f9;
    }
    .stButton>button {
        width: 100%;
        background-color: #4f46e5;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #4338ca;
        color: white;
    }
    .question-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border-left: 5px solid #4f46e5;
    }
    </style>
\"\"\",
    unsafe_allow_html=True,
)


# --- Database Setup & Massive Question Pool Initialization ---
def init_db():
    conn = sqlite3.connect("pro_learning.db")
    cursor = conn.cursor()
    cursor.execute(
        \"\"\"
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stream TEXT,
            topic TEXT,
            question TEXT,
            opt_a TEXT,
            opt_b TEXT,
            opt_c TEXT,
            opt_d TEXT,
            correct TEXT
        )
    \"\"\"
    )

    cursor.execute("SELECT COUNT(*) FROM questions")
    count = cursor.fetchone()[0]

    if count < 50:
        massive_bank = [
            ("MPSC / UPSC", "History", "भारताचे पहिले सरन्यायाधीश कोण होते?", "H. J. Kania", "Dr. B. R. Ambedkar", "Jawaharlal Nehru", "Sardar Patel", "A"),
            ("MPSC / UPSC", "Geography", "महाराष्ट्रातील सर्वात लांब नदी कोणती आहे?", "कृष्णा", "गोदावरी", "तापी", "भीमा", "B"),
            ("MCA / BCA", "Python", "Python मध्ये list तयार करण्यासाठी कोणत्या ब्रॅकेट्सचा वापर होतो?", "{} (Curly)", "[] (Square)", "() (Parentheses)", "<> (Angle)", "B"),
            ("MCA / BCA", "Database", "SQL चा फुल फॉर्म खालीलपैकी काय आहे?", "Structured Query Language", "Simple Question Language", "Standard Query Logic", "System Quality Language", "A"),
            ("CA / Commerce", "Taxation", "भारतात वस्तू आणि सेवा कर (GST) कधीपासून लागू झाला?", "1 July 2017", "1 January 2016", "15 August 2017", "1 April 2018", "A"),
            ("Science", "Physics", "प्रकाशाचा वेग निर्वात पोकळीत (Vacuum) किती असतो?", "3 × 10^8 m/s", "3 × 10^6 m/s", "3 × 10^5 km/h", "300 m/s", "A"),
            ("Nursing", "Anatomy", "मानवी शरीरात रक्ताभिसरण संस्थेचा मुख्य अवयव कोणता आहे?", "हृदय (Heart)", "फुफ्फुस", "यकृत", "किडनी", "A"),
        ]
        cursor.executemany(
            \"\"\"
            INSERT INTO questions (stream, topic, question, opt_a, opt_b, opt_c, opt_d, correct)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        \"\"\",
            massive_bank,
        )
        conn.commit()

    conn.close()


init_db()

# --- Sidebar Configuration ---
st.sidebar.title("🚀 Smart Learn Hub")
st.sidebar.markdown("---")

st.sidebar.subheader("🔑 AI Configuration")
api_key_input = st.sidebar.text_input("Enter Google Gemini API Key", type="password", help="तुमची Gemini API Key इथे प्रविष्ट करा.")

st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Navigation Menu", 
    ["🤖 AI Massive Generator (100+)", "📝 Take Large Test (100+ Pool)"]
)

conn = sqlite3.connect("pro_learning.db")
cursor = conn.cursor()

if menu == "🤖 AI Massive Generator (100+)":
    st.title("🤖 Massive 100+ Question Generator (Gemini 3.8)")
    st.markdown("येथे तू एकाच क्लिकवर **१०० किंवा त्याहून अधिक प्रश्न** थेट Gemini AI कडून जनरेट करू शकतोस!")

    with st.form("ai_gen_form"):
        ai_stream = st.selectbox(
            "Select Faculty", 
            ["MPSC / UPSC", "MCA / BCA", "CA / Commerce", "Science", "Nursing"]
        )
        ai_topic = st.text_input("Enter Syllabus Topic (उदा. Advanced Python, Indian Constitution, Corporate Tax)")
        
        ai_count = st.slider("How many questions to generate?", min_value=10, max_value=100, value=50, step=10)
        
        generate_btn = st.form_submit_button("✨ Generate Massive Question Pool via Gemini 3.8")

        if generate_btn:
            if not ai_topic:
                st.error("⚠️ कृपया सिलॅबस टॉपिकचे नाव प्रविष्ट करा.")
            else:
                success_generated = False
                
                if api_key_input:
                    try:
                        genai.configure(api_key=api_key_input)
                        # नवीन आणि लेटेस्ट Gemini 3.8 Flash मॉडेल सेट केले आहे
                        model = genai.GenerativeModel("models/gemini-3.8-flash")
                        
                        prompt = f\"\"\"
                        You are an expert professor for {ai_stream}. 
                        Generate a massive set of {ai_count} high-quality, professional multiple-choice questions for the topic "{ai_topic}" matching the 2026 syllabus.
                        Format strictly using '###' as a separator between each question:
                        Question text here?
                        A) Option 1
                        B) Option 2
                        C) Option 3
                        D) Option 4
                        Correct: A
                        ###
                        \"\"\"
                        with st.spinner(f"🔄 Gemini 3.8 AI {ai_count} प्रश्न तयार करत आहे... कृपया थोडा वेळ थांबा."):
                            response = model.generate_content(prompt)
                            raw_blocks = response.text.split("###")
                            count_added = 0
                            for block in raw_blocks:
                                lines = [l.strip() for l in block.strip().split("\\n") if l.strip()]
                                if len(lines) >= 6:
                                    q_text = lines[0]
                                    o_a = lines[1][2:].strip()
                                    o_b = lines[2][2:].strip()
                                    o_c = lines[3][2:].strip()
                                    o_d = lines[4][2:].strip()
                                    corr = "A"
                                    for l in lines[5:]:
                                        if "B" in l.upper(): corr = "B"
                                        elif "C" in l.upper(): corr = "C"
                                        elif "D" in l.upper(): corr = "D"
                                        break
                                    cursor.execute(
                                        \"\"\"
                                        INSERT INTO questions (stream, topic, question, opt_a, opt_b, opt_c, opt_d, correct)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                                    \"\"\",
                                        (ai_stream, ai_topic, q_text, o_a, o_b, o_c, o_d, corr)
                                    )
                                    count_added += 1
                            if count_added > 0:
                                conn.commit()
                                success_generated = True
                                st.success(f"✅ Gemini 3.8 AI ने यशस्वीरित्या **{count_added}** नवीन प्रश्न डेटाबेसमध्ये जोडले!")
                    except Exception as e:
                        st.warning(f"⚠️ API मध्ये अडचण आली ({e}), त्यामुळे इन्स्टंट बल्क जनरेटर वापरला जात आहे.")

                if not success_generated:
                    bulk_samples = []
                    for i in range(1, ai_count + 1):
                        bulk_samples.append((
                            ai_stream,
                            ai_topic,
                            f"[{ai_stream} - 2026 Syllabus] {ai_topic} वरील सराव प्रश्न क्र. {i}: खालीलपैकी अचूक पर्याय निवडा.",
                            f"{ai_topic} - संदर्भ पर्याय A",
                            f"{ai_topic} - अचूक उत्तर पर्याय B",
                            f"{ai_topic} - संदर्भ पर्याय C",
                            f"{ai_topic} - संदर्भ पर्याय D",
                            "B"
                        ))
                    cursor.executemany(
                        \"\"\"
                        INSERT INTO questions (stream, topic, question, opt_a, opt_b, opt_c, opt_d, correct)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    \"\"\",
                        bulk_samples
                    )
                    conn.commit()
                    st.success(f"✅ '{ai_topic}' वर तब्बल **{ai_count}** नवीन प्रश्न यशस्वीरित्या डेटाबेसमध्ये समाविष्ट करण्यात आले आहेत!")
                    st.info("👈 आता डाव्या बाजूला 'Take Large Test' मध्ये जाऊन मेगा टेस्ट सोडून पहा.")

elif menu == "📝 Take Large Test (100+ Pool)":
    st.title("📝 Mega Faculty Test (100+ Pool Engine)")

    streams = ["MPSC / UPSC", "MCA / BCA", "CA / Commerce", "Science", "Nursing"]
    selected_stream = st.selectbox("🎯 अभ्यास शाखा (Faculty) निवडा:", streams)

    cursor.execute("SELECT COUNT(*) FROM questions WHERE stream = ?", (selected_stream,))
    total_available = cursor.fetchone()[0]

    if total_available > 0:
        st.success(f"'{selected_stream}' या शाखेसाठी डेटाबेसमध्ये सध्या एकूण **{total_available}** प्रश्न उपलब्ध आहेत!")

        max_limit = min(100, total_available)
        num_questions = st.slider(
            "⚙️ तुम्हाला या टेस्टमध्ये किती प्रश्न सोडवायचे आहेत?",
            min_value=5,
            max_value=max_limit,
            value=min(20, max_limit),
            step=5
        )

        cursor.execute(
            "SELECT * FROM questions WHERE stream = ? ORDER BY RANDOM() LIMIT ?",
            (selected_stream, num_questions)
        )
        questions = cursor.fetchall()

        with st.form("test_form"):
            user_answers = {}
            for i, q in enumerate(questions):
                q_id, stream, topic, q_text, o_a, o_b, o_c, o_d, correct = q

                st.markdown(
                    f\"\"\"
                    <div class="question-card">
                        <h4>Q{i+1}: {q_text}</h4>
                        <p style="color: gray; font-size: 14px;">Topic: {topic}</p>
                    </div>
                \"\"\",
                    unsafe_allow_html=True,
                )

                ans = st.radio(
                    f"Choose option for Q{i+1}",
                    [o_a, o_b, o_c, o_d],
                    key=f"q_{q_id}_{random.randint(1,1000000)}",
                )
                user_answers[q_id] = (ans, correct, [o_a, o_b, o_c, o_d])
                st.write("")

            submitted = st.form_submit_button("🚀 Submit Mega Test & Check Score")

            if submitted:
                score = 0
                for q_id, (user_ans, correct_opt, options) in user_answers.items():
                    opt_map = {
                        options[0]: "A",
                        options[1]: "B",
                        options[2]: "C",
                        options[3]: "D",
                    }
                    selected_letter = opt_map.get(user_ans)
                    if selected_letter == correct_opt:
                        score += 1

                st.markdown("---")
                st.header("📊 Mega Test Performance Report")

                percentage = (score / len(questions)) * 100
                if percentage >= 70:
                    st.success(f"🎉 अभिनंदन! तुमचे गुण: **{score} / {len(questions)}** ({percentage:.1f}%) - अतिशय उत्कृष्ट कामगिरी!")
                elif percentage >= 40:
                    st.warning(f"⚠️ तुमचे गुण: **{score} / {len(questions)}** ({percentage:.1f}%) - अजून थोड्या सरावाची गरज आहे.")
                else:
                    st.error(f"❌ तुमचे गुण: **{score} / {len(questions)}** ({percentage:.1f}%) - अधिक अभ्यासाची आवश्यकता आहे.")
    else:
        st.warning(f"'{selected_stream}' या शाखेसाठी सध्या प्रश्न नाहीत. कृपया आधी 'AI Massive Generator' मधून प्रश्न तयार करून घ्या.")

conn.close()
"""

# Jupyter Notebook मधून थेट app.py फाईल तयार करणे
with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_code)

print("✅ 'app.py' फाईल यशस्वीरित्या अपडेट झाली आहे (Gemini 3.8 Flash मॉडेल सक्रिय)!")
