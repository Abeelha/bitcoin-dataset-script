
"""
Bitcoin Price Data Collection Script
Fetches current and historical Bitcoin prices from CoinGecko API
"""

import requests
import pandas as pd
import json
from pathlib import Path
from datetime import datetime, timedelta
import time

class BitcoinDataCollector:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.coin_id = "bitcoin"

    def collect_current_price(self):
        """Fetch current Bitcoin price and market data"""
        url = f"{self.base_url}/simple/price"
        params = {
            'ids': self.coin_id,
            'vs_currencies': 'usd',
            'include_market_cap': 'true',
            'include_24hr_vol': 'true',
            'include_24hr_change': 'true',
            'include_last_updated_at': 'true'
        }

        print("🔍 Fetching current Bitcoin price...")
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return data[self.coin_id]
        else:
            raise Exception(f"Failed to fetch current price: {response.status_code}")

    def collect_historical_prices(self, days=365):
        """Fetch historical Bitcoin prices for specified number of days"""
        url = f"{self.base_url}/coins/{self.coin_id}/market_chart"
        params = {
            'vs_currency': 'usd',
            'days': days,
            'interval': 'daily'
        }

        print(f"📈 Fetching {days} days of historical Bitcoin prices...")
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch historical data: {response.status_code}")

    def process_historical_data(self, raw_data):
        """Process historical market data into clean DataFrame"""


        prices = raw_data['prices']
        market_caps = raw_data['market_caps']
        volumes = raw_data['total_volumes']


        df_prices = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df_market_caps = pd.DataFrame(market_caps, columns=['timestamp', 'market_cap'])
        df_volumes = pd.DataFrame(volumes, columns=['timestamp', 'volume'])


        df = df_prices.merge(df_market_caps, on='timestamp')
        df = df.merge(df_volumes, on='timestamp')


        df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')


        df['price'] = df['price'].round(2)
        df['market_cap'] = df['market_cap'].round(0).astype('int64')
        df['volume'] = df['volume'].round(0).astype('int64')


        df_final = df[['date', 'datetime', 'price', 'market_cap', 'volume']].copy()

        return df_final

    def save_raw_data(self, current_data, historical_data):
        """Save raw API responses"""
        Path("data/raw").mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")


        with open(f"data/raw/current_price_{timestamp}.json", "w") as f:
            json.dump(current_data, f, indent=2)


        with open(f"data/raw/historical_data_{timestamp}.json", "w") as f:
            json.dump(historical_data, f, indent=2)

        print(f"💾 Raw data saved with timestamp {timestamp}")

    def save_processed_data(self, df):
        """Save processed data as CSV"""
        Path("data/processed").mkdir(parents=True, exist_ok=True)

        output_file = "data/processed/bitcoin_prices.csv"
        df.to_csv(output_file, index=False)

        print(f"✅ Processed data saved to {output_file}")
        print(f"📊 Dataset contains {len(df)} daily records")

        return output_file

    def create_datapackage(self, csv_file):
        """Create/update datapackage.json"""


        df = pd.read_csv(csv_file)

        datapackage = {
            "name": "bitcoin-price-data",
            "title": "Bitcoin Price Data",
            "description": "Daily Bitcoin price, market capitalization, and trading volume data from CoinGecko API",
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "contributors": [
                {
                    "title": "Abeelha (Data Package Creator)",
                    "roles": ["creator", "maintainer"]
                }
            ],
            "licenses": [
                {
                    "name": "CC-BY-4.0",
                    "title": "Creative Commons Attribution 4.0 International",
                    "path": "https://creativecommons.org/licenses/by/4.0/"
                }
            ],
            "sources": [
                {
                    "title": "CoinGecko API",
                    "path": "https://api.coingecko.com/api/v3",
                    "description": "Free cryptocurrency price API"
                }
            ],
            "keywords": ["bitcoin", "cryptocurrency", "price", "market-data", "financial"],
            "resources": [
                {
                    "name": "bitcoin-prices",
                    "path": "data/processed/bitcoin_prices.csv",
                    "title": "Bitcoin Daily Prices",
                    "description": "Daily Bitcoin price, market cap, and volume data",
                    "format": "csv",
                    "mediatype": "text/csv",
                    "encoding": "utf-8",
                    "bytes": len(df) * 100,
                    "schema": {
                        "fields": [
                            {
                                "name": "date",
                                "type": "date",
                                "title": "Date",
                                "description": "Date of price data (YYYY-MM-DD)"
                            },
                            {
                                "name": "datetime",
                                "type": "datetime",
                                "title": "DateTime",
                                "description": "Full timestamp of price data"
                            },
                            {
                                "name": "price",
                                "type": "number",
                                "title": "Price (USD)",
                                "description": "Bitcoin price in US Dollars"
                            },
                            {
                                "name": "market_cap",
                                "type": "integer",
                                "title": "Market Capitalization",
                                "description": "Total market capitalization in USD"
                            },
                            {
                                "name": "volume",
                                "type": "integer",
                                "title": "24h Trading Volume",
                                "description": "24-hour trading volume in USD"
                            }
                        ]
                    }
                }
            ]
        }

        with open("datapackage.json", "w") as f:
            json.dump(datapackage, f, indent=2)

        print("📦 datapackage.json created successfully")

def main():
    """Main execution function"""

    print("🚀 Starting Bitcoin Price Data Collection")
    print("=" * 50)

    collector = BitcoinDataCollector()

    try:

        current_data = collector.collect_current_price()
        print(f"💰 Current Bitcoin Price: ${current_data['usd']:,.2f}")


        time.sleep(1)


        historical_data = collector.collect_historical_prices(days=365)


        collector.save_raw_data(current_data, historical_data)


        df_processed = collector.process_historical_data(historical_data)


        csv_file = collector.save_processed_data(df_processed)


        collector.create_datapackage(csv_file)

        print("\n🎉 Data collection completed successfully!")
        print(f"📈 Latest price: ${df_processed.iloc[-1]['price']:,.2f}")
        print(f"📅 Data range: {df_processed.iloc[0]['date']} to {df_processed.iloc[-1]['date']}")


        print("\n🔍 Validating Data Package...")
        try:
            import subprocess
            result = subprocess.run(['frictionless', 'validate', 'datapackage.json'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Data Package validation successful!")
            else:
                print("⚠️  Validation warnings:")
                print(result.stdout)
        except FileNotFoundError:
            print("ℹ️  Install frictionless to validate: pip install frictionless")

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())