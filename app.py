import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json
from datetime import datetime
import time

# --- 1. 設定網頁標題 ---
st.set_page_config(page_title="我的雲端記帳本", page_icon="💰")
st.title("💰 我的雲端記帳本 (Google Sheets 連線版)")

# --- 2. 連接 Google Sheets 的函式 ---
def get_google_sheet():
    # 設定權限範圍 (包含試算表和雲端硬碟)
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # 從 Secrets 讀取鑰匙
    # 注意：這裡對應您在 Streamlit Secrets 填寫的格式
    json_text = st.secrets["service_account"]["service_account_info"]
    creds_dict = json.loads(json_text)
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    
    # 連線並打開試算表
    client = gspread.authorize(creds)
    # 改用 ID 直接抓取，絕對不會錯
    sheet = client.open_by_key("1VzyglFpEC3yS11aloU1YJclw-6Moaewyf8DTR-j7HDc").sheet1
    # 打開您的試算表 (名稱必須完全一樣)

    return sheet

# --- 3. 讀取目前的資料 ---
try:
    sheet = get_google_sheet()
    # 讀取所有資料
    all_records = sheet.get_all_records()
    df = pd.DataFrame(all_records)
except Exception as e:
    # 如果連線失敗，顯示錯誤訊息
    st.error(f"❌ 連線發生錯誤！\n錯誤原因: {e}")
    st.stop()

# --- 4. 輸入介面 ---
col1, col2 = st.columns(2)
with col1:
    date = st.date_input("日期", datetime.today())
with col2:
    category = st.selectbox("類別", ["餐飲", "交通", "購物", "娛樂", "其他"])

item = st.text_input("項目 (例如：午餐)")
amount = st.number_input("金額", min_value=0, step=1)

# --- 5. 按鈕邏輯 (寫入資料) ---
if st.button("🚀 新增一筆"):
    if item and amount > 0:
        with st.spinner('正在寫入雲端...'):
            try:
                # 準備要寫入的資料：轉成字串的日期, 項目, 金額, 類別
                new_data = [str(date), item, amount, category]
                
                # 寫入 Google Sheet
                sheet.append_row(new_data)
                
                st.success(f"✅ 成功！已將「{item} {amount}元」寫入雲端！")
                
                # 休息 1 秒後重新整理，讓表格更新
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"寫入失敗：{e}")
    else:
        st.warning("⚠️ 請輸入項目和金額喔！")

# --- 6. 顯示目前的帳本 ---
st.markdown("---")
st.subheader("📋 目前的帳本紀錄")

# 如果資料表有資料，就顯示出來
if not df.empty:
    st.dataframe(df, use_container_width=True)
    # 計算總花費
    if "金額" in df.columns:
        total_spent = df["金額"].sum()
        st.info(f"💵 累積總花費： **{total_spent} 元**")
else:
    st.write("目前還沒有資料，快來記第一筆吧！")
