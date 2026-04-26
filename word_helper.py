import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime

# 数据文件
DATA_FILE = "english_words.csv"
PRESET_FILE = "preset_grade1.csv"

# 人教版小学一年级英语预置词库
PRESET_WORDS = [
    {"word": "pen", "phonetic": "/pen/", "meaning": "钢笔", "sentence": "I have a pen."},
    {"word": "pencil", "phonetic": "/ˈpensl/", "meaning": "铅笔", "sentence": "This is my pencil."},
    {"word": "book", "phonetic": "/bʊk/", "meaning": "书", "sentence": "I like this book."},
    {"word": "bag", "phonetic": "/bæɡ/", "meaning": "书包", "sentence": "My bag is blue."},
    {"word": "ruler", "phonetic": "/ˈruːlə/", "meaning": "尺子", "sentence": "Show me your ruler."},
    {"word": "eraser", "phonetic": "/ɪˈreɪzə/", "meaning": "橡皮", "sentence": "I need an eraser."},
    {"word": "pencil-box", "phonetic": "/ˈpenslbɒks/", "meaning": "铅笔盒", "sentence": "Open your pencil-box."},
    {"word": "school", "phonetic": "/skuːl/", "meaning": "学校", "sentence": "Let's go to school."},
    {"word": "teacher", "phonetic": "/ˈtiːtʃə/", "meaning": "老师", "sentence": "She is my teacher."},
    {"word": "student", "phonetic": "/ˈstjuːdənt/", "meaning": "学生", "sentence": "I am a student."},
    {"word": "boy", "phonetic": "/bɔɪ/", "meaning": "男孩", "sentence": "He is a boy."},
    {"word": "girl", "phonetic": "/ɡɜːl/", "meaning": "女孩", "sentence": "She is a girl."},
    {"word": "this", "phonetic": "/ðɪs/", "meaning": "这，这个", "sentence": "This is a dog."},
    {"word": "that", "phonetic": "/ðæt/", "meaning": "那，那个", "sentence": "That is a cat."},
    {"word": "face", "phonetic": "/feɪs/", "meaning": "脸", "sentence": "Touch my face."},
    {"word": "ear", "phonetic": "/ɪə/", "meaning": "耳朵", "sentence": "This is my ear."},
    {"word": "eye", "phonetic": "/aɪ/", "meaning": "眼睛", "sentence": "I have two eyes."},
    {"word": "nose", "phonetic": "/nəʊz/", "meaning": "鼻子", "sentence": "Look at my nose."},
    {"word": "mouth", "phonetic": "/maʊθ/", "meaning": "嘴", "sentence": "Open your mouth."},
    {"word": "arm", "phonetic": "/ɑːm/", "meaning": "胳膊", "sentence": "Wave your arm."},
    {"word": "hand", "phonetic": "/hænd/", "meaning": "手", "sentence": "Clap your hands."},
    {"word": "head", "phonetic": "/hed/", "meaning": "头", "sentence": "Touch your head."},
    {"word": "body", "phonetic": "/ˈbɒdi/", "meaning": "身体", "sentence": "Shake your body."},
    {"word": "leg", "phonetic": "/leɡ/", "meaning": "腿", "sentence": "Shake your leg."},
    {"word": "foot", "phonetic": "/fʊt/", "meaning": "脚", "sentence": "Stamp your foot."},
    {"word": "cat", "phonetic": "/kæt/", "meaning": "猫", "sentence": "It's a cat."},
    {"word": "dog", "phonetic": "/dɒɡ/", "meaning": "狗", "sentence": "It's a dog."},
    {"word": "monkey", "phonetic": "/ˈmʌŋki/", "meaning": "猴子", "sentence": "Funny monkey."},
    {"word": "panda", "phonetic": "/ˈpændə/", "meaning": "熊猫", "sentence": "I like panda."},
    {"word": "bird", "phonetic": "/bɜːd/", "meaning": "鸟", "sentence": "A bird can fly."},
    {"word": "rabbit", "phonetic": "/ˈræbɪt/", "meaning": "兔子", "sentence": "White rabbit."},
    {"word": "duck", "phonetic": "/dʌk/", "meaning": "鸭子", "sentence": "Quack, quack, duck."},
    {"word": "pig", "phonetic": "/pɪɡ/", "meaning": "猪", "sentence": "Big pig."},
    {"word": "red", "phonetic": "/red/", "meaning": "红色", "sentence": "I see red."},
    {"word": "yellow", "phonetic": "/ˈjeləʊ/", "meaning": "黄色", "sentence": "I see yellow."},
    {"word": "green", "phonetic": "/ɡriːn/", "meaning": "绿色", "sentence": "I see green."},
    {"word": "blue", "phonetic": "/bluː/", "meaning": "蓝色", "sentence": "I see blue."},
    {"word": "purple", "phonetic": "/ˈpɜːpl/", "meaning": "紫色", "sentence": "I see purple."},
    {"word": "white", "phonetic": "/waɪt/", "meaning": "白色", "sentence": "I see white."},
    {"word": "black", "phonetic": "/blæk/", "meaning": "黑色", "sentence": "I see black."},
    {"word": "orange", "phonetic": "/ˈɒrɪndʒ/", "meaning": "橙色", "sentence": "I see orange."},
    {"word": "pink", "phonetic": "/pɪŋk/", "meaning": "粉色", "sentence": "I see pink."},
    {"word": "brown", "phonetic": "/braʊn/", "meaning": "棕色", "sentence": "I see brown."},
    {"word": "one", "phonetic": "/wʌn/", "meaning": "一", "sentence": "One pen."},
    {"word": "two", "phonetic": "/tuː/", "meaning": "二", "sentence": "Two apples."},
    {"word": "three", "phonetic": "/θriː/", "meaning": "三", "sentence": "Three books."},
    {"word": "four", "phonetic": "/fɔː/", "meaning": "四", "sentence": "Four cats."},
    {"word": "five", "phonetic": "/faɪv/", "meaning": "五", "sentence": "Five dogs."},
    {"word": "six", "phonetic": "/sɪks/", "meaning": "六", "sentence": "Six birds."},
    {"word": "seven", "phonetic": "/ˈsevən/", "meaning": "七", "sentence": "Seven rabbits."},
    {"word": "eight", "phonetic": "/eɪt/", "meaning": "八", "sentence": "Eight ducks."},
    {"word": "nine", "phonetic": "/naɪn/", "meaning": "九", "sentence": "Nine pigs."},
    {"word": "ten", "phonetic": "/ten/", "meaning": "十", "sentence": "Ten pencils."}
]

