# Google Search Console Data Retrieval

A Python utility for retrieving 16 months of historical data from Google Search Console using a service account.

## Overview

This script connects to the Google Search Console API and extracts search analytics data for your website across a 16-month period. It handles the API's 3-month data request limitation by automatically splitting requests into appropriate chunks.

## Features

- Authenticates using a service account (no user interaction required)
- Retrieves 16 months of historical data
- Works around the Google Search Console API's 3-month request limitation
- Collects key metrics (clicks, impressions, CTR, position)
- Includes important dimensions (query, page, date, device, country)
- Exports data to a timestamped CSV file
- Suitable for automation and scheduled tasks

## Prerequisites

- Python 3.6 or higher
- A Google Cloud project with the Search Console API enabled
- A service account with access to your Search Console property

## Installation

1. Clone this repository or download the script file:

```bash
git clone https://github.com/juliencoquet/gsc-data-retrieval.git
cd gsc-data-retrieval
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

Or install them directly:

```bash
pip install google-api-python-client google-auth pandas
```

## Setup

### Create a Service Account

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Search Console API for your project
4. Navigate to "IAM & Admin" > "Service Accounts"
5. Click "Create Service Account"
6. Provide a name and description for your service account
7. Assign it the "Search Console API User" role
8. Create a JSON key and download it as `service-account-key.json`
9. Save this file in the same directory as the script

### Add the Service Account to Search Console

1. Go to your [Google Search Console](https://search.google.com/search-console)
2. Select your property
3. Click "Settings" > "Users and permissions"
4. Click "Add user"
5. Enter the service account email address (looks like `name@project-id.iam.gserviceaccount.com`)
6. Select "Owner" or at least "Full" permission level
7. Click "Add"

## Configuration

Edit the script to update these key variables:

```python
# Path to your service account JSON key file
service_account_file = 'service-account-key.json'

# Your Google Search Console site URL (including protocol)
site_url = 'https://your-website.com/'
```

Note: if you are pointing to domain properties, you will need to use the following syntax:
`sc-domain:yourdomain.com`

## Usage

Run the script:

```bash
python gsc-data-retrieval.py
```

The script will:
1. Authenticate with the Google Search Console API
2. Retrieve data in 3-month chunks over a 16-month period
3. Combine all data into a single dataset
4. Save the results to a CSV file named `gsc_data_YYYYMMDD.csv`

## Customization

You can customize the script by modifying these parameters:

- `dimensions`: Adjust which dimensions to retrieve (query, page, date, device, country)
- `row_limit`: Change the number of rows retrieved per request (default 25000)
- `months`: Modify the total months of historical data to retrieve

Example of customizing dimensions:

```python
# Fetch only query and page dimensions
chunk_data = fetch_search_analytics_data(
    service, 
    site_url, 
    date_range['start_date'], 
    date_range['end_date'],
    dimensions=['query', 'page']  # Custom dimensions
)
```
## Checking which domains/sites you have access to based on your credentials
Run the domain/site check script:

```bash
python gsc-site-checklist.py
```
This will output the list of domains/sites your credentials (service account email) have access to. You can pipe the output to a text file and have the export script look through that.

## Schedule Automated Runs

### Using cron (Linux/macOS)

Example cron job to run the script daily at 2 AM:

```
0 2 * * * cd /path/to/script && /usr/bin/python3 gsc-data-retrieval.py >> gsc_log.txt 2>&1
```

### Using Task Scheduler (Windows)

1. Open Task Scheduler
2. Create a new task
3. Set the trigger (e.g., daily at 2 AM)
4. Set the action to start a program:
   - Program/script: `python`
   - Arguments: `C:\path\to\gsc-data-retrieval.py.py`
   - Start in: `C:\path\to\script\directory`

## Troubleshooting

### Common Issues

1. **Authentication Error**: 
   - Make sure your service account key file is in the correct location
   - Verify the service account has the necessary permissions

2. **No Data Returned**:
   - Confirm the site URL matches exactly what's in Search Console
   - Check that the service account has been added to the property

3. **API Quota Exceeded**:
   - Add delay between requests or reduce the frequency of script runs

## License

[MIT License](LICENSE)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgements

- [Google Search Console API Documentation](https://developers.google.com/webmaster-tools)
- [Google API Python Client](https://github.com/googleapis/google-api-python-client)
