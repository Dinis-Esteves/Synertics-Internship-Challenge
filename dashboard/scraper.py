import os
import pandas as pd
import requests
from datetime import datetime
from io import BytesIO
import django
import sys
import logging

def log(message):
    logger.info(message)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("scraper.log", "a") as f:
        f.write(f"[{timestamp}] {message}\n")


logger = logging.getLogger(__name__)
from dashboard.models import FuturesPrice
print(f"Initial DB count: {FuturesPrice.objects.count()} records")

def download_todays_excel() -> pd.DataFrame:
    today = datetime.now().strftime('%Y%m%d')
    url = f"https://www.enexgroup.gr/documents/20126/314344/{today}_DER_DOL_EN_v01.xlsx"
    print(f"Fetching today's data from: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises exception for bad status
        return pd.read_excel(BytesIO(response.content), engine="openpyxl")
    except Exception as e:
        print(f"Download failed: {str(e)}")
        return None

def save_all_contracts(df: pd.DataFrame):
    if df is None:
        return
        
    print("\nFound columns:", df.columns.tolist())
    print(f"\nProcessing {len(df)} rows...")
    
    for index, row in df.iterrows():
        try:
            product = str(row.get("Instrument ", "")).strip()
            avg_price = float(row.get("Average Price of Orders ", 0))

            if avg_price != 0:
                print(f"Row {index}: {product} = {avg_price}")
                
                obj, created = FuturesPrice.objects.update_or_create(
                    date=datetime.now().date(),
                    product_name=product,
                    defaults={'average_price': avg_price}
                )
                print(f"{'Created' if created else 'Updated'}: {product}")
                
        except Exception as e:
            print(f"Error on row {index}: {str(e)}")
            continue

def run_scraper():
    log("=== Starting scrape ===")
    today_df = download_todays_excel()

    if today_df is not None:
        save_all_contracts(today_df)
        product_names = today_df["Instrument "].dropna().unique()
        total = len(product_names)
        log("Scraping successful.")
        return {
            "status": "success",
            "date": str(datetime.now().date()),
            "products": list(product_names),
            "count": total
        }
    else:
        log("Scraping failed.")
        log("Failed to download today's data.")
        raise Exception("Failed to download today's data.")
