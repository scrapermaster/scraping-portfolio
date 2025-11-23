import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import random
import time
import os

# TECH STACK: undetected-chromedriver (Cloudflare Bypass), Shadow DOM traversal

def get_proxy():
    # Proxy rotation required for IP hygiene
    return os.environ.get('ROTATING_PROXY')

# Helper: Access elements inside Shadow DOM (Closed Shadow Roots)
def get_shadow_element(driver, shadow_host_css, shadow_element_css):
    shadow_host = driver.find_element(By.CSS_SELECTOR, shadow_host_css)
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", shadow_host)
    return shadow_root.find_element(By.CSS_SELECTOR, shadow_element_css)

def run_scraper():
    options = uc.ChromeOptions()
    options.add_argument(f'--user-agent={os.environ.get("USER_AGENT")}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    # Initialize Undetected Chromedriver
    driver = uc.Chrome(options=options, version_main=140)
    driver.maximize_window()

    try:
        driver.get('https://www.mattressfirm.com')
        
        # 1. Handle "Access Denied" or Cloudflare Challenges
        if '<title>Access Denied</title>' in driver.page_source:
            print("Detected. Rotating IP...")
            return

        # 2. Handle Popups (Email Modals)
        try:
            button_close = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[class^=EmailModal_newModal_closeButton]"))
            )
            driver.execute_script("arguments[0].click();", button_close)
        except: pass

        # 3. Store Locator Logic (Input Zip Code)
        # This simulates a user setting their local store to find specific inventory
        store_locator = WebDriverWait(driver, 15).until(
             EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Store locator']"))
        )
        driver.execute_script("arguments[0].click();", store_locator)
        
        # [Additional logic for iterating through zip codes and extracting inventory...]

    finally:
        driver.quit()

if __name__ == "__main__":
    run_scraper()
