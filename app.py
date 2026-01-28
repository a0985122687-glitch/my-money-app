import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📈 我的股票分析助理")

# 輸入框
ticker = st.text_input("請輸入股票代碼 (台股請加 .TW)", value="2330.TW")

# 選擇日期範圍
days = st.slider("顯示天數", min_value=10, max_value=365, value=100)

# 抓取資料
data = yf.download(ticker, period=f"{days}d")

if not data.empty:
    # 顯示收盤價折線圖
    st.subheader(f"{ticker} 最近 {days} 天走勢")
    st.line_chart(data['Close'])
    
    # 顯示數據表格
    st.subheader("最新數據摘要")
    st.write(data.tail())
else:
    st.error("找不到這檔股票，請確認代碼是否輸入正確。")
