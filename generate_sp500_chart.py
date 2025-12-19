import pandas as pd
import plotly.graph_objects as go
from fredapi import Fred
import os

# FRED API key - you'll need to set this as a GitHub secret
fred = Fred(api_key=os.environ.get('FRED_API_KEY'))

# Fetch S&P 500 data
sp500 = fred.get_series('SP500')
sp500_df = sp500.to_frame(name='SP500')
sp500_df.index.name = 'Date'
sp500_df.reset_index(inplace=True)

# Create Plotly figure
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=sp500_df['Date'],
    y=sp500_df['SP500'],
    mode='lines',
    name='S&P 500',
    line=dict(color='#1f77b4', width=2)
))

fig.update_layout(
    title='S&P 500 Index',
    xaxis_title='Date',
    yaxis_title='Index Value',
    hovermode='x unified',
    template='plotly_white',
    height=600
)

# Save as HTML
fig.write_html('index.html', include_plotlyjs='cdn')