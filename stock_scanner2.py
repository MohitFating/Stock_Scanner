#!/usr/bin/env python
# coding: utf-8

# In[2]:


import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Function to get stock data and analyze for lifetime high and price appreciation
def analyze_stocks(stock_symbols, analysis_period='10y', appreciation_threshold=20):
    results = []
    today = datetime.now()
    start_date = today - timedelta(days=3650)  # 10 years ago

    for symbol in stock_symbols:
        print(f"Analyzing {symbol}...")
        stock_data = yf.Ticker(symbol)

        # Fetch historical data
        hist = stock_data.history(period=analysis_period)
        
        if hist.empty:
            print(f"No data available for {symbol}. Skipping.")
            continue
        
        # Calculate the lifetime high
        lifetime_high = hist['Close'].max()
        high_date = hist['Close'].idxmax()  # Date when the high occurred

        # Find the price after reaching the lifetime high
        price_after_high = hist.loc[high_date:].tail(1)['Close'].values[0]

        # Calculate price appreciation
        price_appreciation = ((price_after_high - lifetime_high) / lifetime_high) * 100

        # Check if the price after the high appreciated significantly
        if price_appreciation >= appreciation_threshold:
            results.append({
                'Ticker': symbol,
                'Lifetime High': lifetime_high,
                'Date of High': high_date.date(),
                'Price After High': price_after_high,
                'Price Appreciation (%)': price_appreciation,
            })

    return results

# Function to summarize the results
def summarize_results(results):
    total_opportunities = len(results)
    annual_opportunities = total_opportunities / 10  # Assuming analysis over 10 years
    successful_opportunities = len([r for r in results if r['Price Appreciation (%)'] > 0])
    success_rate = (successful_opportunities / total_opportunities) * 100 if total_opportunities > 0 else 0

    print("\nSummary of Results:")
    print(f"Total Opportunities: {total_opportunities}")
    print(f"Annual Opportunities: {annual_opportunities:.2f}")
    print(f"Success Rate: {success_rate:.2f}%")
    print("Detailed Results:")
    
    for result in results:
        print(result)

# List of stock symbols to analyze
stock_symbols = ['AAPL', 'TSLA', 'GOOGL', 'AMZN', 'MSFT', 'NFLX']  # Add your own list of stocks

# Run the analysis with a lower appreciation threshold
results = analyze_stocks(stock_symbols, analysis_period='10y', appreciation_threshold=10)


# Summarize results
summarize_results(results)


# In[ ]:




