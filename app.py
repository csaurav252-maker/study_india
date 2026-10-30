# Final Ed-Tech App with Database Clear/Delete Option

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


# --- Database Setup ---
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

# --- Sidebar Configuration ---
st.sidebar.title("🚀 Smart Learn Hub")
st.sidebar.markdown("---")

st.sidebar.subheader("🔑 AI Configuration")
api_key_input = st.sidebar.text_input("Enter Google Gemini API Key", type="password", help="तुमची Gemini API Key इथे प्रविष्ट करा.")

st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Navigation Menu", 
    [
        "🤖 AI Real Question Generator", 
        "📝 Take Mega Test (100+ Pool)",
        "🗑️ Database Management (Delete All)"
    ]
)

conn = sqlite3.connect("pro_learning.db")
cursor = conn.cursor()

if menu == "🤖 AI Real Question Generator":
    st.title("🤖 Real AI Question Generator (Gemini 3.8)")
    st.markdown("येथे फक्त आणि फक्त **खऱ्या आणि दर्जेदार प्रश्नांची** निर्मिती केली जाईल.")

    with st.form("ai_gen_form"):
        ai_stream = st.selectbox(
            "Select Faculty", 
            ["MPSC / UPSC", "MCA / BCA", "CA / Commerce", "Science", "Nursing"]
        )
        ai_topic = st.text_input("Enter Syllabus Topic (उदा. Python Functions, Indian Polity, GST)")
        
        ai_count = st.slider("How many questions to generate in this batch?", min_value=5, max_value=25, value=15, step=5)
        
        generate_btn = st.form_submit_button("✨ Generate Real Questions via Gemini AI")

        if generate_btn:
            if not api_key_input:
                st.error("⚠️ कृपया डाव्या बाजूच्या मेनूमध्ये तुमची Google Gemini API Key प्रविष्ट करा.")
            elif not ai_topic:
                st.error("⚠️ कृपया सिलॅबस टॉपिकचे नाव प्रविष्ट करा.")
            else:
                try:
                    genai.configure(api_key=api_key_input)
                    model = genai.GenerativeModel("models/gemini-3.8-flash")
                    
                    prompt = f\"\"\"
                    You are an expert professor and examiner for {ai_stream}. 
                    Generate exactly {ai_count} professional, high-quality multiple-choice questions for the topic "{ai_topic}" matching the 2026 syllabus.
                    Format each question strictly in this format using '###' as a separator between questions:
                    Question text here?
                    A) Option 1
                    B) Option 2
                    C) Option 3
                    D) Option 4
                    Correct: A
                    ###
                    Make sure questions are completely accurate, academic, and relevant.
                    \"\"\"
                    
                    with st.spinner(f"🔄 Gemini AI {ai_topic} वर अचूक प्रश्न तयार करत आहे... कृपया थोडा वेळ थांबा."):
                        response = model.generate_content(prompt)
                        text_output = response.text
                        
                        raw_questions = text_output.split("###")
                        added_count = 0
                        
                        for q_block in raw_questions:
                            lines = [l.strip() for l in q_block.strip().split("\\n") if l.strip()]
                            if len(lines) >= 6:
                                q_text = lines[0]
                                o_a = lines[1][2:].strip() if lines[1].startswith("A)") else lines[1]
                                o_b = lines[2][2:].strip() if lines[2].startswith("B)") else lines[2]
                                o_c = lines[3][2:].strip() if lines[3].startswith("C)") else lines[3]
                                o_d = lines[4][2:].strip() if lines[4].startswith("D)") else lines[4]
                                
                                correct_ans = "A"
                                for l in lines[5:]:
                                    if "Correct" in l or "अचूक" in l:
                                        if "B" in l.upper(): correct_ans = "B"
                                        elif "C" in l.upper(): correct_ans = "C"
                                        elif "D" in l.upper(): correct_ans = "D"
                                        break
                                
                                cursor.execute(
                                    \"\"\"
                                    INSERT INTO questions (stream, topic, question, opt_a, opt_b, opt_c, opt_d, correct)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                                \"\"\",
                                    (ai_stream, ai_topic, q_text, o_a, o_b, o_c, o_d, correct_ans)
                                )
                                added_count += 1
                        
                        conn.commit()
                        if added_count > 0:
                            st.success(f"✅ Gemini AI द्वारे '{ai_topic}' वर यशस्वीरित्या **{added_count}** अस्सल प्रश्न डेटाबेसमध्ये जोडले गेले आहेत!")
                        else:
                            st.warning("⚠️ AI ने रिस्पॉन्स दिला पण फॉर्मेट जुळला नाही. पुन्हा प्रयत्न करा.")
                            
                except Exception as e:
                    st.error(f"❌ API एरर आला: {str(e)}")

