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
data = {
    'Date': pd.to_datetime(np.random.choice(dates, n_records)),
    'Product': np.random.choice(['Laptop', 'Desktop', 'Tablet', 'Phone', 'Accessories'], n_records),
    'Sales Amount': np.random.uniform(100, 5000, n_records).round(2),
    'Opportunity Status': np.random.choice(['Won', 'Lost', 'Pending'], n_records, p=[0.7, 0.2, 0.1]),
    'Customer': [f'Customer_{i}' for i in np.random.randint(1, 101, n_records)]
}

# Create DataFrame
df = pd.DataFrame(data)

# Sort by date
df = df.sort_values('Date')

# Calculate Total Sales
df['Total Sales'] = df.groupby('Date')['Sales Amount'].transform('sum')

# Save to CSV
df.to_csv('Sales Dataset.csv', index=False, date_format='%Y-%m-%d')

print("Sample sales dataset has been created successfully!") 