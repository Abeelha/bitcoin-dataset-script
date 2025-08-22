# 🪙 Bitcoin Price Data Package

An automated Data Package for collecting, processing, and visualizing Bitcoin price data using the Frictionless Data standard.

![Bitcoin](https://img.shields.io/badge/Bitcoin-F7931A?style=for-the-badge&logo=bitcoin&logoColor=white)
![Data Package](https://img.shields.io/badge/Data%20Package-007ACC?style=for-the-badge&logo=data&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 📊 Dataset Overview

This Data Package provides comprehensive Bitcoin market data including:

- **Daily price data** (USD)
- **Market capitalization**
- **24-hour trading volume**
- **Historical trends** (1 year lookback)

Data is automatically collected from the [CoinGecko API](https://api.coingecko.com/) and follows the [Frictionless Data Package](https://datapackage.org/) standard.

## 🚀 Quick Start

### Prerequisites

```bash
pip install -r scripts/requirements.txt
```

### Data Collection

```bash
# Collect Bitcoin price data
python scripts/collect_bitcoin_data.py

# Generate visualizations
python scripts/create_visualizations.py
```

### Validation

```bash
# Validate the Data Package
frictionless validate datapackage.json
```

## 📁 Project Structure

```
bitcoin-price-datapackage/
├── datapackage.json              # Data Package descriptor
├── README.md                     # This file
├── data/
│   ├── raw/                     # Raw API responses
│   │   ├── current_price_*.json
│   │   └── historical_data_*.json
│   └── processed/               # Cleaned CSV data
│       └── bitcoin_prices.csv   # Main dataset
├── scripts/
│   ├── collect_bitcoin_data.py  # Data collection script
│   ├── create_visualizations.py # Visualization generator
│   └── requirements.txt         # Python dependencies
└── visualizations/
    ├── bitcoin_dashboard.html   # Interactive dashboard
    ├── bitcoin_price_chart.html # Price & volume chart
    ├── bitcoin_market_cap.html  # Market cap chart
    └── bitcoin_gauge.html       # Current price gauge
```

## 📈 Data Schema

| Field        | Type     | Description                        |
| ------------ | -------- | ---------------------------------- |
| `date`       | date     | Date of price data (YYYY-MM-DD)    |
| `datetime`   | datetime | Full timestamp with time           |
| `price`      | number   | Bitcoin price in USD               |
| `market_cap` | integer  | Total market capitalization in USD |
| `volume`     | integer  | 24-hour trading volume in USD      |

## 🎨 Visualizations

The package includes several interactive visualizations:

1. **📊 Main Dashboard** (`bitcoin_dashboard.html`)

   - Combined price, volume, and market cap charts
   - Key statistics and metrics
   - Real-time price gauge

2. **📈 Price Chart** (`bitcoin_price_chart.html`)

   - Daily price trends
   - Trading volume overlay

3. **💰 Market Cap Chart** (`bitcoin_market_cap.html`)

   - Market capitalization over time

4. **⏱️ Price Gauge** (`bitcoin_gauge.html`)
   - Current price vs yearly range

## 🔄 Automation

### Manual Updates

```bash
python scripts/collect_bitcoin_data.py
python scripts/create_visualizations.py
```

### Scheduled Updates

#### Using Cron (Linux/Mac)

```bash
# Add to crontab for daily updates at 9 AM
0 9 * * * cd /path/to/bitcoin-price-datapackage && python scripts/collect_bitcoin_data.py
```

#### Using GitHub Actions

Create `.github/workflows/update-data.yml`:

```yaml
name: Update Bitcoin Data
on:
  schedule:
    - cron: "0 9 * * *" # Daily at 9 AM UTC
  workflow_dispatch:

jobs:
  update-data:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.9"
      - name: Install dependencies
        run: pip install -r scripts/requirements.txt
      - name: Collect data
        run: python scripts/collect_bitcoin_data.py
      - name: Create visualizations
        run: python scripts/create_visualizations.py
      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add -A
          git commit -m "Update Bitcoin data $(date)" || exit 0
          git push
```

## 📊 Data Sources

- **CoinGecko API**: https://api.coingecko.com/api/v3
  - Free tier: 10-30 calls/minute
  - No API key required
  - Comprehensive cryptocurrency data

## 🔍 Data Quality

### Validation Checks

- ✅ Schema validation with Frictionless
- ✅ Data type verification
- ✅ Missing value handling
- ✅ Timestamp consistency
- ✅ Price range validation

### Error Handling

- Network timeout handling
- API rate limit respect
- Data consistency checks
- Graceful error recovery

## 📄 License

This Data Package is made available under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

### Data Sources License

- CoinGecko API data is used under their [Terms of Service](https://www.coingecko.com/en/terms)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run validation: `frictionless validate datapackage.json`
5. Submit a pull request

## 📞 Support

- **Issues**: Create an issue on GitHub
- **Data Package Spec**: https://datapackage.org/
- **CoinGecko API**: https://www.coingecko.com/en/api

## 🏷️ Version History

- **v1.0.0**: Initial release with daily price collection and basic visualizations

---

_Created as part of the Datopian tech onboarding process - turning awesome data into Frictionless Data Packages! 🚀_
