
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="我的專業記帳本", page_icon="💰")

if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['日期', '項目', '金額', '類別'])

st.title("💰 我的專業記帳本 (永久版)")
st.info("👋 歡迎來到永久部署版本！資料會暫存於此，若重新整理頁面資料會重置，請記得下載備份。")

with st.sidebar:
    st.header("📝 新增紀錄")
    date = st.date_input("日期")
    item = st.text_input("項目")
    amount = st.number_input("金額", min_value=0, step=10)
    category = st.selectbox("類別", ['餐飲', '交通', '購物', '娛樂', '固定支出', '其他'])
    
    if st.button("新增一筆", type="primary"):
        if item and amount > 0:
            new_data = pd.DataFrame([{'日期': date, '項目': item, '金額': amount, '類別': category}])
            st.session_state.expenses = pd.concat([st.session_state.expenses, new_data], ignore_index=True)
            st.success("✅ 已新增！")
        else:
            st.error("⚠️ 請輸入項目與金額")

    st.markdown("---")
    uploaded_file = st.file_uploader("📂 上傳舊帳本 (CSV)")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.expenses = df
            st.success("讀取成功！")
        except:
            st.error("檔案格式錯誤")

tab1, tab2 = st.tabs(["📋 帳本清單", "📊 圓餅圖分析"])
with tab1:
    st.dataframe(st.session_state.expenses, use_container_width=True)
    if not st.session_state.expenses.empty:
        csv = st.session_state.expenses.to_csv(index=False).encode('utf-8-sig')
        st.download_button("💾 下載帳本備份", csv, 'my_expenses.csv', 'text/csv')

with tab2:
    if not st.session_state.expenses.empty:
        fig, ax = plt.subplots()
        # 為了永久版相容性，簡單處理字型
        cat_sum = st.session_state.expenses.groupby('類別')['金額'].sum()
        ax.pie(cat_sum, labels=cat_sum.index, autopct='%1.1f%%', startangle=90)
        st.pyplot(fig)
    else:
        st.info("👈 請先新增資料")
