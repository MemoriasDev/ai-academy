#!/usr/bin/env python3
"""
Validate S3 URLs and update manifest with signed URLs if needed.
"""

import json
import requests
import sys
from urllib.parse import urlparse, parse_qs

def check_url(url):
    """Check if a URL is accessible."""
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        return response.status_code == 200
    except:
        return False

def extract_base_url(signed_url):
    """Extract base URL from a signed S3 URL."""
    parsed = urlparse(signed_url)
    # Remove query parameters
    base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    return base_url

def main():
    # Load manifest
    with open('s3_manifest_cohort3.json', 'r') as f:
        manifest = json.load(f)
    
    print("🔍 Validating S3 URLs for Cohort 3...")
    print("=" * 50)
    
    valid_count = 0
    invalid_urls = []
    
    # Get sample signed URL parameters from the working example
    sample_url = input("Paste a working signed S3 URL (or press Enter to skip validation): ").strip()
    
    auth_params = {}
    if sample_url:
        parsed = urlparse(sample_url)
        auth_params = parse_qs(parsed.query)
        print(f"\n✅ Extracted authentication parameters from sample URL")
        print(f"   Will apply to all URLs in manifest\n")
    
    for i, video in enumerate(manifest['videos'], 1):
        url = video['url']
        
        # Add auth parameters if we have them
        if auth_params:
            # Build query string from auth params
            query_parts = []
            for key, values in auth_params.items():
                if key not in ['x-id']:  # Skip request-specific params
                    query_parts.append(f"{key}={values[0]}")
            
            # Add query to URL
            if '?' not in url:
                url_with_auth = url + '?' + '&'.join(query_parts)
            else:
                url_with_auth = url + '&' + '&'.join(query_parts)
            
            video['url_with_auth'] = url_with_auth
            is_valid = check_url(url_with_auth)
        else:
            is_valid = check_url(url)
        
        status = "✅" if is_valid else "❌"
        print(f"{status} Week {video['week']} Class {video['lesson']}: {video['date']}")
        
        if is_valid:
            valid_count += 1
        else:
            invalid_urls.append(video)
    
    print("\n" + "=" * 50)
    print(f"Summary: {valid_count}/{len(manifest['videos'])} URLs valid")
    
    if invalid_urls:
        print(f"\n⚠️  {len(invalid_urls)} URLs need attention:")
        for video in invalid_urls:
            print(f"   - Week {video['week']} Class {video['lesson']} ({video['date']})")
        
        print("\nPossible issues:")
        print("1. Files might not exist on S3")
        print("2. Different date format in filename")
        print("3. Authentication required")
        print("\nYou can:")
        print("1. Check the actual S3 bucket for correct filenames")
        print("2. Update the manifest with correct dates/filenames")
        print("3. Add signed URL parameters")
    
    # Save updated manifest if we added auth
    if auth_params:
        with open('s3_manifest_cohort3_signed.json', 'w') as f:
            json.dump(manifest, f, indent=2)
        print(f"\n✅ Saved manifest with authentication: s3_manifest_cohort3_signed.json")

if __name__ == "__main__":
    main()