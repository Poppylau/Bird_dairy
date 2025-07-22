import streamlit as st
import pandas as pd
import random

# 讀取 Excel 檔案
df = pd.read_excel("Bird_app.xlsx")

st.sidebar.title("📘 請選擇頁面：")
page = st.sidebar.selectbox("", ["📖 每日一雀", "🗂 所有鳥類", "🧠 小遊戲"])

def show_bird_info(bird):
    st.subheader(f"{bird['chinese_name']} ({bird['english_name']})")
    st.markdown(f"**學名**: *{bird['scientific_name']}*")
    st.markdown(f"**德文名**: {bird['german_name']}")
    st.markdown(f"**科別**: {bird['family']}")
    st.image(bird['image_url'], width=300)
    if pd.notna(bird['audio_url']):
        st.audio(bird['audio_url'])
    st.markdown(f"**簡介**:{bird['introduction']}")
    st.markdown(f"**有趣知識**:{bird['fun_facts']}")

if page == "📖 每日一雀":
    st.title("📖 每日一雀")
    bird = df.sample(1).iloc[0]
    show_bird_info(bird)

elif page == "🗂 所有鳥類":
    st.title("🗂 所有鳥類")
    families = df['family'].dropna().unique()
    selected_family = st.selectbox("選擇科別", ["全部"] + sorted(families.tolist()))
    if selected_family != "全部":
        filtered_df = df[df['family'] == selected_family]
    else:
        filtered_df = df
    for _, bird in filtered_df.iterrows():
        with st.expander(f"{bird['chinese_name']} ({bird['english_name']})"):
            show_bird_info(bird)

elif page == "🧠 小遊戲":
    st.title("🧠 小遊戲：你認得呢隻雀嗎？")
    bird = df.sample(1).iloc[0]
    options = df.sample(3).append(bird).drop_duplicates().sample(4)
    question_type = random.choice(["chinese_name", "english_name", "german_name", "scientific_name"])
    label_map = {
        "chinese_name": "中文名稱",
        "english_name": "English name",
        "german_name": "Deutsch Name",
        "scientific_name": "Scientific name"
    }
    st.image(bird['image_url'], width=300)
    st.markdown(f"請問呢隻雀嘅 **{label_map[question_type]}** 係：")
    choices = options[question_type].tolist()
    answer = st.radio("選項：", choices, index=None)
    if answer:
        if answer == bird[question_type]:
            st.success("✅ 答對啦！")
        else:
            st.error(f"❌ 唔啱。正確答案係：{bird[question_type]}")
        with st.expander("🔍 更多資料"):
            show_bird_info(bird)