elif menu == "📝 Take Mega Test (100+ Pool)":
    st.title("📝 Mega Faculty Test Engine")

    streams = ["MPSC / UPSC", "MCA / BCA", "CA / Commerce", "Science", "Nursing"]
    selected_stream = st.selectbox("🎯 अभ्यास शाखा (Faculty) निवडा:", streams)

    cursor.execute("SELECT COUNT(*) FROM questions WHERE stream = ?", (selected_stream,))
    total_available = cursor.fetchone()[0]

    if total_available > 0:
        st.success(f"'{selected_stream}' या शाखेसाठी डेटाबेसमध्ये एकूण **{total_available}** प्रश्न उपलब्ध आहेत.")

        max_limit = min(50, total_available)
        num_questions = st.slider(
            "⚙️ टेस्टमध्ये किती प्रश्न हवे आहेत?",
            min_value=5,
            max_value=max_limit,
            value=min(10, max_limit),
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
                        <p style="color: gray; font-size: 14px;">Topic: {topic} | Stream: {stream}</p>
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
                    st.success(f"🎉 अभिनंदन! तुमचे गुण: **{score} / {len(questions)}** ({percentage:.1f}%) - अतिशय उच्च कामगिरी!")
                elif percentage >= 40:
                    st.warning(f"⚠️ तुमचे गुण: **{score} / {len(questions)}** ({percentage:.1f}%) - अजून थोड्या सरावाची गरज आहे.")
                else:
                    st.error(f"❌ तुमचे गुण: **{score} / {len(questions)}** ({percentage:.1f}%) - अधिक अभ्यासाची आवश्यकता आहे.")
    else:
        st.warning(f"'{selected_stream}' या शाखेसाठी सध्या डेटाबेसमध्ये प्रश्न नाहीत. कृपया आधी 'AI Real Question Generator' मधून प्रश्न तयार करून घ्या.")

elif menu == "🗑️ Database Management (Delete All)":
    st.title("🗑️ Database Management & Cleanup")
    st.markdown("येथून तू डेटाबेसमध्ये साठलेले **सर्व जुने किंवा डमी प्रश्न एकाच क्लिकवर डिलीट** करू शकतोस.")

    cursor.execute("SELECT COUNT(*) FROM questions")
    total_q = cursor.fetchone()[0]
    st.info(f"सध्या डेटाबेसमध्ये एकूण **{total_q}** प्रश्न साठलेले आहेत.")

    if st.button("⚠️ DELETE ALL QUESTIONS (डेटाबेस पूर्णपणे रिकामा करा)"):
        cursor.execute("DELETE FROM questions")
        conn.commit()
        st.success("✅ डेटाबेस यशस्वीरित्या क्लिन करण्यात आला आहे! सर्व जुने प्रश्न डिलीट झाले आहेत.")
        st.balloons()

conn.close()
"""

# Jupyter Notebook मधून थेट app.py फाईल तयार करणे
with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_code)

print("✅ 'app.py' फाईल यशस्वीरित्या अपडेट झाली आहे (डेटाबेस डिलीट/क्लिन ऑप्शनसह)!")
