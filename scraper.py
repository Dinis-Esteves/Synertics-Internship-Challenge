import os
import pandas as pd
import requests
from datetime import datetime
from io import BytesIO
import django
import sys

# Setup Django environment
sys.path.append(".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "futures_dashboard.settings")
django.setup()

from dashboard.models import FuturesPrice
print(f"Initial DB count: {FuturesPrice.objects.count()} records")

def download_specific_date() -> pd.DataFrame:
    fixed_date = datetime(2025, 4, 30)
    url = f"https://www.enexgroup.gr/documents/20126/314344/{fixed_date.strftime('%Y%m%d')}_DER_DOL_EN_v01.xlsx"
    print(f"Fetching data for April 30, 2025 from: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        # Read specific sheet (DOL_Derivatives is sheet 1)
        df = pd.read_excel(BytesIO(response.content), sheet_name=1, engine="openpyxl")
        print(f"Successfully downloaded {len(df)} rows")
        return df
    except Exception as e:
        print(f"Download failed: {str(e)}")
        return None

def save_all_instruments(df: pd.DataFrame):
    if df is None:
        print("No data to process")
        return
        
    # Clean column names (remove spaces and make lowercase)
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    print("\nAvailable columns:", df.columns.tolist())
    
    target_date = datetime(2025, 4, 30).date()
    saved_count = 0
    
    for index, row in df.iterrows():
        try:
            instrument = str(row['instrument']).strip()
            
            # Get average price (try different possible columns)
            avg_price = None
            for col in ['average_price_of_orders', 'average_price_of_trades_(vwap)', 'fixing_prices']:
                if pd.notna(row.get(col)):
                    avg_price = float(row[col])
                    break
            
            if avg_price is None:
                print(f"Skipping {instrument} - no valid price data")
                continue
                
            print(f"Processing: {instrument} @ {avg_price}")
            
            obj, created = FuturesPrice.objects.update_or_create(
                date=target_date,
                product_name=instrument,
                defaults={'average_price': avg_price}
            )
            saved_count += 1
            status = "Created" if created else "Updated"
            print(f"{status}: {instrument} = {avg_price}")
            
        except Exception as e:
            print(f"Error on row {index}: {str(e)}")
            continue
    
    print(f"\nSuccessfully saved/updated {saved_count} records")
    print(f"Final DB count: {FuturesPrice.objects.count()} records")

if __name__ == "__main__":
    print("\n=== Starting scrape for April 30, 2025 ===")
    df = download_specific_date()
    if df is not None:
        save_all_instruments(df)
    print("=== Done ===")