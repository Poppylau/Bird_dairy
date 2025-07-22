import streamlit as st
import pandas as pd
import random

# --- 讀取 Excel 資料 ---
df = pd.read_excel("Bird_app.xlsx")

# --- 網頁標題 ---
st.set_page_config(page_title="Bird Diary", layout="wide")
st.title("🐦 Bird Diary 鳥類日記")

# --- 選單 ---
page = st.sidebar.selectbox("請選擇頁面：", ["📖 每日一雀", "🗂️ 所有鳥類總覽", "🎮 小遊戲：猜猜鳥"])

# --- 每日一雀 ---
if page == "📖 每日一雀":
    bird = df.sample(1).iloc[0]  # 隨機抽一隻
    st.header(bird['chinese_name'] + f" ({bird['english_name']})")
    st.subheader(bird['german_name'])

    if pd.notna(bird['image_url']):
        st.image(bird['image_url'], use_container_width=True)

    st.markdown(f"**學名**：{bird['scientific_name']}")
    st.markdown(f"**科別**：{bird['family']}")

    st.markdown("---")
    st.markdown("### 📚 介紹")
    st.write(bird['introduction'])

    st.markdown("### 🎉 趣聞 Fun Facts")
    st.write(bird['fun_facts'])

    if pd.notna(bird['audio_url']):
        st.markdown("[🎧 聽叫聲]({})".format(bird['audio_url']))

# --- 所有鳥類 ---
elif page == "🗂️ 所有鳥類總覽":
    families = sorted(df['family'].dropna().unique())
    selected_family = st.sidebar.selectbox("篩選科別：", ["全部"] + families)

    if selected_family != "全部":
        filtered_df = df[df['family'] == selected_family]
    else:
        filtered_df = df

    for _, bird in filtered_df.iterrows():
        st.subheader(bird['chinese_name'] + f" ({bird['english_name']})")
        col1, col2 = st.columns([1, 2])
        with col1:
            if pd.notna(bird['image_url']):
                st.image(bird['image_url'], width=200)
        with col2:
            st.markdown(f"**德文名**：{bird['german_name']}")
            st.markdown(f"**學名**：{bird['scientific_name']}")
            st.markdown(f"**科別**：{bird['family']}")
            st.markdown(f"**介紹**：{bird['introduction'][:150]}...")
            st.markdown(f"**趣聞**：{bird['fun_facts'][:100]}...")
            if pd.notna(bird['audio_url']):
                st.markdown("[🎧 聽叫聲]({})".format(bird['audio_url']))
        st.markdown("---")

# --- 小遊戲 ---
elif page == "🎮 小遊戲：猜猜鳥":
    st.subheader("🎯 小測驗：猜猜鳥的中文名")
    options = df.sample(4)
    answer_row = options.sample(1).iloc[0]

    st.image(answer_row['image_url'], caption="請問這是什麼鳥？")
    choices = options['chinese_name'].tolist()
    random.shuffle(choices)
    
    selected = st.radio("你的答案是？", choices)

    if st.button("提交答案"):
        if selected == answer_row['chinese_name']:
            st.success("答對啦！👏👏")
        else:
            st.error(f"可惜，正確答案係：{answer_row['chinese_name']}")

        with st.expander("查看更多資訊"):
            st.markdown(f"**英文名**：{answer_row['english_name']}")
            st.markdown(f"**德文名**：{answer_row['german_name']}")
            st.markdown(f"**學名**：{answer_row['scientific_name']}")
            st.markdown(f"**科別**：{answer_row['family']}")
            st.write(answer_row['introduction'])
            st.markdown(f"**趣聞**：{answer_row['fun_facts']}")
            if pd.notna(answer_row['audio_url']):
                st.markdown("[🎧 聽叫聲]({})".format(answer_row['audio_url']))
