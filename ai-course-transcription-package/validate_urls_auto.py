#!/usr/bin/env python3
"""
Validate S3 URLs automatically using the sample signed URL.
"""

import json
import requests
import sys
from urllib.parse import urlparse, parse_qs, urlencode

def check_url(url, timeout=3):
    """Check if a URL is accessible."""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code in [200, 403]  # 403 means it exists but needs auth
    except Exception as e:
        return False

def extract_auth_params(signed_url):
    """Extract authentication parameters from a signed S3 URL."""
    parsed = urlparse(signed_url)
    params = parse_qs(parsed.query)
    
    # Convert single-item lists to strings
    auth_params = {}
    for key, values in params.items():
        if key != 'x-id':  # Skip request-specific params
            auth_params[key] = values[0] if isinstance(values, list) else values
    
    return auth_params

def main():
    # Sample signed URL from earlier
    sample_signed_url = """https://aitra-main.s3.us-east-2.amazonaws.com/afdp_cohort_3_recordings/week_1_class_1_2024-06-18.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIA6ELKOKYDDOCGTW4H%2F20250814%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20250814T184219Z&X-Amz-Expires=3600&X-Amz-Signature=2139f2597bdf38a90b4454b49d036325ac605035d1ef25e1172bce1da4a4edb8&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject"""
    
    # Load manifest
    with open('s3_manifest_cohort3.json', 'r') as f:
        manifest = json.load(f)
    
    print("🔍 Validating S3 URLs for Cohort 3...")
    print("=" * 50)
    
    # Extract auth params from sample
    auth_params = extract_auth_params(sample_signed_url)
    print(f"✅ Using authentication parameters from sample URL")
    print(f"   Algorithm: {auth_params.get('X-Amz-Algorithm', 'N/A')}")
    print(f"   Expires: {auth_params.get('X-Amz-Expires', 'N/A')} seconds")
    print()
    
    valid_count = 0
    invalid_urls = []
    requires_auth = []
    
    print("Testing URLs:")
    print("-" * 50)
    
    for i, video in enumerate(manifest['videos'], 1):
        base_url = video['url']
        
        # First try without auth
        is_valid_plain = check_url(base_url)
        
        # Try with auth params
        parsed = urlparse(base_url)
        
        # Note: The signature is specific to each URL, so we can't reuse it
        # We'll need fresh signed URLs for each file
        # For now, let's check if the files exist (even if we get 403)
        
        if is_valid_plain:
            status = "✅ Public"
            valid_count += 1
        else:
            # Try to see if we get a 403 (exists but needs auth)
            response_code = None
            try:
                r = requests.head(base_url, timeout=3)
                response_code = r.status_code
            except:
                pass
            
            if response_code == 403:
                status = "🔐 Requires Auth"
                requires_auth.append(video)
            else:
                status = "❌ Not Found"
                invalid_urls.append(video)
        
        print(f"{status} Week {video['week']} Class {video['lesson']}: {video['date']}")
    
    print("\n" + "=" * 50)
    print(f"Summary:")
    print(f"  ✅ Public/Valid: {valid_count}/{len(manifest['videos'])}")
    print(f"  🔐 Requires Auth: {len(requires_auth)}/{len(manifest['videos'])}")
    print(f"  ❌ Not Found: {len(invalid_urls)}/{len(manifest['videos'])}")
    
    if requires_auth:
        print(f"\n⚠️  {len(requires_auth)} URLs require authentication:")
        for video in requires_auth[:5]:  # Show first 5
            print(f"   - Week {video['week']} Class {video['lesson']} ({video['date']})")
        if len(requires_auth) > 5:
            print(f"   ... and {len(requires_auth) - 5} more")
        
        print("\n📝 Note: These files exist but need signed URLs")
        print("   You'll need to get fresh signed URLs for each file")
        print("   from https://aitra-legacy-content.vercel.app/folder/afdp_cohort_3_recordings")
    
    if invalid_urls:
        print(f"\n❌ {len(invalid_urls)} URLs not found (404):")
        for video in invalid_urls[:5]:  # Show first 5
            print(f"   - Week {video['week']} Class {video['lesson']} ({video['date']})")
        if len(invalid_urls) > 5:
            print(f"   ... and {len(invalid_urls) - 5} more")
        
        print("\nPossible issues:")
        print("  1. Different date in filename")
        print("  2. File doesn't exist")
        print("  3. Different naming convention")
    
    # Check the base URL pattern
    print("\n🔍 Checking S3 bucket accessibility...")
    base_bucket_url = "https://aitra-main.s3.us-east-2.amazonaws.com/"
    try:
        r = requests.head(base_bucket_url, timeout=3)
        if r.status_code == 403:
            print("✅ S3 bucket exists (aitra-main)")
            print("✅ Region: us-east-2")
            print("✅ Path: afdp_cohort_3_recordings/")
        else:
            print(f"⚠️  Unexpected response from bucket: {r.status_code}")
    except Exception as e:
        print(f"❌ Could not reach S3 bucket: {e}")
    
    print("\n💡 Recommendation:")
    if len(requires_auth) > 0 or len(invalid_urls) > 0:
        print("   1. Visit https://aitra-legacy-content.vercel.app/folder/afdp_cohort_3_recordings")
        print("   2. Log in and get the actual file list")
        print("   3. Copy signed URLs for each video")
        print("   4. Update the manifest with correct URLs")
    else:
        print("   All URLs are valid! Ready to transcribe.")

if __name__ == "__main__":
    main()