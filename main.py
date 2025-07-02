from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


import time
import json

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)


def main():
    # Step 1: Go to DMW Approved Job Orders page
    driver.get("https://dmw.gov.ph/approved-job-orders")

    # Step 2: Scroll to the 'Search by' secction
    search_by = driver.find_element(By.CLASS_NAME, "form-input")
    ActionChains(driver).scroll_to_element(search_by).perform()

    #Step 2.1: Type 'United Kingdom' and Enter
    search_by.clear()
    search_by.send_keys("United Kingdom" + Keys.ENTER)
    time.sleep(3) 

    # Create data variable
    data = []

    #Step 3 Scrape per Page
    total_page = 3  #[NEED] Change this to X amount of pages
    for i in range(total_page):  
        
        print(f"\nScraping page {i+1}...")
        ActionChains(driver).scroll_to_element(search_by).perform()

        # Get all rows
        rows = driver.find_elements(By.XPATH, '//tbody/tr')
        for row in rows:
            try:
                jobsite = row.find_element(By.XPATH, './/td[@data-label="Jobsite"]//span').text
                position = row.find_element(By.XPATH, './/td[@data-label="Position / Agency / Principal"]/div/div[1]').text
                agency = row.find_element(By.XPATH, './/td[@data-label="Position / Agency / Principal"]/div/div[3]').text
                principal = row.find_element(By.XPATH, './/td[@data-label="Position / Agency / Principal"]/div/div[5]').text
                accreditation = row.find_element(By.XPATH, './/td[@data-label="Accreditation Class"]/div/div').text
                needed = row.find_element(By.XPATH, './/td[@data-label="Needed"]/div/div').text
                approval = row.find_element(By.XPATH, './/td[@data-label="Approval"]/div/div').text

                r_data = {
                    "Jobsite": jobsite,
                    "Position": position,
                    "Agency": agency,
                    "Principal": principal,
                    "Accreditation": accreditation,
                    "Needed": needed,
                    "Approval": approval
                }

                data.append(r_data)

            except Exception as e:
                print("Error reading a row:", e)
                
        if i < total_page - 1:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/div[4]/div[2]/div[2]/div[1]/button[3]'))).click()
            time.sleep(3)

            # Click return to 'Return to top' button
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/button'))).click()
            time.sleep(5)

    #Step 4: Convert to JSON file
    filename = "United Kingdom Job Order.json"
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

    # Wait for 10 seconds then close the chrome
    time.sleep(10)
    driver.quit()

if __name__ ==  '__main__':
    main()