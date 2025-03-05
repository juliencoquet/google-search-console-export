import os
import pandas as pd
import json
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Google Search Console API scope
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

def authenticate_gsc_service_account(service_account_file):
    """Authenticate with Google Search Console API using a service account"""
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES)
    
    # Create delegated credentials if needed (for domain-wide delegation)
    # If you've set up domain-wide delegation, uncomment and use this:
    # delegated_credentials = credentials.with_subject('user@yourdomain.com')
    # return build('webmasters', 'v3', credentials=delegated_credentials)
    
    return build('webmasters', 'v3', credentials=credentials)

def get_date_ranges(months=16):
    """Generate 3-month chunks for the past 16 months from today"""
    end_date = datetime.today()
    date_ranges = []
    
    for i in range(0, months, 3):
        chunk_end = end_date - timedelta(days=i*30)
        
        # Handle the last chunk potentially being shorter than 3 months
        chunk_length = min(3, months - i)
        chunk_start = chunk_end - timedelta(days=chunk_length*30)
        
        date_ranges.append({
            'start_date': chunk_start.strftime('%Y-%m-%d'),
            'end_date': chunk_end.strftime('%Y-%m-%d')
        })
    
    return date_ranges

def fetch_search_analytics_data(service, site_url, start_date, end_date, 
                              dimensions=['query', 'page', 'date', 'device', 'country'],
                              row_limit=25000):
    """Fetch data from Google Search Console for a specific date range"""
    
    request = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': dimensions,
        'rowLimit': row_limit,
        'startRow': 0
    }
    
    response = service.searchanalytics().query(siteUrl=site_url, body=request).execute()
    
    if 'rows' not in response:
        return pd.DataFrame()
    
    # Process the response into a DataFrame
    rows_list = []
    for row in response['rows']:
        row_data = {}
        
        # Add dimension data
        for i, dimension in enumerate(dimensions):
            row_data[dimension] = row['keys'][i]
        
        # Add metrics
        row_data['clicks'] = row['clicks']
        row_data['impressions'] = row['impressions']
        row_data['ctr'] = row['ctr']
        row_data['position'] = row['position']
        
        rows_list.append(row_data)
    
    return pd.DataFrame(rows_list)

def main():
    # Path to your service account JSON key file
    service_account_file = 'service-account-key.json'
    
    # Your Google Search Console site URL (including protocol, e.g., https://example.com/)
    site_url = 'https://your-website.com/'
    
    # Authenticate and build the service
    service = authenticate_gsc_service_account(service_account_file)
    
    # Get date ranges for the past 16 months in 3-month chunks
    date_ranges = get_date_ranges(16)
    
    # Initialize an empty DataFrame to store all data
    all_data = pd.DataFrame()
    
    # Fetch data for each date range
    for date_range in date_ranges:
        print(f"Fetching data from {date_range['start_date']} to {date_range['end_date']}...")
        
        chunk_data = fetch_search_analytics_data(
            service, 
            site_url, 
            date_range['start_date'], 
            date_range['end_date']
        )
        
        # Append to the full dataset
        if not chunk_data.empty:
            all_data = pd.concat([all_data, chunk_data], ignore_index=True)
            print(f"Retrieved {len(chunk_data)} rows of data")
        else:
            print("No data retrieved for this period")
    
    # Save the complete dataset
    timestamp = datetime.now().strftime("%Y%m%d")
    output_file = f"gsc_data_{timestamp}.csv"
    all_data.to_csv(output_file, index=False)
    
    print(f"Data retrieval complete! Total rows: {len(all_data)}")
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()
