import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Generate dates
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)
dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days)]

# Create sample data
n_records = 1000

# Marketing channels
channels = ['Social Media', 'Email', 'Search Ads', 'Display Ads', 'Content Marketing']
regions = ['North', 'South', 'East', 'West', 'Central']
campaign_types = ['Brand Awareness', 'Lead Generation', 'Conversion', 'Retention']

data = {
    'Date': pd.to_datetime(np.random.choice(dates, n_records)),
    'Marketing_Channel': np.random.choice(channels, n_records),
    'Region': np.random.choice(regions, n_records),
    'Campaign_Type': np.random.choice(campaign_types, n_records),
    'Impressions': np.random.randint(1000, 100000, n_records),
    'Clicks': np.random.randint(10, 2000, n_records),
    'Cost': np.random.uniform(100, 5000, n_records).round(2),
    'Leads': np.random.randint(1, 50, n_records),
    'Conversions': np.random.randint(0, 20, n_records)
}

# Create DataFrame
df = pd.DataFrame(data)

# Calculate derived metrics
df['CTR'] = (df['Clicks'] / df['Impressions'] * 100).round(2)  # Click-through rate
df['CPC'] = (df['Cost'] / df['Clicks']).round(2)  # Cost per click
df['CPL'] = (df['Cost'] / df['Leads']).round(2)  # Cost per lead
df['Conversion_Rate'] = (df['Conversions'] / df['Leads'] * 100).round(2)  # Conversion rate

# Sort by date
df = df.sort_values('Date')

# Save to CSV
df.to_csv('Marketing Dataset.csv', index=False, date_format='%Y-%m-%d')

print("Marketing dataset has been created successfully!")
print("\nDataset includes the following metrics:")
print("- Basic metrics: Impressions, Clicks, Cost, Leads, Conversions")
print("- Calculated metrics: CTR (%), CPC ($), CPL ($), Conversion Rate (%)")
print("- Dimensions: Marketing Channel, Region, Campaign Type")
print(f"\nTotal records: {len(df)}") 