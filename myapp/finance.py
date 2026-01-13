# import yfinance as yf
# msft = yf.Ticker("ADANIPORTS")
# print(msft.info)
from datetime import datetime, timedelta

#
#         Company name      Symbol
# 0  Adani Enterprises    ADANIENT
# 1  Adani Ports & SEZ  ADANIPORTS
# 2   Apollo Hospitals  APOLLOHOSP
# 3       Asian Paints  ASIANPAINT
# 4          Axis Bank    AXISBANK
# import pandas as pd
# import requests
#
# url = "https://en.wikipedia.org/wiki/NIFTY_50"
# headers = {"User-Agent": "Mozilla/5.0"}
#
# response = requests.get(url, headers=headers)
# tables = pd.read_html(response.text)
#
# # Print all table headers to see what's inside
# for i, table in enumerate(tables):
#     print(f"Table {i} columns:", table.columns)
#
# # Usually NIFTY 50 is at index 1 or 0:
# nifty = tables[1] if 'Symbol' in tables[1].columns else tables[0]
# print("\n✅ Found table columns:", nifty.columns)
#
# # Now display only the company + symbol columns dynamically
# cols = [c for c in nifty.columns if 'Company' in c or 'Symbol' in c]
# print(nifty[cols].head())
#
#
import yfinance as yf
import pandas as pd



def get_stock_data(symbol):
    try:
        print('hrr')
        stock = yf.Ticker(f"MSFT")
        # Get last 1 hour data with 1-minute intervals for more frequent updates
        end_date = datetime.now()
        start_date = end_date - timedelta(days=5,hours=1)
        df = stock.history(start=start_date, end=end_date, interval='1m')

        if df.empty:
            print('empty data')
            return None

        # Calculate simple moving average for prediction
        df['MA20'] = df['Close'].rolling(window=20).mean()

        # Convert timestamps to string format
        df.index = df.index.strftime('%Y-%m-%d %H:%M:%S')

        cleaned_data = {
            'timestamps': df.index.tolist(),
            'actual': clean_data(df['Close']),
            'predicted': clean_data(df['MA20']),
            'volume': clean_data(df['Volume']),
            'time': datetime.now().strftime('%H:%M:%S')
        }

        for i,j in cleaned_data.items():
            print(i)
            print(j)
            print("+++++++++++++++++++++++++++++++++++++++++++++")

        return cleaned_data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return None

def clean_data(series):
    """Clean data by replacing NaN with None and converting numpy types to native Python types"""
    return [float(x) if pd.notnull(x) else None for x in series]

get_stock_data('symbol')
