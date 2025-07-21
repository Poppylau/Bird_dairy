import streamlit as st
import pandas as pd
from datetime import date
import hashlib
import random

st.set_page_config(page_title="每日一鳥", page_icon="🐦", layout="centered")

# 讀 Excel
df = pd.read_excel("Bird_app.xlsx")
birds = df.to_dict(orient="records")

def get_today_bird():
    return random.choice(birds)

# 主選單
page = st.sidebar.radio("📖 選擇頁面", ["🐦 每日一鳥", "📋 所有鳥類"])

if page == "🐦 每日一鳥":
    bird = get_today_bird()
    st.title("🐦 每日一鳥")
    st.header(f"{bird['chinese_name']} ({bird['english_name']} / {bird['german_name']})")
    st.subheader(f"📖 學名：{bird['scientific_name']}｜科：{bird['family']}")
    st.image(bird["image_url"], use_container_width=True)
    if pd.notna(bird["audio_url"]):
        st.audio(bird["audio_url"])
    st.markdown("### 📘 介紹")
    st.write(bird["introduction"])

elif page == "📋 所有鳥類":
    st.title("📋 所有鳥類清單")

    # 按 family 分組
    grouped = df.groupby("family")

    for family_name, group in grouped:
        with st.expander(f"🧬 科：{family_name}（共 {len(group)} 種）"):
            for _, bird in group.iterrows():
                with st.expander(f"{bird['chinese_name']} ({bird['english_name']} / {bird['german_name']})"):
                    st.subheader(f"學名：{bird['scientific_name']}｜科：{bird['family']}")
                    st.image(bird["image_url"], use_container_width=True)
                    if pd.notna(bird["audio_url"]):
                        st.audio(bird["audio_url"])
                    st.markdown("### 📘 介紹")
                    st.write(bird["introduction"])

