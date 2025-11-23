import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
import random
import time
import os

# Architecture: Distributed workers pulling jobs from MySQL
# Target: Zillow (protected by PerimeterX/verify)

def get_db_connection():
    return mysql.connector.connect(
      host=os.environ.get('DB_HOST'),
      user=os.environ.get('DB_USER'),
      password=os.environ.get('DB_PASS'),
      database="zillow_data"
    )

def worker_process():
    mydb = get_db_connection()
    mycursor = mydb.cursor()
    
    # FETCH JOB: Get URL that hasn't been scraped yet
    mycursor.execute("SELECT * FROM zillow_search_urls WHERE scraped = '0' AND in_work = '0' ORDER BY rand() LIMIT 10")
    jobs = mycursor.fetchall()

    if not jobs:
        return

    # LOCK JOB: Mark as 'in_work' so other workers don't grab it
    job_ids = [str(job[0]) for job in jobs]
    mycursor.execute(f"UPDATE `zillow_search_urls` SET `in_work` = '1' WHERE `id` IN ({','.join(job_ids)})")
    mydb.commit()

    # SETUP BROWSER
    options = uc.ChromeOptions()
    options.add_argument(f'--proxy-server={os.environ.get("PROXY")}') 
    options.add_argument('--headless')
    
    driver = uc.Chrome(options=options)
    
    for job in jobs:
        url = job[5]
        driver.get(url)
        
        # Anti-Bot Handling: Check for CAPTCHA or 'Press & Hold'
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "challenge-running"))
            )
            print("Challenge detected - taking evasive action...")
            # [Logic to solve captcha or rotate IP]
        except:
            pass
            
        # Extract Agent Data
        try:
            agent_container = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'p[data-testid="attribution-LISTING_AGENT"]'))
            )
            # [Parsing logic...]
            print("Agent data extracted successfully")
            
            # Update DB with success
            mycursor.execute("UPDATE `zillow_search_urls` SET `scraped`='1' WHERE id = %s", (job[0],))
            mydb.commit()
            
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

    driver.quit()

if __name__ == "__main__":
    worker_process()
