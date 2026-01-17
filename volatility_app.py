import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Volatility Estimator",
    layout="wide"
)

# Title and description
st.title(" Multi-Timeframe Volatility Estimator")
st.markdown("""
Analyze stock volatility using multiple methodologies:
**Historical** | **Rolling Windows** | **EWMA** | **Event Analysis**
""")

# Sidebar inputs
st.sidebar.header("Configuration")
symbol = st.sidebar.text_input("Stock Ticker", value="AAPL", max_chars=10).upper()
years = st.sidebar.slider("Years of Data", min_value=1, max_value=5, value=3)

# Fetch button
if st.sidebar.button(" Analyze", type="primary"):
    
    with st.spinner(f"Fetching {symbol} data..."):
        try:
            # Download data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=years*365)
            
            data = yf.download(symbol, start=start_date, end=end_date, progress=False)
            
            if len(data) == 0:
                st.error(f"No data found for {symbol}. Check the ticker symbol.")
                st.stop()
            
            # Calculate returns
            df = data[['Close']].copy()
            df.columns = ['Price']
            df['Daily_Return'] = np.log(df['Price'] / df['Price'].shift(1))
            df = df.dropna()
            
            # Calculate volatilities
            # 1. Historical
            hist_vol = df['Daily_Return'].std() * np.sqrt(252)
            
            # 2. Rolling windows
            for window in [20, 60, 120]:
                df[f'Vol_{window}d'] = df['Daily_Return'].rolling(window=window).std() * np.sqrt(252)
            
            # 3. EWMA
            df['Vol_EWMA'] = df['Daily_Return'].ewm(alpha=0.06, adjust=False).std() * np.sqrt(252)
            
            df_clean = df.dropna()
            
            # Store in session state
            st.session_state['df'] = df_clean
            st.session_state['symbol'] = symbol
            st.session_state['hist_vol'] = hist_vol
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.stop()

# Display results if data exists
if 'df' in st.session_state:
    df = st.session_state['df']
    symbol = st.session_state['symbol']
    hist_vol = st.session_state['hist_vol']
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    latest = df.iloc[-1]
    
    with col1:
        st.metric("Historical Vol", f"{hist_vol*100:.2f}%")
    with col2:
        st.metric("20-Day Vol", f"{latest['Vol_20d']*100:.2f}%")
    with col3:
        st.metric("60-Day Vol", f"{latest['Vol_60d']*100:.2f}%")
    with col4:
        st.metric("EWMA Vol", f"{latest['Vol_EWMA']*100:.2f}%")
    
    # Main chart
    st.subheader(f"{symbol} Volatility Analysis")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df['Vol_20d']*100,
        mode='lines',
        name='20-Day',
        line=dict(width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df['Vol_60d']*100,
        mode='lines',
        name='60-Day',
        line=dict(width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df['Vol_120d']*100,
        mode='lines',
        name='120-Day',
        line=dict(width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df['Vol_EWMA']*100,
        mode='lines',
        name='EWMA',
        line=dict(width=3, color='red')
    ))
    
    fig.update_layout(
        title=f"{symbol} Multi-Timeframe Volatility",
        xaxis_title="Date",
        yaxis_title="Annualized Volatility (%)",
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Two column layout
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Volatility Regime")
        
        current_vol = latest['Vol_60d'] * 100
        median_vol = df['Vol_60d'].median() * 100
        
        if current_vol > median_vol * 1.3:
            st.error(f" HIGH VOLATILITY: {current_vol:.2f}% (median: {median_vol:.2f}%)")
            st.write("Elevated risk environment. Consider reducing position sizes.")
        elif current_vol < median_vol * 0.7:
            st.success(f" LOW VOLATILITY: {current_vol:.2f}% (median: {median_vol:.2f}%)")
            st.write("Calm market conditions. Potential for volatility selling strategies.")
        else:
            st.info(f" NORMAL VOLATILITY: {current_vol:.2f}% (median: {median_vol:.2f}%)")
            st.write("Typical market conditions.")
    
    with col_right:
        st.subheader("Risk Metrics")
        
        current_price = latest['Price']
        daily_vol = df['Daily_Return'].std()
        
        st.write(f"**Current Price:** ${current_price:.2f}")
        st.write(f"**Daily Expected Move:** ±${current_price * daily_vol:.2f} ({daily_vol*100:.2f}%)")
        
        annual_vol = latest['Vol_60d']
        upper_1yr = current_price * np.exp(annual_vol)
        lower_1yr = current_price * np.exp(-annual_vol)
        
        st.write(f"**1-Year Expected Range (68% confidence):**")
        st.write(f"High: ${upper_1yr:.2f} | Low: ${lower_1yr:.2f}")
    
    # Data table
    st.subheader("Latest Values")
    display_df = df[['Price', 'Vol_20d', 'Vol_60d', 'Vol_120d', 'Vol_EWMA']].tail(10).copy()
    display_df['Vol_20d'] = display_df['Vol_20d'] * 100
    display_df['Vol_60d'] = display_df['Vol_60d'] * 100
    display_df['Vol_120d'] = display_df['Vol_120d'] * 100
    display_df['Vol_EWMA'] = display_df['Vol_EWMA'] * 100
    
    display_df.columns = ['Price ($)', '20-Day Vol (%)', '60-Day Vol (%)', '120-Day Vol (%)', 'EWMA Vol (%)']
    st.dataframe(display_df.style.format({
        'Price ($)': '{:.2f}',
        '20-Day Vol (%)': '{:.2f}',
        '60-Day Vol (%)': '{:.2f}',
        '120-Day Vol (%)': '{:.2f}',
        'EWMA Vol (%)': '{:.2f}'
    }), use_container_width=True)

else:
    st.info(" Enter a stock ticker and click 'Analyze' to get started!")
    
    st.markdown("""
    ### How to use:
    1. Enter a stock ticker (e.g., AAPL, TSLA, SPY)
    2. Select how many years of data to analyze
    3. Click 'Analyze' to generate the report
    
    ### What you'll get:
    - **Historical Volatility**: Overall baseline volatility
    - **Rolling Windows**: 20/60/120-day volatility trends
    - **EWMA**: Shock-weighted volatility (reacts faster to events)
    - **Regime Analysis**: Current market risk environment
    - **Risk Metrics**: Expected price ranges
    """)

# Footer
st.markdown("---")
st.markdown("Built with Python, Streamlit, and yfinance | Data from Yahoo Finance")