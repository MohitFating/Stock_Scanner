#!/usr/bin/env python
# coding: utf-8

# In[5]:


import yfinance as yf
import pandas as pd
from datetime import datetime

# Function to get stock data
def get_stock_data(stock_symbol, period):
    stock_data = yf.Ticker(stock_symbol)
    hist = stock_data.history(period=period)
    return hist

# Function to analyze stocks for lifetime highs and price appreciation
def analyze_stocks(stock_symbols, analysis_period='10y', appreciation_threshold=2):  # Reduce threshold to 2%
    summary = {
        'Total Opportunities': 0,
        'Annual Opportunities': 0.0,
        'Success Rate': 0.0,
    }
    detailed_results = []
    
    for stock in stock_symbols:
        print(f"Analyzing {stock}...")
        hist = get_stock_data(stock, analysis_period)

        if len(hist) == 0:
            print(f"No data available for {stock}.")
            continue

        # Get the lifetime high and its date
        lifetime_high = hist['Close'].max()
        high_date = hist['Close'].idxmax().date()
        
        # Current price to compare for appreciation
        current_price = hist['Close'].iloc[-1]
        
        # Log the current and lifetime high for debugging
        print(f"Lifelong High: {lifetime_high}, Current Price: {current_price}")

        # Check for price appreciation
        if current_price >= lifetime_high * (1 + appreciation_threshold / 100):
            price_appreciation = ((current_price - lifetime_high) / lifetime_high) * 100
            detailed_results.append({
                'Ticker': stock,
                'Lifetime High': round(lifetime_high, 2),
                'Date of High': high_date,
                'Price After High': round(current_price, 2),
                'Price Appreciation (%)': round(price_appreciation, 2)
            })
            summary['Total Opportunities'] += 1

    # Calculate annual opportunities and success rate
    if detailed_results:
        summary['Annual Opportunities'] = summary['Total Opportunities'] / (datetime.now().year - (datetime.now().year - 10))
        summary['Success Rate'] = (summary['Total Opportunities'] / len(stock_symbols)) * 100

    return summary, detailed_results

# List of stock symbols to analyze
stock_symbols = ['AAPL', 'TSLA', 'GOOGL', 'AMZN', 'MSFT', 'NFLX']  # Add your own list of stocks

# Run the analysis
summary, detailed_results = analyze_stocks(stock_symbols, analysis_period='10y', appreciation_threshold=5)

# Print summary
print("\nSummary of Results:")
print(f"Total Opportunities: {summary['Total Opportunities']}")
print(f"Annual Opportunities: {summary['Annual Opportunities']:.2f}")
print(f"Success Rate: {summary['Success Rate']:.2f}%")


# In[ ]:




