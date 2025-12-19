import pandas as pd
import plotly.graph_objects as go
from fredapi import Fred
import os

# FRED API key
fred = Fred(api_key=os.environ.get('FRED_API_KEY'))

# Fetch S&P 500 data
sp500 = fred.get_series('SP500')
sp500_df = sp500.to_frame(name='SP500')
sp500_df.index.name = 'Date'
sp500_df.reset_index(inplace=True)

# Create Plotly figure with light mode
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

# Create HTML with dark mode toggle
html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>S&P 500 Chart</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: Arial, sans-serif;
            transition: background-color 0.3s ease;
        }}
        body.light-mode {{
            background-color: #ffffff;
            color: #000000;
        }}
        body.dark-mode {{
            background-color: #111111;
            color: #ffffff;
        }}
        .toggle-container {{
            text-align: right;
            margin-bottom: 10px;
        }}
        .toggle-btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: background-color 0.3s ease;
        }}
        .light-mode .toggle-btn {{
            background-color: #333;
            color: #fff;
        }}
        .dark-mode .toggle-btn {{
            background-color: #fff;
            color: #333;
        }}
        .toggle-btn:hover {{
            opacity: 0.8;
        }}
        #chart {{
            width: 100%;
            height: 600px;
        }}
    </style>
</head>
<body class="light-mode">
    <div class="toggle-container">
        <button class="toggle-btn" onclick="toggleTheme()">🌙 Dark Mode</button>
    </div>
    <div id="chart"></div>
    
    <script>
        var lightLayout = {{
            title: 'S&P 500 Index',
            xaxis: {{title: 'Date'}},
            yaxis: {{title: 'Index Value'}},
            hovermode: 'x unified',
            template: 'plotly_white',
            height: 600,
            paper_bgcolor: '#ffffff',
            plot_bgcolor: '#ffffff',
            font: {{color: '#000000'}}
        }};
        
        var darkLayout = {{
            title: 'S&P 500 Index',
            xaxis: {{title: 'Date'}},
            yaxis: {{title: 'Index Value'}},
            hovermode: 'x unified',
            template: 'plotly_dark',
            height: 600,
            paper_bgcolor: '#111111',
            plot_bgcolor: '#111111',
            font: {{color: '#ffffff'}}
        }};
        
        var data = {data};
        
        var currentTheme = 'light';
        
        // Initialize chart
        Plotly.newPlot('chart', data, lightLayout, {{responsive: true}});
        
        function toggleTheme() {{
            var body = document.body;
            var btn = document.querySelector('.toggle-btn');
            
            if (currentTheme === 'light') {{
                body.className = 'dark-mode';
                btn.textContent = '☀️ Light Mode';
                Plotly.relayout('chart', darkLayout);
                currentTheme = 'dark';
                localStorage.setItem('theme', 'dark');
            }} else {{
                body.className = 'light-mode';
                btn.textContent = '🌙 Dark Mode';
                Plotly.relayout('chart', lightLayout);
                currentTheme = 'light';
                localStorage.setItem('theme', 'light');
            }}
        }}
        
        // Load saved theme preference
        window.onload = function() {{
            var savedTheme = localStorage.getItem('theme');
            if (savedTheme === 'dark') {{
                toggleTheme();
            }}
        }}
    </script>
</body>
</html>
"""

# Convert figure data to JSON
import json
data_json = json.dumps(fig.data, cls=plotly.utils.PlotlyJSONEncoder)

# Write HTML file
with open('index.html', 'w') as f:
    f.write(html_template.format(data=data_json))