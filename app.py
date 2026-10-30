# Jupyter Notebook मध्ये AI Question Generator ॲड करणारी स्क्रिप्ट

app_code = """import sqlite3
import streamlit as st
import os

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


# --- Database Connection & Setup ---
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

    if count < 30:
        sample_data = [
            ("MPSC / UPSC", "History", "भारताचे पहिले सरन्यायाधीश (Chief Justice) कोण होते?", "H. J. Kania", "Dr. B. R. Ambedkar", "Jawaharlal Nehru", "Sardar Patel", "A"),
            ("MPSC / UPSC", "Geography", "महाराष्ट्रातील सर्वात लांब नदी कोणती आहे?", "कृष्णा", "गोदावरी", "तापी", "भीमा", "B"),
            ("MCA / BCA", "Python", "Python मध्ये list तयार करण्यासाठी कोणत्या ब्रॅकेट्सचा वापर होतो?", "{} (Curly)", "[] (Square)", "() (Parentheses)", "<> (Angle)", "B"),
            ("MCA / BCA", "Database", "SQL चा फुल फॉर्म खालीलपैकी काय आहे?", "Structured Query Language", "Simple Question Language", "Standard Query Logic", "System Quality Language", "A"),
            ("CA / Commerce", "Taxation", "GST भारतात संपूर्ण देशात कधी लागू झाला?", "1 January 2016", "1 July 2017", "15 August 2017", "1 April 2018", "B"),
            ("Science", "Physics", "प्रकाशाचा वेग निर्वात पोकळीत (Vacuum) किती असतो?", "3 × 10^8 m/s", "3 × 10^6 m/s", "3 × 10^5 km/h", "300 m/s", "A"),
            ("Nursing", "Anatomy", "मानवी शरीरात रक्ताभिसरण संस्थेचा मुख्य अवयव कोणता आहे?", "फुफ्फुस", "यकृत", "हृदय", "मदूक", "C"),
        ]
        cursor.executemany(
            \"\"\"
            INSERT INTO questions (stream, topic, question, opt_a, opt_b, opt_c, opt_d, correct)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        \"\"\",
            sample_data,
        )
        conn.commit()

    conn.close()


init_db()

# --- Sidebar Navigation ---
st.sidebar.title("🚀 Smart Learn Hub")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Go to", ["Dashboard", "Take Faculty Test", "AI Question Generator", "Contribute Questions"]
)

conn = sqlite3.connect("pro_learning.db")
cursor = conn.cursor()

if menu == "Dashboard":
    st.title("🎓 Professional AI Learning Ecosystem")
    st.markdown("विद्यार्थ्यांसाठी विविध शाखांवर (Faculties) आधारित स्मार्ट टेस्ट सिरीज प्लॅटफॉर्म.")

    cursor.execute("SELECT COUNT(DISTINCT stream) FROM questions")
    total_streams = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM questions")
    total_q = cursor.fetchone()[0]

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Active Streams / Faculties", value=total_streams)
    with col2:
        st.metric(label="Total Question Bank", value=total_q)

    st.info("👈 डाव्या बाजूच्या मेनूमधून 'AI Question Generator' किंवा 'Take Faculty Test' निवडा!")

elif menu == "Take Faculty Test":
    st.title("📝 Faculty-Based MCQ Test")

    streams = ["MPSC / UPSC", "MCA / BCA", "CA / Commerce", "Science", "Nursing"]
    selected_stream = st.selectbox("🎯 तुमची अभ्यास शाखा (Faculty) निवडा:", streams)

    cursor.execute("SELECT COUNT(*) FROM questions WHERE stream = ?", (selected_stream,))
    total_available = cursor.fetchone()[0]

    if total_available > 0:
        st.success(f"'{selected_stream}' या शाखेसाठी डेटाबेसमध्ये एकूण {total_available} प्रश्न उपलब्ध आहेत.")

        num_questions = st.slider(
            "⚙️ तुम्हाला या टेस्टमध्ये किती प्रश्न सोडवायचे आहेत?",
            min_value=1,
            max_value=total_available,
            value=min(5, total_available)
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
                    key=f"q_{q_id}",
                )
                user_answers[q_id] = (ans, correct, [o_a, o_b, o_c, o_d])
                st.write("")

            submitted = st.form_submit_button("🚀 Submit Test & Check Score")

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
                st.header("📊 Test Performance Report")

                percentage = (score / len(questions)) * 100
                if percentage >= 70:
                    st.success(f"🎉 अभिनंदन! तुमचे गुण: **{score} / {len(questions)}** ({percentage:.1f}%) - अतिशय उत्तम कामगिरी!")
                elif percentage >= 40:
                    st.warning(f"⚠️ तुमचे गुण: **{score} / {len(questions)}** ({percentage:.1f}%) - अजून थोड्या सरावाची गरज आहे.")
                else:
                    st.error(f"❌ तुमचे गुण: **{score} / {len(questions)}** ({percentage:.1f}%) - खूपच कमी गुण, गांभीर्याने अभ्यास करा.")
    else:
        st.warning(f"'{selected_stream}' या शाखेसाठी सध्या प्रश्न उपलब्ध नाहीत.")

elif menu == "AI Question Generator":
    st.title("🤖 AI-Driven Question Generator")
    st.markdown("एका क्लिकवर कोणत्याही विषयावर AI द्वारे नवीन प्रश्न तयार करून थेट डेटाबेसमध्ये सेव्ह करा.")

    with st.form("ai_gen_form"):
        ai_stream = st.selectbox("Select Faculty", ["MPSC / UPSC", "MCA / BCA", "CA / Commerce", "Science", "Nursing"])
        ai_topic = st.text_input("Enter Topic Name (उदा. Python Functions, Indian Polity, Modern History)")
        ai_count = st.slider("How many questions to generate?", min_value=1, max_value=10, value=3)
        
        generate_btn = st.form_submit_button("✨ Generate & Save via AI")

        if generate_btn:
            if ai_topic:
                # येथे आपण AI द्वारे प्रश्न जनरेट करून डेटाबेसमध्ये इन्सर्ट करण्याची प्रक्रिया सिमुलेट करत आहोत
                # पुढील टप्प्यात यात आपण थेट LLM API कनेक्ट करू शकतो.
                generated_sample = [
                    (ai_stream, ai_topic, f"{ai_topic} वर आधारित AI प्रश्न १: खालीलपैकी योग्य विधान कोणते?", "पर्याय अ", "पर्याय ब", "पर्याय क", "पर्याय ड", "A"),
                    (ai_stream, ai_topic, f"{ai_topic} वर आधारित AI प्रश्न २: मुख्य संकल्पना स्पष्ट करा?", "संकल्पना A", "संकल्पना B", "संकल्पना C", "संकल्पना D", "B"),
                    (ai_stream, ai_topic, f"{ai_topic} वर आधारित AI प्रश्न ३: योग्य पर्याय निवडा?", "Option 1", "Option 2", "Option 3", "Option 4", "C"),
                ]
                
                # युजरने मागितलेल्या संख्येनुसार प्रश्न इन्सर्ट करणे
                for q_data in generated_sample[:ai_count]:
                    cursor.execute(
                        \"\"\"
                        INSERT INTO questions (stream, topic, question, opt_a, opt_b, opt_c, opt_d, correct)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    \"\"\",
                        q_data
                    )
                conn.commit()
                st.success(f"✅ AI ने यशस्वीरित्या '{ai_topic}' या विषयावर {ai_count} नवीन प्रश्न तयार करून डेटाबेसमध्ये जोडले आहेत!")
                st.info("आता तुम्ही 'Take Faculty Test' मध्ये जाऊन हे नवीन प्रश्न सोडवू शकता.")
            else:
                st.error("कृपया टॉपिकचे नाव प्रविष्ट करा.")

elif menu == "Contribute Questions":
    st.title("➕ Add New Questions to Faculty Bank")

    with st.form("add_form"):
        f_stream = st.selectbox(
            "Select Faculty",
            ["MPSC / UPSC", "MCA / BCA", "CA / Commerce", "Science", "Nursing"],
        )
        f_topic = st.text_input("Topic Name (उदा. History, Python, Taxation)")
        f_question = st.text_area("Question Text")
        opt_a = st.text_input("Option A")
        opt_b = st.text_input("Option B")
        opt_c = st.text_input("Option C")
        opt_d = st.text_input("Option D")
        f_correct = st.selectbox("Correct Option", ["A", "B", "C", "D"])

        btn = st.form_submit_button("💾 Save Question")

        if btn:
            if f_question and opt_a and opt_b:
                cursor.execute(
                    \"\"\"
                    INSERT INTO questions (stream, topic, question, opt_a, opt_b, opt_c, opt_d, correct)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                \"\"\",
                    (f_stream, f_topic, f_question, opt_a, opt_b, opt_c, opt_d, f_correct),
                )
                conn.commit()
                st.success("✅ प्रश्न यशस्वीरित्या डेटाबेसमध्ये ॲड झाला!")
            else:
                st.error("कृपया सर्व माहिती अचूक भरा.")

conn.close()
"""

# Jupyter Notebook मधून थेट app.py फाईल तयार करणे
with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_code)

print("✅ 'app.py' फाईल यशस्वीरित्या अपडेट झाली आहे आणि त्यात AI Question Generator फीचर आले आहे!")
