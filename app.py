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
    st.title("🎮 小遊戲：測下你識幾多雀！")

    if "quiz_index" not in st.session_state:
        st.session_state.quiz_index = random.randint(0, len(birds) - 1)
        st.session_state.answered = False
        st.session_state.correct = None
        st.session_state.selected_option = None
        st.session_state.question_type = random.choice(["english_name", "german_name", "scientific_name", "chinese_name", "introduction"])

    bird = birds[st.session_state.quiz_index]
    question_type = st.session_state.question_type

    # 問題文字
    question_map = {
        "english_name": "呢隻鳥嘅英文名係邊個？",
        "german_name": "呢隻鳥嘅德文名係邊個？",
        "scientific_name": "呢隻鳥嘅學名係邊個？",
        "chinese_name": "呢隻鳥嘅中文名係邊個？",
        "introduction": "以下邊段係呢隻鳥嘅簡介？"
    }
    correct_answer = bird[question_type]

    st.image(bird["image_url"], use_container_width=True)
    st.markdown(f"### ❓ {question_map[question_type]}")

    # 隨機選項（含正確答案）
    options = [correct_answer]
    while len(options) < 4:
        option = random.choice(birds)[question_type]
        if option not in options and pd.notna(option):
            options.append(option)
    random.shuffle(options)

    # 顯示選項
    selected = st.radio("請選擇：", options, index=options.index(st.session_state.selected_option) if st.session_state.selected_option in options else 0)

    if not st.session_state.answered:
        if st.button("✅ 提交答案"):
            st.session_state.selected_option = selected
            if selected == correct_answer:
                st.success("🎉 答啱喇！")
                st.session_state.correct = True
            else:
                st.error(f"😢 錯喇，正確答案係：{correct_answer}")
                st.session_state.correct = False
            st.session_state.answered = True
    else:
        if st.session_state.correct is True:
            st.success("🎉 你啱晒啦！")
        else:
            st.error(f"😢 錯喇，正確答案係：{correct_answer}")

        if st.button("➡️ 下一題"):
            st.session_state.quiz_index = random.randint(0, len(birds) - 1)
            st.session_state.answered = False
            st.session_state.correct = None
            st.session_state.selected_option = None
            st.session_state.question_type = random.choice(["english_name", "german_name", "scientific_name", "chinese_name", "introduction"])
