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
    st.title("🎮 雀鳥小測驗")
    bird = get_today_bird()

    st.markdown("#### 以下是介紹，請猜猜是哪一隻雀：")
    st.write(bird["introduction"])

    choice = st.radio("你覺得係邊隻雀？", [b["chinese_name"] for b in birds])
    
    if st.button("提交答案"):
        if choice == bird["chinese_name"]:
            st.success("🎉 答對了！")
            st.write(f"英文名：**{bird['english_name']}**")
            st.write(f"德文名：**{bird['german_name']}**")
            st.write(f"學名：**{bird['scientific_name']}**")
        else:
            st.error("❌ 錯咗，再試下！")
            st.info(f"正確答案係：{bird['chinese_name']}")
