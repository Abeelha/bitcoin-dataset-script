#!/usr/bin/env python3
"""
Bitcoin Price Visualization - Fixed Version
Creates interactive charts from the processed Bitcoin data
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from pathlib import Path
import json

def load_data():
    """Load the processed Bitcoin data"""
    try:
        df = pd.read_csv("data/processed/bitcoin_prices.csv")
        df['date'] = pd.to_datetime(df['date'])
        df['datetime'] = pd.to_datetime(df['datetime'])
        return df
    except FileNotFoundError:
        print("❌ Error: Bitcoin price data not found. Run the collector script first.")
        return None

def create_simple_price_chart(df):
    """Create a simple price chart"""

    fig = go.Figure()

    # Add price line
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['price'],
            mode='lines',
            name='Bitcoin Price',
            line=dict(color='orange', width=2),
            hovertemplate='<b>$%{y:,.2f}</b><br>%{x}<extra></extra>'
        )
    )

    # Update layout
    fig.update_layout(
        title='Bitcoin Price Over Time',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        height=600,
        showlegend=False
    )

    return fig

def create_volume_chart(df):
    """Create trading volume chart"""

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['volume'],
            name='24h Volume',
            marker_color='lightblue',
            hovertemplate='<b>$%{y:,.0f}</b><br>%{x}<extra></extra>'
        )
    )

    fig.update_layout(
        title='Bitcoin 24h Trading Volume',
        xaxis_title='Date',
        yaxis_title='Volume (USD)',
        height=400,
        showlegend=False
    )

    return fig

def create_summary_stats(df):
    """Create summary statistics"""

    current_price = df.iloc[-1]['price']
    min_price = df['price'].min()
    max_price = df['price'].max()
    avg_price = df['price'].mean()

    stats = {
        'Current Price': f'${current_price:,.2f}',
        'Year High': f'${max_price:,.2f}',
        'Year Low': f'${min_price:,.2f}',
        'Average Price': f'${avg_price:,.2f}',
        'Price Range': f'${max_price - min_price:,.2f}'
    }

    return stats

def create_html_report(price_fig, volume_fig, stats):
    """Create HTML report with charts"""

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bitcoin Price Report</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
            .stat-box {{ text-align: center; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
            .chart {{ margin: 20px 0; }}
        </style>
    </head>
    <body>
        <h1>🪙 Bitcoin Price Report</h1>
        <p>Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M UTC')}</p>

        <div class="stats">
    """

    for label, value in stats.items():
        html_content += f"""
            <div class="stat-box">
                <h3>{value}</h3>
                <p>{label}</p>
            </div>
        """

    html_content += """
        </div>

        <div class="chart">
            <div id="price-chart"></div>
        </div>

        <div class="chart">
            <div id="volume-chart"></div>
        </div>

        <script>
    """

    html_content += f"""
            var priceConfig = {price_fig.to_json()};
            Plotly.newPlot('price-chart', priceConfig.data, priceConfig.layout, {{responsive: true}});

            var volumeConfig = {volume_fig.to_json()};
            Plotly.newPlot('volume-chart', volumeConfig.data, volumeConfig.layout, {{responsive: true}});
        </script>
    </body>
    </html>
    """

    return html_content

def main():
    """Main visualization function"""

    print("📊 Creating Bitcoin Price Visualizations...")

    # Load data
    df = load_data()
    if df is None:
        return 1

    # Create output directory
    Path("visualizations").mkdir(exist_ok=True)

    # Create charts
    print("📈 Creating price chart...")
    price_fig = create_simple_price_chart(df)

    print("📊 Creating volume chart...")
    volume_fig = create_volume_chart(df)

    print("📋 Calculating statistics...")
    stats = create_summary_stats(df)

    # Save individual charts
    price_fig.write_html("visualizations/bitcoin_price_chart.html")
    volume_fig.write_html("visualizations/bitcoin_volume_chart.html")

    # Create report
    print("📄 Creating HTML report...")
    report_html = create_html_report(price_fig, volume_fig, stats)

    with open("visualizations/bitcoin_report.html", "w") as f:
        f.write(report_html)

    print("✅ Visualizations created successfully!")
    print("📁 Available files:")
    print("   - visualizations/bitcoin_report.html (Main report)")
    print("   - visualizations/bitcoin_price_chart.html")
    print("   - visualizations/bitcoin_volume_chart.html")

    # Print stats to console
    print("\n📊 Bitcoin Statistics:")
    for label, value in stats.items():
        print(f"   {label}: {value}")

    return 0

if __name__ == "__main__":
    exit(main())