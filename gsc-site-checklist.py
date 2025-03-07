import os
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Google Search Console API scope
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

def authenticate_gsc_service_account(service_account_file):
    """Authenticate with Google Search Console API using a service account"""
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES)
    
    return build('webmasters', 'v3', credentials=credentials)

def main():
    # Path to your service account JSON key file
    service_account_file = 'creds.json'
    
    # Authenticate and build the service
    service = authenticate_gsc_service_account(service_account_file)
    
    # List all sites the service account has access to
    sites = service.sites().list().execute()
    
    print("Sites the service account has access to:")
    if 'siteEntry' in sites:
        for site in sites['siteEntry']:
            print(f"- {site['siteUrl']} (Permission level: {site.get('permissionLevel', 'Unknown')})")
    else:
        print("No sites found. The service account doesn't have access to any properties.")
    
    print("\nMake sure to use one of these exact URLs in your data retrieval script.")

if __name__ == "__main__":
    main()