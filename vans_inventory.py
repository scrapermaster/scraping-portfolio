from browserforge.fingerprints import Screen
from camoufox.sync_api import Camoufox
from datetime import date, datetime, timedelta
import json
import pymysql
import random
import sys
import time
import os

# Anti-Bot Config: Camoufox used for TLS/Fingerprint spoofing
# to bypass PerimeterX protections on the target site.

def get_proxy():
    # Placeholder for proxy rotation logic
    proxies = [os.environ.get('PROXY_1'), os.environ.get('PROXY_2')]     
    return random.choice(proxies)

def execute_sequence_with_browser():
    # Initialize Camoufox with Geolocation and Proxy support
    with Camoufox(
        headless=False,
        geoip=True,
        proxy={"server": get_proxy()}
        ) as browser:
        
        page = browser.new_page()
        page.goto('https://www.vans.com/en-us/c/shop-5000?sort=whatsNew', wait_until="domcontentloaded")

        # Logic to extract total product count from raw HTML
        html_content = page.content()
        # [Extraction logic omitted for brevity...]
        
        next_page = 1
        while True:
            try:
                # Wait for critical elements to load to avoid bot detection triggers
                page.wait_for_selector("a[data-test-id='product-card-title']", timeout=180000)
                product_cards = page.query_selector_all("div[data-test-id='product-card']")
                
                for card in product_cards:
                    # Extracting Model/Price Data
                    title_element = card.query_selector("a[data-test-id='product-card-title']")
                    if not title_element: continue
                        
                    model = title_element.text_content().strip()
                    # [Database Insertion Logic Placeholder]
                    print(f"Scraped: {model}")

                # Pagination Logic: locating the 'View More' button via XPath
                selectors = [
                    "xpath=//a[contains(@href, 'shop-5000?sort=whatsNew&page="+str(next_page)+"')]",
                    "xpath=//a[.//span[contains(text(), 'View More')]]"
                ]
                
                # Human-like interaction: Scroll into view before clicking
                for selector in selectors:
                    element = page.locator(selector)
                    if element.count() > 0:
                        element.scroll_into_view_if_needed()
                        element.click(timeout=180000)
                        page.wait_for_load_state('networkidle')
                        next_page += 1
                        break
                            
            except Exception as e:
                print(f"Error or End of List: {e}")
                break
    
        browser.close() 

if __name__ == "__main__":
    execute_sequence_with_browser()
