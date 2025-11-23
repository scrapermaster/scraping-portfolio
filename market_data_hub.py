import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gspread # Google Sheets API
import time

# GOAL: Scrape dynamic financial table (EEX) and sync to Google Sheets

def scrape_eex_data():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    driver = uc.Chrome(options=options)
    
    driver.get('https://www.eex.com/en/market-data/market-data-hub')
    
    # 1. Handle Cookie Consent (Crucial for accessing the table)
    try:
        button_close = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Accept']"))
        )
        driver.execute_script("arguments[0].click();", button_close)
    except: pass

    # 2. Interact with Dynamic Dropdowns (Country -> Maturity -> Delivery)
    countries_select = Select(driver.find_element(By.ID, "tableGraph_areaSelect"))
    
    results = []
    
    for country in countries_select.options:
        if country.text == "Select Country": continue
        
        countries_select.select_by_visible_text(country.text)
        
        # Trigger table update
        go_button = driver.find_element(By.ID, "tableGraph_submitBtn") 
        driver.execute_script("arguments[0].click();", go_button)
        
        # Wait for Loading Spinner to disappear
        WebDriverWait(driver, 30).until(
            lambda d: "open" not in d.find_element(By.CSS_SELECTOR, "div.fixed-table-loading").get_attribute("class")
        )
        
        # Parse Table
        rows = driver.find_elements(By.CSS_SELECTOR, "table#tableGraph_dataTable>tbody tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 3:
                price = cells[3].text
                results.append([country.text, price])

    driver.quit()
    return results

def upload_to_gsheets(data):
    # Syncs the scraped data to a Google Sheet for the finance team
    gc = gspread.service_account(filename='credentials.json')
    sh = gc.open_by_key(os.environ.get('SHEET_ID'))
    worksheet = sh.get_worksheet(0)
    worksheet.append_rows(data)

if __name__ == "__main__":
    data = scrape_eex_data()
    upload_to_gsheets(data)
