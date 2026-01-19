import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json
import time
from datetime import datetime

# --- 網頁設定 ---
st.set_page_config(page_title="我的雲端記帳本", page_icon="💰")
st.title("💰 我的雲端記帳本")

# --- 連線設定 ---
def get_sheet():
    # 讀取 Secrets 裡的鑰匙
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    json_text = st.secrets["service_account"]["service_account_info"]
    creds = Credentials.from_service_account_info(json.loads(json_text), scopes=scope)
    client = gspread.authorize(creds)
    
    # 直接連線到您的試算表 (使用您提供的 ID)
    sheet_url = "https://docs.google.com/spreadsheets/d/1VzyglFpEC3yS11aloU1YJclw-6Moaewyf8DTR-j7HDc/edit"
    return client.open_by_url(sheet_url).sheet1

# --- 主程式 ---
try:
    sheet = get_sheet()
    
    # 建立輸入表單
    with st.form("accounting_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        date = col1.date_input("日期", datetime.today())
        category = col2.selectbox("類別", ["餐飲", "交通", "購物", "娛樂", "生活", "其他"])
        item = st.text_input("項目 (例如：午餐、捷運)")
        amount = st.number_input("金額", min_value=0, step=1)
        
        submitted = st.form_submit_button("💰 記一筆")
        
        if submitted and amount > 0:
            # 寫入 Google Sheet
            sheet.append_row([str(date), item, amount, category])
            st.success(f"✅ 成功儲存：{item} ${amount}")
            time.sleep(1)
            st.rerun()
            
    # 顯示最近的記帳紀錄
    st.write("---")
    st.subheader("📋 最近的收支紀錄")
    data = sheet.get_all_records()
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.info("目前還沒有資料，快來記第一筆吧！")

except Exception as e:
    st.error("連線發生錯誤！")
    st.write(f"錯誤原因：{e}")
