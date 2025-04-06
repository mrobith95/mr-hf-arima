from datetime import datetime, timedelta
import pandas as pd

def find_missing_dates(data):

    # Create full date range
    full_range = pd.date_range(start=data['Date'].min(), end=data['Date'].max(), freq='D')

    # Dates completely missing from the data
    missing_dates = set(full_range) - set(data['Date'])

    # Dates where Price is NaN
    missing_price_dates = data[data['Open'].isna()]['Date']

    # detecting if there is a sunday or saturday that has open price
    # Add a column for the day of the week (0 = Monday, 6 = Sunday)
    data['Weekday'] = data['Date'].dt.weekday

    # Filter for Saturdays (5) and Sundays (6) with non-null price
    weekend_with_price = data[(data['Weekday'] >= 5) & (data['Open'].notna())]

    # Check if any such rows exist
    if not weekend_with_price.empty:
        ada_minggu = True
    else:
        ada_minggu = False

    return sorted(missing_dates.union(missing_price_dates)), ada_minggu
