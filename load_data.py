import sqlite3
import pandas as pd
import re

def clean_amount(value):
    """Превращает '42 Lac' в 4200000, а '1 Cr' в 10000000"""
    if pd.isna(value) or 'Call' in str(value):
        return None
    
    val = str(value).replace(',', '').strip()
    try:
        num = float(re.findall(r"[-+]?\d*\.\d+|\d+", val)[0])
        if 'Lac' in val:
            return int(num * 100000)
        elif 'Cr' in val:
            return int(num * 10000000)
        return int(num)
    except:
        return None

df = pd.read_csv('house_prices.csv')

df.columns = [c.replace(' ', '_').replace('(', '').replace(')', '') for c in df.columns]

df['Amount_Clean'] = df['Amountin_rupees'].apply(clean_amount)

df['Area_Clean'] = df['Carpet_Area'].str.extract('(\d+)').astype(float)

conn = sqlite3.connect('digital_trace.db')
df.to_sql('houses', conn, if_exists='replace', index=False)

conn.close()