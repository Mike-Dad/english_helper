import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime

# 数据文件
DATA_FILE = "english_words.csv"

# 初始化数据
def init_data():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=[
            "word", "unit", "meaning", "sentence",
            "add_time", "master", "wrong_count"
        ])
        df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")

# 读取单词库
def load_words():
    return pd.read_csv(DATA_FILE, encoding="utf-8-sig")

# 保存单词库
def save_words(df):
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")

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

init_data()
df = load_words()

# 侧边栏导航
menu = st.sidebar.radio(
    "功能菜单",
    ["📝 添加生词", "📚 单词记忆库", "🃏 背诵卡片","🧪 随机小测试", "📊 学习统计"]
)

# 1. 添加生词
if menu == "📝 添加生词":
    st.header("📝 录入新单词")
    with st.form("word_form"):
        word = st.text_input("英文单词")
        unit = st.text_input("单元（选填）")
        meaning = st.text_input("中文释义")
        sentence = st.text_input("简单例句（儿童短句）")
        submitted = st.form_submit_button("保存到记忆库")

    if submitted:
        if word.strip() and meaning.strip():
            new_row = {
                "word": word.strip(),
                "unit": unit.strip(),
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
            st.warning("请填写单词和释义")

# 2. 单词记忆库 + 编辑/删除功能
elif menu == "📚 单词记忆库":
    st.header("📚 单词记忆库 & 在线编辑")
    st.info("支持修改单词、释义、单元、例句，也可删除不需要的单词")

    # 可编辑表格
    edit_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic"
    )

    # 保存编辑内容
    if st.button("💾 保存修改内容"):
        save_words(edit_df)
        st.success("✅ 单词表修改已保存！")
        # 刷新数据
        df = load_words()

    st.divider()
    # 单独删除指定单词
    st.subheader("🗑️ 删除单个单词")
    if len(df) > 0:
        del_word = st.selectbox("选择要删除的单词", df["word"].tolist())
        if st.button("确认删除"):
            df = df[df["word"] != del_word].reset_index(drop=True)
            save_words(df)
            st.success(f"✅ 已删除单词：{del_word}")
    else:
        st.info("暂无单词可删除")

    st.divider()
    # 导出
    st.download_button(
        label="📥 导出单词表",
        data=edit_df.to_csv(index=False, encoding="utf-8-sig"),
        file_name="儿童英语生词表.csv",
        mime="text/csv"
    )

# 3. 背诵卡片 【新增核心模块】
elif menu == "🃏 背诵卡片":
    st.header("🃏 单词卡片背诵")
    mode = st.radio("背诵范围", ["全部单词", "仅未掌握单词"], horizontal=True)

    # 筛选卡片列表
    if mode == "仅未掌握单词":
        card_df = df[df["master"] == 0].reset_index(drop=True)
    else:
        card_df = df.reset_index(drop=True)

    if len(card_df) == 0:
        st.info("暂无需要背诵的单词～")
    else:
        # 重置卡片列表
        if not st.session_state.card_list or len(st.session_state.card_list) != len(card_df):
            st.session_state.card_list = card_df.index.tolist()
            random.shuffle(st.session_state.card_list)
            st.session_state.card_idx = 0
            st.session_state.show_chinese = False

        # 当前单词
        now_idx = st.session_state.card_list[st.session_state.card_idx]
        row = card_df.loc[now_idx]

        # 卡片样式
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

        # 卡片正反面
        if not st.session_state.show_chinese:
            st.markdown(f"""
            <div class="card">
                <h2>{row['word']}</h2>
                <p style="color:#666;">{row['unit']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="card">
                <h2>{row['word']}</h2>
                <p style="color:#666;">{row['unit']}</p>
                <hr>
                <h3 style="color:#2E86AB;">{row['meaning']}</h3>
                <p style="color:#888;">{row['sentence']}</p>
            </div>
            """, unsafe_allow_html=True)

        # 功能按钮
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
        # 掌握标记
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ 标记为已掌握"):
                df.loc[df["word"] == row["word"], "master"] = 1
                save_words(df)
                st.success(f"【{row['word']}】已标记掌握")
                st.rerun()
        with c2:
            if st.button("❌ 标记为薄弱"):
                df.loc[df["word"] == row["word"], "master"] = 0
                save_words(df)
                st.warning(f"【{row['word']}】设为薄弱词")
                st.rerun()

        st.caption(f"进度：{st.session_state.card_idx+1} / {len(st.session_state.card_list)}")

# 4. 自动小测试
elif menu == "🧪 随机小测试":
    st.header("🧪 生词小测验")
    if len(df) == 0:
        st.info("记忆库暂无单词，请先添加生词")
    else:
        test_num = st.slider("本次出题数量", 3, 15, 5)
        start_test = st.button("开始测试")

        if start_test:
            test_words = df.sample(min(test_num, len(df))).reset_index(drop=True)
            score = 0
            total = len(test_words)

            for idx, row in test_words.iterrows():
                st.divider()
                st.subheader(f"题目 {idx+1}")
                st.write(f"**单词：{row['word']}**")
                ans = st.text_input(f"请写出中文释义 #{idx+1}", key=f"ans_{idx}")

                if ans.strip() == row["meaning"].strip():
                    st.success("答对啦🎉")
                    score += 1
                elif ans.strip():
                    st.error(f"答错啦，正确答案：{row['meaning']}")
                    df.loc[df["word"] == row["word"], "wrong_count"] += 1

            st.divider()
            st.metric("本次得分", f"{score}/{total}")
            save_words(df)

# 5. 学习统计
elif menu == "📊 学习统计":
    st.header("📊 学习数据统计")
    total_cnt = len(df)
    wrong_total = df["wrong_count"].sum()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("已收录生词总数", total_cnt)
    with col2:
        st.metric("累计错题次数", wrong_total)

    st.subheader("易错单词TOP5")
    hard_words = df.sort_values("wrong_count", ascending=False).head(5)
    st.dataframe(hard_words[["word","meaning","wrong_count"]], use_container_width=True)