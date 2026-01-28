import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 設定頁面
st.set_page_config(page_title="台股買賣策略助理", layout="wide")
st.title("🇹🇼 台股波段買賣決策助手")

# 側邊欄：台股輸入優化
st.sidebar.header("搜尋設定")
stock_id = st.sidebar.text_input("輸入台股代碼", value="2330")
market = st.sidebar.selectbox("市場類型", ["上市 (.TW)", "上櫃 (.TWO)"])
suffix = ".TW" if market == "上市 (.TW)" else ".TWO"
full_ticker = f"{stock_id}{suffix}"

# 抓取資料
data = yf.download(full_ticker, period="1y")

if not data.empty:
    # 計算台股常用的 MA5 (週線) 與 MA20 (月線)
    data['MA5'] = data['Close'].rolling(window=5).mean()
    data['MA20'] = data['Close'].rolling(window=20).mean()
    
    # 取得最新一筆數據
    latest_price = data['Close'].iloc[-1]
    ma5_now = data['MA5'].iloc[-1]
    ma20_now = data['MA20'].iloc[-1]

    # --- 戰略儀表板 ---
    st.subheader(f"📊 {full_ticker} 戰略分析")
    c1, c2, c3 = st.columns(3)
    c1.metric("當前股價", f"{latest_price:.2f}")
    c2.metric("5日均價 (MA5)", f"{ma5_now:.2f}")
    c3.metric("20日均價 (MA20)", f"{ma20_now:.2f}")

    # --- 買賣訊號判斷 ---
    st.divider()
    if ma5_now > ma20_now:
        st.success("🟢 目前狀態：【多方佔優】（黃金交叉中）")
        st.info("💡 買賣建議：趨勢向上，若回測 MA5 不破可考慮進場或續抱。")
    else:
        st.error("🔴 目前狀態：【空方佔優】（死亡交叉中）")
        st.warning("💡 買賣建議：短期走勢偏弱，建議觀望，直到股價重新站回月線(MA20)。")

    # --- 互動 K 線圖 ---
    fig = go.Figure(data=[go.Candlestick(
        x=data.index, open=data['Open'], high=data['High'],
        low=data['Low'], close=data['Close'], name='K線'
    )])
    fig.add_trace(go.Scatter(x=data.index, y=data['MA5'], line=dict(color='blue', width=1.5), name='5日線'))
    fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], line=dict(color='orange', width=1.5), name='20日線'))
    
    fig.update_layout(height=600, title=f"{full_ticker} 技術走勢圖", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error(f"無法取得 {full_ticker} 的資料，請確認代碼與市場類型是否正確。")
