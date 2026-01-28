import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="股票策略助手", layout="wide")
st.title("📈 股票買賣決策助手")

# 1. 輸入設定
ticker = st.sidebar.text_input("請輸入代碼 (台股加 .TW)", value="2330.TW")
period = st.sidebar.selectbox("分析區間", ["3mo", "6mo", "1y", "2y"], index=2)

# 2. 抓取數據
data = yf.download(ticker, period=period)

if not data.empty:
    # 3. 計算技術指標
    data['MA5'] = data['Close'].rolling(window=5).mean()
    data['MA20'] = data['Close'].rolling(window=20).mean()
    
    # 獲取最新狀態
    current_price = data['Close'].iloc[-1]
    last_ma5 = data['MA5'].iloc[-1]
    last_ma20 = data['MA20'].iloc[-1]
    
    # 4. 顯示買賣建議 (邏輯判斷)
    st.subheader("🤖 AI 策略建議")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("當前股價", f"{current_price:.2f}")
    
    with col2:
        if last_ma5 > last_ma20:
            st.success("黃金交叉 (看多)")
            st.write("💡 建議：短期走勢強於長期，適合持股或分批佈局。")
        else:
            st.error("死亡交叉 (看空)")
            st.write("💡 建議：短期走勢轉弱，應注意風險，不宜追高。")

    # 5. 繪製專業 K 線圖
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'], high=data['High'],
                low=data['Low'], close=data['Close'], name='K線')])
    
    fig.add_trace(go.Scatter(x=data.index, y=data['MA5'], line=dict(color='blue', width=1), name='5日均線'))
    fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], line=dict(color='orange', width=1), name='20日均線'))
    
    fig.update_layout(title=f"{ticker} 走勢與均線分析", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("找不到資料！台股請記得加 .TW (例如 2330.TW)")
