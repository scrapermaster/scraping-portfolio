import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# GOAL: Automate messaging without triggering "Bot detected" flags.
# STRATEGY: Emulate human delays, mouse clicks, and scroll behavior.

def human_login(driver):
    driver.get('https://www.peerspace.com/')
    
    # 1. Click Log In (using JS to bypass overlay issues, but mimicking click)
    signin_button = driver.find_element(By.LINK_TEXT, "Log In")
    driver.execute_script("arguments[0].click();", signin_button)
    
    # 2. Enter Credentials
    signin_input = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "signin-email"))
    )
    signin_input.clear()
    signin_input.send_keys(os.environ.get('PEERSPACE_EMAIL')) # Sanitized
    
    pass_input = driver.find_element(By.ID, "signin-pw")
    pass_input.send_keys(os.environ.get('PEERSPACE_PASS'))    # Sanitized
    
    # 3. Human Delay before clicking submit
    time.sleep(random.uniform(2, 5)) 
    driver.find_element(By.CSS_SELECTOR, "button.form").click()

def process_inbox(driver):
    # Navigate to inbox
    driver.get('https://www.peerspace.com/inbox')
    
    # Detect new messages
    messages = driver.find_elements(By.CSS_SELECTOR, "div.inbox-panel-row")
    
    for message in messages:
        # Check status (e.g., 'Accepted', 'Completed')
        status = message.find_element(By.TAG_NAME, 'span').text
        
        if status == 'Accepted':
            # Enter dialogue logic
            message.click()
            
            # Send automated reply
            textarea = driver.find_element(By.CSS_SELECTOR, "textarea")
            textarea.send_keys("Hi! Thanks for the booking. Here are the details...")
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR, "button[aria-label='Send message']").click()

if __name__ == "__main__":
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    human_login(driver)
    process_inbox(driver)
