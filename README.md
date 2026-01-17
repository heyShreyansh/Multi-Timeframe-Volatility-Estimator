#  Multi-Timeframe Volatility Estimator

A quantitative finance analytics tool that estimates, visualizes, and interprets stock price volatility across multiple time horizons.  
Built using Python, Streamlit, Plotly, and Yahoo Finance data, this project bridges financial theory, statistical modeling, and product-grade dashboards.
<img width="1680" height="926" alt="Screenshot 2026-01-17 at 1 59 37 PM" src="https://github.com/user-attachments/assets/878664ac-a754-4f18-8fb7-7bd9cf9ee6ae" />

---

##  What This Project Does

This tool helps answer questions like:
- Is the market currently calm or risky?
- Is volatility rising or mean-reverting?
- What price range should I expect over the next day or year?
- How does short-term volatility compare to long-term risk?

It does this using:
- Historical volatility
- Rolling window volatility (20 / 60 / 120 days)
- EWMA (Exponentially Weighted Moving Average)
- Volatility regime detection
- Risk metrics & confidence intervals

---

##  Methodology

- **Returns**: Log returns for statistical stability  
- **Annualization**: √252 trading days  
- **Rolling Windows**: Capture short, medium, and long-term dynamics  
- **EWMA (α = 0.06)**: Reacts faster to market shocks  
- **Regime Detection**:
  - High Volatility → > 1.3 × historical median  
  - Low Volatility → < 0.7 × historical median  
  - Normal otherwise  

---

##  Interactive Dashboard (Streamlit)

Run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

##  Dashboard Walkthrough

### 1. Landing Page & Configuration
Explains how to select a stock, choose data range, and run the analysis.

### 2. Volatility Summary Metrics
Displays Historical, 20-Day, 60-Day, and EWMA volatility for instant risk assessment.

### 3. Multi-Timeframe Volatility Chart
Compares short-term, medium-term, long-term, and shock-weighted volatility trends.

### 4. Volatility Regime Detection
Classifies market conditions into LOW / NORMAL / HIGH volatility regimes.

### 5. Risk Metrics
Shows expected daily move and 1-year price range with 68% confidence.

### 6. Latest Values Table
Provides recent prices and volatility values for transparency and validation.

---

##  Quant-Style CLI Report

The project also generates a terminal-style volatility report including:
- Volatility snapshot
- Regime analysis
- Trend comparison
- Risk metrics
- Historical extremes
- Methodology notes

---

##  Project Structure

```
volatility-estimator/
├── app.py
├── requirements.txt
├── notebooks/
│   └── Volatility_Estimator.ipynb
├── assets/
│   ├── dashboard.png
│   ├── chart.png
│   ├── regime.png
│   ├── risk_metrics.png
│   └── cli_report.png
└── README.md
```

---

##  Tech Stack

- Python
- pandas, numpy
- yfinance
- plotly
- streamlit
- Jupyter Notebook

---

##  Use Cases

- Options traders → volatility & premium estimation  
- Risk managers → regime monitoring  
- Portfolio managers → cross-asset risk comparison  
- Researchers → volatility dynamics & event studies  

---

<img width="1680" height="928" alt="Screenshot 2026-01-17 at 1 54 58 PM" src="https://github.com/user-attachments/assets/e6c380e9-afdd-4b10-ba2d-6b5bedbcb8c6" />

<img width="1678" height="929" alt="Screenshot 2026-01-17 at 1 55 19 PM" src="https://github.com/user-attachments/assets/8db3ea25-c78b-4c38-9658-bbe5f1dc5134" />


