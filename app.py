import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="每日一鳥", page_icon="🐦", layout="centered")

# 讀 Excel
df = pd.read_excel("Bird_app.xlsx")
birds = df.to_dict(orient="records")

def get_today_bird():
    return random.choice(birds)

def show_bird_info(bird):
    st.header(f"{bird['chinese_name']} ({bird['english_name']} / {bird['german_name']})")
    st.subheader(f"📖 學名：{bird['scientific_name']}｜科：{bird['family']}")
    
    if pd.notna(bird["image_url"]) and str(bird["image_url"]).strip().startswith("http"):
        st.image(bird["image_url"], use_container_width=True)

    if pd.notna(bird["audio_url"]) and str(bird["audio_url"]).strip().startswith("http"):
        st.audio(bird["audio_url"])
    
    st.markdown("### 📘 介紹")
    st.write(bird["introduction"])

    if pd.notna(bird["fun_facts"]) and bird["fun_facts"] != "":
        st.markdown("### 🎯 趣味小知識")
        st.write(bird["fun_facts"])


# 主選單
page = st.sidebar.radio("📖 請選擇頁面：", ["🐦 每日一雀", "📋 所有鳥類", "🎮 小遊戲"])

# 🐦 每日一雀
if page == "🐦 每日一雀":
    st.title("🐦 每日一雀")
    bird = get_today_bird()
    show_bird_info(bird)

# 📋 所有鳥類
elif page == "📋 所有鳥類":
    st.title("📋 所有鳥類清單")
    grouped = df.groupby("family")
    for family_name, group in grouped:
        with st.expander(f"🧬 科：{family_name}（共 {len(group)} 種）"):
            for _, bird in group.iterrows():
                with st.expander(f"{bird['chinese_name']} ({bird['english_name']} / {bird['german_name']})"):
                    show_bird_info(bird)

# 🎮 小遊戲
elif page == "🎮 小遊戲":

    def init_quiz():
        st.session_state.quiz_index = random.randint(0, len(birds) - 1)
        st.session_state.answered = False
        st.session_state.correct = False
        st.session_state.question_type = random.choice(
            ["scientific_name", "chinese_name", "english_name", "german_name", "introduction"]
        )

    if "quiz_index" not in st.session_state:
        init_quiz()

    bird = birds[st.session_state.quiz_index]
    question_type = st.session_state.question_type

    st.title("🎮 小遊戲：測下你識幾多雀！")

    question_map = {
        "scientific_name": "學名",
        "chinese_name": "中文名",
        "english_name": "英文名",
        "german_name": "德文名",
        "introduction": "介紹"
    }

    if question_type == "introduction":
        st.markdown("### ❓ 根據以下介紹，呢隻係咩鳥？")
        st.info(bird["introduction"])
        correct_answer = bird["chinese_name"]
        options = [correct_answer]
        while len(options) < 4:
            other = random.choice(birds)["chinese_name"]
            if other not in options and pd.notna(other):
                options.append(other)
    else:
        st.image(bird["image_url"], width=300)
        st.markdown(f"### ❓ 呢隻鳥嘅 {question_map[question_type]} 係邊個？")
        correct_answer = bird[question_type]
        options = [correct_answer]
        while len(options) < 4:
            other = random.choice(birds)[question_type]
            if other not in options and pd.notna(other):
                options.append(other)

    random.shuffle(options)

    # 只更新 radio，唔即時處理答案
    if "user_answer" not in st.session_state:
        st.session_state.user_answer = None

    selected = st.radio("請選擇：", options, key="quiz_radio")

    # 改左 radio，要手動更新 user_answer
    if st.session_state.user_answer != selected:
        st.session_state.user_answer = selected


    if not st.session_state.answered:
        if st.button("✅ 提交答案"):
            if st.session_state.user_answer == correct_answer:
                st.success("🎉 答啱喇！")
                st.session_state.correct = True
            else:
                st.error(f"😢 錯喇，正確答案係：{correct_answer}")
            st.session_state.answered = True

