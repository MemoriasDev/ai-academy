#!/usr/bin/env python3
"""
Authentication handler for accessing password-protected course recordings.
Supports both Selenium and Playwright for robust authentication.
"""

import json
import os
import time
from typing import Dict, Optional, List
from urllib.parse import urlparse, urljoin
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthHandler:
    """Handle authentication and session management for protected content."""
    
    def __init__(self, base_url: str = "https://aitra-legacy-content.vercel.app/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.driver = None
        self.authenticated = False
        
    def load_credentials(self, credentials_path: str = "../config/credentials.json") -> Dict[str, str]:
        """Load authentication credentials from JSON file."""
        try:
            with open(credentials_path, 'r') as f:
                credentials = json.load(f)
            return credentials
        except FileNotFoundError:
            logger.error(f"Credentials file not found: {credentials_path}")
            # Create template credentials file
            template = {
                "username": "YOUR_USERNAME",
                "password": "YOUR_PASSWORD",
                "note": "Replace with actual credentials"
            }
            with open(credentials_path, 'w') as f:
                json.dump(template, f, indent=2)
            logger.info(f"Created template credentials file: {credentials_path}")
            raise ValueError("Please update credentials file with actual values")
    
    def setup_selenium_driver(self, headless: bool = True) -> webdriver.Chrome:
        """Setup Chrome WebDriver with optimal settings."""
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument("--headless")
        
        # Optimization flags
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(30)
            return driver
        except WebDriverException as e:
            logger.error(f"Failed to setup Chrome driver: {e}")
            raise
    
    def authenticate_selenium(self, username: str, password: str) -> bool:
        """Authenticate using Selenium WebDriver."""
        try:
            self.driver = self.setup_selenium_driver()
            logger.info(f"Navigating to {self.base_url}")
            
            self.driver.get(self.base_url)
            
            # Wait for login form to load
            wait = WebDriverWait(self.driver, 10)
            
            # Find username field (adjust selectors based on actual form)
            username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
            password_field = self.driver.find_element(By.NAME, "password")
            
            # Fill in credentials
            username_field.clear()
            username_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(password)
            
            # Submit form
            submit_button = self.driver.find_element(By.TYPE, "submit")
            submit_button.click()
            
            # Wait for successful login (adjust based on actual redirect/content)
            time.sleep(3)
            
            # Check if login was successful by looking for expected content
            if "dashboard" in self.driver.current_url.lower() or "cohort" in self.driver.page_source.lower():
                logger.info("Authentication successful!")
                
                # Extract cookies for requests session
                self._extract_session_cookies()
                self.authenticated = True
                return True
            else:
                logger.error("Authentication failed - unexpected page content")
                return False
                
        except TimeoutException:
            logger.error("Timeout waiting for login form")
            return False
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return False
    
    def _extract_session_cookies(self):
        """Extract cookies from Selenium session to requests session."""
        if self.driver:
            for cookie in self.driver.get_cookies():
                self.session.cookies.set(cookie['name'], cookie['value'])
            logger.info("Session cookies extracted successfully")
    
    def discover_video_urls(self) -> Dict[str, List[str]]:
        """Discover all available video URLs organized by cohort."""
        if not self.authenticated:
            logger.error("Must authenticate before discovering URLs")
            return {}
        
        video_urls = {}
        
        try:
            # Navigate through cohort pages to find video links
            for cohort_num in range(2, 7):  # Cohorts 2-6
                cohort_key = f"cohort_{cohort_num}"
                video_urls[cohort_key] = []
                
                # Try to find cohort-specific pages
                cohort_url = urljoin(self.base_url, f"cohort-{cohort_num}")
                
                if self.driver:
                    self.driver.get(cohort_url)
                    time.sleep(2)
                    
                    # Find all video links (adjust selectors based on actual HTML)
                    video_elements = self.driver.find_elements(By.TAG_NAME, "video")
                    video_elements.extend(self.driver.find_elements(By.CSS_SELECTOR, "a[href*='.mp4']"))
                    video_elements.extend(self.driver.find_elements(By.CSS_SELECTOR, "a[href*='.webm']"))
                    
                    for element in video_elements:
                        video_url = element.get_attribute('src') or element.get_attribute('href')
                        if video_url:
                            video_urls[cohort_key].append(video_url)
                
                logger.info(f"Found {len(video_urls[cohort_key])} videos for {cohort_key}")
        
        except Exception as e:
            logger.error(f"Error discovering video URLs: {e}")
        
        return video_urls
    
    def download_video(self, video_url: str, output_path: str) -> bool:
        """Download a video file using authenticated session."""
        try:
            # Use requests session with cookies from Selenium
            response = self.session.get(video_url, stream=True)
            response.raise_for_status()
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            logger.info(f"Downloaded: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to download {video_url}: {e}")
            return False
    
    def save_session_manifest(self, video_urls: Dict[str, List[str]], output_path: str = "../config/video_manifest.json"):
        """Save discovered video URLs to JSON manifest."""
        try:
            with open(output_path, 'w') as f:
                json.dump(video_urls, f, indent=2)
            logger.info(f"Video manifest saved: {output_path}")
        except Exception as e:
            logger.error(f"Failed to save manifest: {e}")
    
    def cleanup(self):
        """Clean up resources."""
        if self.driver:
            self.driver.quit()
        self.session.close()

def main():
    """Test authentication and discovery."""
    auth = AuthHandler()
    
    try:
        # Load credentials
        credentials = auth.load_credentials()
        
        # Authenticate
        if auth.authenticate_selenium(credentials['username'], credentials['password']):
            
            # Discover videos
            video_urls = auth.discover_video_urls()
            
            # Save manifest
            auth.save_session_manifest(video_urls)
            
            print("Authentication and discovery completed successfully!")
            print(f"Found videos for {len(video_urls)} cohorts")
            
        else:
            print("Authentication failed!")
            
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        auth.cleanup()

if __name__ == "__main__":
    main()
