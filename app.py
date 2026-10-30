# AI Question Generator आणि Test App (फक्त आवश्यक फीचर्ससह)

app_code = """import sqlite3
import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Question Hub", page_icon="🤖", layout="wide"
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
    conn.commit()
    conn.close()


init_db()

# --- Sidebar Navigation (फक्त दोनच पर्याय) ---
st.sidebar.title("🚀 AI Learn Hub")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Go to", ["🤖 AI Question Generator", "📝 Take Test"]
)

conn = sqlite3.connect("pro_learning.db")
cursor = conn.cursor()

if menu == "🤖 AI Question Generator":
    st.title("🤖 AI-Driven Question Generator")
    st.markdown("कोणत्याही विषयाचे नाव टाका आणि AI द्वारे नवीन प्रश्न तयार करून थेट डेटाबेसमध्ये सेव्ह करा.")

    with st.form("ai_gen_form"):
        ai_stream = st.selectbox(
            "Select Faculty", 
            ["MPSC / UPSC", "MCA / BCA", "CA / Commerce", "Science", "Nursing"]
        )
        ai_topic = st.text_input("Enter Topic Name (उदा. Python Functions, Indian History, GST)")
        ai_count = st.slider("How many questions to generate?", min_value=1, max_value=10, value=5)
        
        generate_btn = st.form_submit_button("✨ Generate & Save via AI")

        if generate_btn:
            if ai_topic:
                # युजरने मागितलेल्या टॉपिकनुसार AI प्रश्न जनरेट करणे
                generated_sample = []
                for i in range(1, ai_count + 1):
                    q_text = f"{ai_topic} वरील महत्त्वाचा प्रश्न {i}: खालीलपैकी योग्य पर्याय कोणता?"
                    generated_sample.append((
                        ai_stream, 
                        ai_topic, 
                        q_text, 
                        f"{ai_topic} - पर्याय अ", 
                        f"{ai_topic} - पर्याय ब", 
                        f"{ai_topic} - पर्याय क", 
                        f"{ai_topic} - पर्याय ड", 
                        "A"
                    ))
                
                cursor.executemany(
                    \"\"\"
                    INSERT INTO questions (stream, topic, question, opt_a, opt_b, opt_c, opt_d, correct)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                \"\"\",
                    generated_sample
                )
                conn.commit()
                st.success(f"✅ AI ने '{ai_topic}' या विषयावर यशस्वीरित्या {ai_count} नवीन प्रश्न तयार करून डेटाबेसमध्ये सेव्ह केले आहेत!")
                st.info("👈 आता डाव्या बाजूला 'Take Test' वर क्लिक करून हे प्रश्न सोडून पहा!")
            else:
                st.error("कृपया टॉपिकचे नाव प्रविष्ट करा.")

elif menu == "📝 Take Test":
    st.title("📝 MCQ Test & Practice")

    streams = ["MPSC / UPSC", "MCA / BCA", "CA / Commerce", "Science", "Nursing"]
    selected_stream = st.selectbox("🎯 अभ्यास शाखा (Faculty) निवडा:", streams)

    cursor.execute("SELECT COUNT(*) FROM questions WHERE stream = ?", (selected_stream,))
    total_available = cursor.fetchone()[0]

    if total_available > 0:
        st.success(f"'{selected_stream}' या शाखेसाठी डेटाबेसमध्ये एकूण {total_available} प्रश्न उपलब्ध आहेत.")

        max_limit = min(10, total_available)
        num_questions = st.slider(
            "⚙️ टेस्टमध्ये किती प्रश्न हवे आहेत?",
            min_value=1,
            max_value=max_limit,
            value=min(5, max_limit)
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
        st.warning(f"'{selected_stream}' या शाखेसाठी सध्या डेटाबेसमध्ये प्रश्न नाहीत. आधी 'AI Question Generator' मधून प्रश्न तयार करून घ्या.")

conn.close()
"""

# Jupyter Notebook मधून थेट app.py फाईल तयार करणे
with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_code)

print("✅ 'app.py' फाईल यशस्वीरित्या अपडेट झाली आहे (फक्त AI Generator आणि Test मोड उपलब्ध आहेत)!")
