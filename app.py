import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json
from datetime import datetime
import time

# --- 網頁設定 ---
st.set_page_config(page_title="記帳本偵錯模式", page_icon="🐞")
st.title("🐞 記帳本連線偵錯模式")

# --- 定義試算表 ID (這是您的檔案身分證) ---
# 請確認這串號碼跟您網址列上的一模一樣
SHEET_ID = "1VzyglFpEC3yS11aloU1YJclw-6Moaewyf8DTR-j7HDc"

def get_google_sheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # 讀取 Secrets
    json_text = st.secrets["service_account"]["service_account_info"]
    creds_dict = json.loads(json_text)
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    
    # 顯示機器人身分 (關鍵！)
    st.info(f"🤖 **機器人正在使用這個 Email 連線：**\n\n`{creds.service_account_email}`")
    st.info(f"📂 **機器人正在嘗試開啟這個 ID：**\n\n`{SHEET_ID}`")
    
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).sheet1
    return sheet

# --- 主程式邏輯 ---
try:
    st.write("---")
    st.write("正在嘗試連線...")
    sheet = get_google_sheet()
    st.success("🎉 **恭喜！連線成功！找不到檔案的問題解決了！**")
    
    # 讀取資料測試
    records = sheet.get_all_records()
    df = pd.DataFrame(records)
    st.write("目前資料預覽：")
    st.dataframe(df)

except Exception as e:
    st.error(f"❌ 連線失敗！\n錯誤訊息: {e}")
    st.warning("""
    **💡 如果看到上面的機器人 Email 跟您共用的不一樣：**
    1. 請複製上面顯示的藍色 Email 地址。
    2. 回到 Google 試算表 -> 右上角「共用」。
    3. 把舊的機器人刪掉，重新貼上這個新的 Email，並設為「編輯者」。
    4. 回來這裡按 Rerun。
    """)
