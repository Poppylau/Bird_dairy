import streamlit as st
import json
from datetime import date
import hashlib

# ✅ 必須放在第一行 streamlit 指令
st.set_page_config(page_title="每日一鳥", page_icon="🐦", layout="centered")

# 讀取 JSON 檔
with open("birds.json", "r", encoding="utf-8") as f:
    birds = json.load(f)

# 根據日期顯示一隻鳥
def get_today_bird():
    today = str(date.today())
    hash_value = int(hashlib.md5(today.encode()).hexdigest(), 16)
    index = hash_value % len(birds)
    return birds[index]

# 側邊欄選擇頁面
page = st.sidebar.radio("📖 選擇頁面", ["🐦 每日一鳥", "📋 所有鳥類"])

# =============================
# 每日一鳥
# =============================
if page == "🐦 每日一鳥":
    bird = get_today_bird()
    st.title("🐦 每日一鳥")
    st.header(f"{bird['chinese_name']} ({bird['english_name']})")
    st.subheader(bird["scientific_name"])
    st.image(bird["image_url"], caption=bird["chinese_name"], use_container_width=True)
    st.audio(bird["audio_url"])
    st.markdown("### 📘 小知識")
    st.write(bird["description"])

# =============================
# 所有鳥類
# =============================
elif page == "📋 所有鳥類":
    st.title("📋 我的鳥類清單")
    for bird in birds:
        with st.expander(f"{bird['chinese_name']} ({bird['english_name']})"):
            st.subheader(bird["scientific_name"])
            st.image(bird["image_url"], caption=bird["chinese_name"], use_container_width=True)
            st.audio(bird["audio_url"])
            st.markdown("### 📘 小知識")
            st.write(bird["description"])
