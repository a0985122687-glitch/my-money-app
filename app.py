import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json
from datetime import datetime
import time

# --- 設定頁面 ---
st.set_page_config(page_title="我的雲端記帳本", page_icon="💰")
st.title("💰 我的雲端記帳本 (Google Sheets 連線版)")

# --- 連接 Google Sheets 的函式 ---
def get_google_sheet():
    # 設定權限範圍
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    
    # 從 Secrets 讀取鑰匙
    # 這裡會去抓你在 Streamlit 後台設定的 service_account_info
    json_text = st.secrets["service_account"]["service_account_info"]
    creds_dict = json.loads(json_text)
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    
    # 連線並打開試算表
    client = gspread.authorize(creds)
    
    # ⚠️ 這裡的名字符合你剛剛建立的試算表名稱
    sheet = client.open("我的記帳app").sheet1 
    return sheet

# --- 讀取資料 ---
try:
    sheet = get_google_sheet()
    # 讀取所有資料
    all_records = sheet.get_all_records()
    df = pd.DataFrame(all_records)
except Exception as e:
    st.error(f"❌ 連線失敗！請檢查 Secrets 設定或試算表名稱。\n錯誤訊息: {e}")
    st.stop()

# --- 輸入介面 ---
col1, col2 = st.columns(2)
with col1:
    date = st.date_input("日期", datetime.today())
with col2:
    category = st.selectbox("類別", ["餐飲", "交通", "購物", "娛樂", "其他"])

item = st.text_input("項目 (例如：午餐)")
amount = st.number_input("金額", min_value=0, step=1)

# --- 按鈕邏輯 ---
if st.button("🚀 新增一筆"):
    if item and amount > 0:
        with st.spinner('正在寫入雲端...'):
            # 準備要寫入的資料
            # 注意：這裡的日期轉成字串，方便 Excel 閱讀
            new_data = [str(date), item, amount, category]
            
            # 寫入 Google Sheet (加在最後一行)
            sheet.append_row(new_data)
            
            st.success(f"✅ 成功！已將「{item} {amount}元」寫入雲端！")
            
            # 休息一下再重整，讓資料同步
            time.sleep(1)
            st.rerun()
    else:
        st.warning("⚠️ 請輸入項目和金額喔！")

# --- 顯示目前的帳本 ---
st.markdown("---")
st.subheader("📋 目前的帳本紀錄")

if not df.empty:
    # 顯示表格
    st.dataframe(df, use_container_width=True)
    
    # 簡單統計
    total_spent = df["金額"].sum()
    st.info(f"💵 累積總花費： **{total_spent} 元**")
else:
    st.write("目前還沒有資料，快來記第一筆吧！")