# 初始化自定义词库
def init_data():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=[
            "word", "phonetic", "meaning", "sentence",
            "add_time", "master", "wrong_count"
        ])
        df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")

# 初始化预置词库
def init_preset():
    if not os.path.exists(PRESET_FILE):
        df = pd.DataFrame(PRESET_WORDS)
        df["add_time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        df["master"] = 0
        df["wrong_count"] = 0
        df.to_csv(PRESET_FILE, index=False, encoding="utf-8-sig")

# 读取单词库
def load_words():
    return pd.read_csv(DATA_FILE, encoding="utf-8-sig")

# 读取预置词库
def load_preset():
    return pd.read_csv(PRESET_FILE, encoding="utf-8-sig")

# 保存单词库
def save_words(df):
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")

# 保存预置词库
def save_preset(df):
    df.to_csv(PRESET_FILE, index=False, encoding="utf-8-sig")

# 页面配置
st.set_page_config(
    page_title="儿童英语生词学习助手",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化会话状态
if "card_idx" not in st.session_state:
    st.session_state.card_idx = 0
if "show_chinese" not in st.session_state:
    st.session_state.show_chinese = False
if "card_list" not in st.session_state:
    st.session_state.card_list = []

# 初始化测试状态
if "test_started" not in st.session_state:
    st.session_state.test_started = False
if "test_words" not in st.session_state:
    st.session_state.test_words = pd.DataFrame()
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

init_data()
init_preset()
df = load_words()
preset_df = load_preset()

# 侧边栏导航
menu = st.sidebar.radio(
    "功能菜单",
    [
        "📝 添加生词",
        "📚 单词记忆库(可编辑)",
        "📖 预置单词库(一年级)",
        "🃏 背诵卡片",
        "🧪 随机小测试",
        "📊 学习统计"
    ]
)

# 1. 添加生词（修改：仅单词必填，释义/例句选填）
if menu == "📝 添加生词":
    st.header("📝 录入新单词")
    with st.form("word_form"):
        word = st.text_input("英文单词（必填）")
        phonetic = st.text_input("音标（选填）")
        meaning = st.text_input("中文释义（选填）")
        sentence = st.text_input("简单例句（选填）")
        submitted = st.form_submit_button("保存到记忆库")

    if submitted:
        # 仅校验单词必填
        if word.strip():
            new_row = {
                "word": word.strip(),
                "phonetic": phonetic.strip(),
                "meaning": meaning.strip(),
                "sentence": sentence.strip(),
                "add_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "master": 0,
                "wrong_count": 0
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_words(df)
            st.success(f"✅ 单词【{word}】已存入记忆库！")
        else:
            st.warning("请填写单词")

# 2. 单词记忆库(可编辑)
elif menu == "📚 单词记忆库(可编辑)":
    st.header("📚 单词记忆库 & 在线编辑")
    st.info("双击单元格即可修改内容，修改后记得保存")

    edit_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic"
    )

    if st.button("💾 保存修改内容"):
        save_words(edit_df)
        st.success("✅ 修改已保存！")
        df = load_words()

    st.divider()
    st.subheader("🗑️ 删除指定单词")
    if len(df) > 0:
        del_word = st.selectbox("选择单词", df["word"].tolist())
        if st.button("确认删除"):
            df = df[df["word"] != del_word].reset_index(drop=True)
            save_words(df)
            st.success(f"✅ 已删除：{del_word}")
    else:
        st.info("暂无单词")

    st.divider()
    st.download_button(
        label="📥 导出单词表",
        data=edit_df.to_csv(index=False, encoding="utf-8-sig"),
        file_name="儿童英语生词表.csv",
        mime="text/csv"
    )

# 3. 预置单词库（一年级）
elif menu == "📖 预置单词库(一年级)":
    st.header("📖 人教版小学一年级英语单词库")
    st.success("内置53个一年级核心单词，只读不可编辑，学习进度自动保存")
    st.dataframe(preset_df[["word", "phonetic", "meaning", "sentence"]], use_container_width=True)
    
    st.divider()
    st.subheader("📊 预置词库学习进度")
    total_p = len(preset_df)
    master_p = len(preset_df[preset_df["master"] == 1])
    weak_p = len(preset_df[preset_df["master"] == 0])
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("总单词数", total_p)
    with c2:
        st.metric("已掌握", master_p)
    with c3:
        st.metric("待学习", weak_p)

# 4. 背诵卡片（修改：默认不显示音标，音标放入显示释义中）
elif menu == "🃏 背诵卡片":
    st.header("🃏 单词卡片背诵")
    
    # 词库选择
    book_source = st.radio("选择词库", ["自定义记忆库", "一年级预置词库"], horizontal=True)
    mode = st.radio("背诵范围", ["全部单词", "仅未掌握单词"], horizontal=True)

    # 加载对应词库
    if book_source == "自定义记忆库":
        source_df = df
        save_func = save_words
    else:
        source_df = preset_df
        save_func = save_preset

    # 筛选范围
    if mode == "仅未掌握单词":
        card_df = source_df[source_df["master"] == 0].reset_index(drop=True)
    else:
        card_df = source_df.reset_index(drop=True)

    if len(card_df) == 0:
        st.info("暂无需要背诵的单词～")
    else:
        if not st.session_state.card_list or len(st.session_state.card_list) != len(card_df):
            st.session_state.card_list = card_df.index.tolist()
            random.shuffle(st.session_state.card_list)
            st.session_state.card_idx = 0
            st.session_state.show_chinese = False

        now_idx = st.session_state.card_list[st.session_state.card_idx]
        row = card_df.loc[now_idx]

        card_style = """
        <style>
        .card{
            padding:40px;
            border-radius:16px;
            background:#f0f8ff;
            text-align:center;
            box-shadow: 0 2px 8px #eee;
        }
        </style>
        """
        st.markdown(card_style, unsafe_allow_html=True)

        # 默认仅显示单词，不显示音标
        if not st.session_state.show_chinese:
            st.markdown(f"""
            <div class="card">
                <h2>{row['word']}</h2>
            </div>
            """, unsafe_allow_html=True)
        # 显示释义时：单词+音标+释义+例句
        else:
            st.markdown(f"""
            <div class="card">
                <h2>{row['word']}</h2>
                <p style="color:#666;">{row['phonetic']}</p>
                <hr>
                <h3 style="color:#2E86AB;">{row['meaning']}</h3>
                <p style="color:#888;">{row['sentence']}</p>
            </div>
            """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("🔍 显示释义"):
                st.session_state.show_chinese = True
                st.rerun()
        with col2:
            if st.button("⬅️ 上一个") and st.session_state.card_idx > 0:
                st.session_state.card_idx -= 1
                st.session_state.show_chinese = False
                st.rerun()
        with col3:
            if st.button("➡️ 下一个") and st.session_state.card_idx < len(st.session_state.card_list)-1:
                st.session_state.card_idx += 1
                st.session_state.show_chinese = False
                st.rerun()
        with col4:
            if st.button("🔀 随机换卡"):
                random.shuffle(st.session_state.card_list)
                st.session_state.card_idx = 0
                st.session_state.show_chinese = False
                st.rerun()

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ 标记为已掌握"):
                if book_source == "自定义记忆库":
                    df.loc[df["word"] == row["word"], "master"] = 1
                else:
                    preset_df.loc[preset_df["word"] == row["word"], "master"] = 1
                save_func(source_df)
                st.success(f"【{row['word']}】已标记掌握")
                st.rerun()
        with c2:
            if st.button("❌ 标记为薄弱"):
                if book_source == "自定义记忆库":
                    df.loc[df["word"] == row["word"], "master"] = 0
                else:
                    preset_df.loc[preset_df["word"] == row["word"], "master"] = 0
                save_func(source_df)
                st.warning(f"【{row['word']}】设为薄弱词")
                st.rerun()

        st.caption(f"进度：{st.session_state.card_idx+1} / {len(st.session_state.card_list)}")

# 5. 随机小测试（修改：删除输入框，改为选择对/错）
elif menu == "🧪 随机小测试":
    st.header("🧪 生词小测验")
    
    # 词库选择
    book_source = st.radio("选择词库", ["自定义记忆库", "一年级预置词库"], horizontal=True)
    
    if book_source == "自定义记忆库":
        test_df = df
        save_func = save_words
    else:
        test_df = preset_df
        save_func = save_preset

    if len(test_df) == 0:
        st.info("当前词库暂无单词")
    else:
        test_num = st.slider("本次出题数量", 3, 15, 5)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("开始测试"):
                st.session_state.test_started = True
                st.session_state.test_words = test_df.sample(min(test_num, len(test_df))).reset_index(drop=True)
                st.session_state.user_answers = {}
                st.rerun()
        with col2:
            if st.button("重置测试"):
                st.session_state.test_started = False
                st.session_state.test_words = pd.DataFrame()
                st.session_state.user_answers = {}
                st.rerun()

        if st.session_state.test_started and not st.session_state.test_words.empty:
            test_words = st.session_state.test_words
            total = len(test_words)
            
            st.subheader(f"本次共 {total} 题，全部答完后提交")
            
            for idx, row in test_words.iterrows():
                st.divider()
                st.subheader(f"题目 {idx+1}")
                st.write(f"**单词：{row['word']}**")
                
                key = f"ans_{idx}"
                # 替换为：手动选择对/错
                ans = st.radio("你是否掌握该单词？", ["对", "错"], key=key, horizontal=True)
                st.session_state.user_answers[key] = ans

            st.divider()
            if st.button("✅ 提交全部答案"):
                score = 0
                df_local = test_df.copy()
                
                for idx, row in test_words.iterrows():
                    user_ans = st.session_state.user_answers.get(f"ans_{idx}", "")
                    
                    st.divider()
                    st.subheader(f"第 {idx+1} 题结果")
                    st.write(f"单词：**{row['word']}** ")
                    st.write(f"你的选择：{user_ans}")
                    
                    # 选择对=测试通过，得分+1；选择错=不通过，错题数+1
                    if user_ans == "对":
                        st.success("测试通过🎉")
                        score += 1
                    else:
                        st.error("测试未通过❌")
                        df_local.loc[df_local["word"] == row["word"], "wrong_count"] += 1
                
                save_func(df_local)
                st.divider()
                st.metric("最终得分", f"{score}/{total}")
                st.session_state.test_started = False

# 6. 学习统计
elif menu == "📊 学习统计":
    st.header("📊 学习数据统计")
    
    # 词库选择
    book_source = st.radio("查看词库", ["自定义记忆库", "一年级预置词库"], horizontal=True)
    
    if book_source == "自定义记忆库":
        stat_df = df
    else:
        stat_df = preset_df

    total_cnt = len(stat_df)
    master_cnt = len(stat_df[stat_df["master"] == 1])
    weak_cnt = len(stat_df[stat_df["master"] == 0])
    wrong_total = stat_df["wrong_count"].sum()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("总生词数", total_cnt)
    with col2:
        st.metric("已掌握", master_cnt)
    with col3:
        st.metric("待复习", weak_cnt)

    st.divider()
    st.subheader("⚠️ 易错单词TOP5")
    hard_words = stat_df.sort_values("wrong_count", ascending=False).head(5)
    st.dataframe(hard_words[["word","meaning","wrong_count"]], use_container_width=True)