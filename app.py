# Jupyter Notebook मध्ये Professional App Update करणारी स्क्रिप्ट

app_code = """import sqlite3
import streamlit as st

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

    # जर डेटाबेस रिकामा असेल, तर प्रत्येक फॅकल्टीसाठी भरपूर सॅम्पल प्रश्न इन्सर्ट करणे
    cursor.execute("SELECT COUNT(*) FROM questions")
    if cursor.fetchone()[0] == 0:
        sample_data = [
            # MPSC / UPSC (History, Geography, Polity, Economics)
            ("MPSC / UPSC", "History", "भारताचे पहिले सरन्यायाधीश (Chief Justice) कोण होते?", "H. J. Kania", "Dr. B. R. Ambedkar", "Jawaharlal Nehru", "Sardar Patel", "A"),
            ("MPSC / UPSC", "Geography", "महाराष्ट्रातील सर्वात लांब नदी कोणती आहे?", "कृष्णा", "गोदावरी", "तापी", "भीमा", "B"),
            ("MPSC / UPSC", "Polity", "भारतीय संविधानाचे शिल्पकार म्हणून कोणाला ओळखले जाते?", "महात्मा गांधी", "डॉ. बाबासाहेब आंबेडकर", "राजेंद्र प्रसाद", "जवाहरलाल नेहरू", "B"),
            ("MPSC / UPSC", "History", "सन १८५७ च्या उठावाची सुरुवात महाराष्ट्रात कोणत्या ठिकाणाहून झाली?", "पुणे", "नागपूर", "पेठ", "सातारा", "C"),
            ("MPSC / UPSC", "Economics", "भारतात नियोजन आयोगाची (Planning Commission) स्थापना कधी झाली?", "1947", "1950", "1952", "1951", "B"),
            
            # MCA / BCA (Python, Database, Data Structures, Networking)
            ("MCA / BCA", "Python", "Python मध्ये list तयार करण्यासाठी कोणत्या ब्रॅकेट्सचा वापर होतो?", "{} (Curly)", "[] (Square)", "() (Parentheses)", "<> (Angle)", "B"),
            ("MCA / BCA", "Database", "SQL चा फुल फॉर्म खालीलपैकी काय आहे?", "Structured Query Language", "Simple Question Language", "Standard Query Logic", "System Quality Language", "A"),
            ("MCA / BCA", "Data Structures", "FIFO (First In, First Out) तत्त्वावर खालीलपैकी काय काम करते?", "Stack", "Queue", "Tree", "Graph", "B"),
            ("MCA / BCA", "Python", "Python मध्ये कोणती की-वर्ड फंक्शन डिफाइन करण्यासाठी वापरतात?", "func", "define", "def", "function", "C"),
            ("MCA / BCA", "Networking", "IP address चे किती बिट्सचे व्हर्जन IPv4 मध्ये असते?", "16-bit", "32-bit", "64-bit", "128-bit", "B"),

            # CA / Commerce (Taxation, Accounting, Economics, Auditing)
            ("CA / Commerce", "Taxation", "GST भारतात संपूर्ण देशात कधी लागू झाला?", "1 January 2016", "1 July 2017", "15 August 2017", "1 April 2018", "B"),
            ("CA / Commerce", "Accounting", "खालीलपैकी कोणता ताळेबंद (Balance Sheet) चा भाग आहे?", "Assets & Liabilities", "Income & Expenses", "Profit & Loss", "Cash Flow Only", "A"),
            ("CA / Commerce", "Auditing", "कंपनीच्या हिशोबाची तपासणी करणाऱ्या व्यक्तीला काय म्हणतात?", "Accountant", "Auditor", "Director", "Manager", "B"),
            ("CA / Commerce", "Economics", "महागाई वाढल्यास चलनात काय परिणाम होतो?", "पैशाचे मूल्य वाढते", "पैशाचे मूल्य घटते", "काहीही बदल होत नाही", "बँक बंद पडतात", "B"),

            # Science (Physics, Chemistry, Biology)
            ("Science", "Physics", "प्रकाशाचा वेग निर्वात पोकळीत (Vacuum) किती असतो?", "3 × 10^8 m/s", "3 × 10^6 m/s", "3 × 10^5 km/h", "300 m/s", "A"),
            ("Science", "Chemistry", "सर्वात हलका वायू (Lightest Element) कोणता आहे?", "ऑक्सिजन", "हायड्रोजन", "नायट्रोजन", "हेलियम", "B"),
            ("Science", "Biology", "मानवी शरीरातील सर्वात मोठी ग्रंथी (Gland) कोणती?", "लसिका ग्रंथी", "यकृत (Liver)", "जठर", "थायरॉईड", "B"),
            ("Science", "Physics", "विजेच्या दाबाचे (Voltage) एकक काय आहे?", "अम्पियर", "व्होल्ट", "ओहम", "वॅट", "B"),

            # Nursing (Anatomy, First Aid, Pharmacology)
            ("Nursing", "Anatomy", "मानवी शरीरात रक्ताभिसरण संस्थेचा मुख्य अवयव कोणता आहे?", "फुफ्फुस", "यकृत", "हृदय", "मदूक", "C"),
            ("Nursing", "First Aid", "सामान्य मानवी शरीराचे तापमान किती असते?", "98.6°F", "95.0°F", "102.4°F", "97.0°F", "A"),
            ("Nursing", "Pharmacology", "पॅरासिटामॉल औषध प्रामुख्याने कशासाठी वापरले जाते?", "ताप आणि वेदना कमी करण्यासाठी", "रक्ताचा दाब वाढवण्यासाठी", "डोळ्यांच्या संसर्गासाठी", "रक्ताची साखर नियंत्रणासाठी", "A"),
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
    "Go to", ["Dashboard", "Take Faculty Test", "Contribute Questions"]
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

    st.info("👈 डाव्या बाजूच्या मेनूमधून 'Take Faculty Test' निवडून तुमच्या आवडीच्या शाखेची टेस्ट सुरू करा!")

elif menu == "Take Faculty Test":
    st.title("📝 Faculty-Based MCQ Test")

    streams = [
        "MPSC / UPSC",
        "MCA / BCA",
        "CA / Commerce",
        "Science",
        "Nursing",
    ]
    selected_stream = st.selectbox("🎯 तुमची अभ्यास शाखा (Faculty) निवडा:", streams)

    # उस फॅकल्टीसाठी उपलब्ध एकूण प्रश्न तपासणे
    cursor.execute("SELECT COUNT(*) FROM questions WHERE stream = ?", (selected_stream,))
    total_available = cursor.fetchone()[0]

    if total_available > 0:
        st.success(f"'{selected_stream}' या शाखेसाठी डेटाबेसमध्ये एकूण {total_available} प्रश्न उपलब्ध आहेत.")

        # युजरला हवी असलेली प्रश्नांची संख्या निवडण्यासाठी स्लायडर (Custom Test Length)
        num_questions = st.slider(
            "⚙️ तुम्हाला या टेस्टमध्ये किती प्रश्न सोडवायचे आहेत?",
            min_value=1,
            max_value=total_available,
            value=min(3, total_available)
        )

        # निवडलेल्या संख्येनुसार रँडम प्रश्न फेच करणे
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
        st.warning(f"'{selected_stream}' या शाखेसाठी सध्या प्रश्न उपलब्ध नाहीत. तुम्ही 'Contribute Questions' मधून नवीन प्रश्न ॲड करू शकता.")

elif menu == "Contribute Questions":
    st.title("➕ Add New Questions to Faculty Bank")

    with st.form("add_form"):
        f_stream = st.selectbox(
            "Select Faculty",
            [
                "MPSC / UPSC",
                "MCA / BCA",
                "CA / Commerce",
                "Science",
                "Nursing",
            ],
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
                    (
                        f_stream,
                        f_topic,
                        f_question,
                        opt_a,
                        opt_b,
                        opt_c,
                        opt_d,
                        f_correct,
                    ),
                )
                conn.commit()
                st.success("✅ प्रश्न यशस्वीरित्या डेटाबेसमध्ये ॲड झाला! आता तो टेस्टमध्ये दिसेल.")
            else:
                st.error("कृपया सर्व माहिती अचूक भरा.")

conn.close()
"""

# Jupyter Notebook मधून थेट app.py फाईल तयार करणे
with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_code)

print("✅ 'app.py' फाईल यशस्वीरित्या सेव्ह झाली आहे आणि त्यात टेस्ट कस्टमायझेशन फीचर आले आहे!")
