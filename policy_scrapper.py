import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def Web_scraping(max_click_nextpage=3):
    '''
    This function is for web scraping policy reviews from the website of Seoul City.
    max_click_nextpage: Int
    number of clicks to next page (Default: 3)
    '''
    # Setting up Chrome WebDriver
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    # URL to scrape
    url = 'https://youth.seoul.go.kr/mainA.do'
    driver.get(url)
    time.sleep(2)
    
    # Click on the review tab
    review_tab = driver.find_element(By.XPATH, '//*[@id="exit-container"]/div[1]/div[2]/div/div/div/a[2]')
    review_tab.click()
    
    # Code to view 30 posts (default value set to 10)
    more_review = driver.find_element(By.CSS_SELECTOR, '#frm > div.board-top > div.rg > div > div > a > em')
    more_review.click()
    click_30 = driver.find_element(By.XPATH, '//*[@id="30"]')
    click_30.click()
    time.sleep(2)
    
    apply_button = driver.find_element(By.CSS_SELECTOR, '#frm > div.board-top > div.rg > div > button')
    apply_button.click()
    
    # Lists to store scraped data (title, review, writer, category, update date)
    title_list = []
    review_list = []
    writer_list = []
    category_list = []
    update_list = []
    
    x_path_num = 4
    for page in range(1, max_click_nextpage + 1):
        for max_num in range(1, 31):
            time.sleep(1)
            
            name_xpath = f'//*[@id="frm"]/table/tbody/tr[{max_num}]/td[5]'
            date_xpath = f'//*[@id="frm"]/table/tbody/tr[{max_num}]/td[6]'
            
            name = driver.find_element(By.XPATH, name_xpath)
            date = driver.find_element(By.XPATH, date_xpath)
            
            writer_list.append(name.text)
            update_list.append(date.text)
            
            css_selector = f'#frm > table > tbody > tr:nth-child({max_num}) > td.text-lf > div > a'
            title_tab = driver.find_element(By.CSS_SELECTOR, css_selector)
            title_tab.click()
            
            title = driver.find_element(By.CLASS_NAME, 'flex')
            review = driver.find_element(By.CSS_SELECTOR, '#frm > div > div.view-cont > div')
            category = driver.find_element(By.CLASS_NAME, 'fc-blue')
            
            title_list.append(title.text)
            review_list.append(review.text)
            category_list.append(category.text)
            
            # Click the back button
            catalog = driver.find_element(By.CLASS_NAME, 'icn-list')
            catalog.click()
            time.sleep(0.5)
            
        if page % 5 == 0:
            print("Netx section")
            next_button = driver.find_element(By.CLASS_NAME, 'arr1.next')
            next_button.click()
            # x_path number 초기화
            x_path_num = 4
        else:
            print('Next page')
            next_button = driver.find_element(By.XPATH, f'//*[@id="frm"]/div[4]/a[{x_path_num}]')
            next_button.click()
            x_path_num += 1
        if page == max_click_nextpage :
            break
    
    # Save the results to a DataFrame
    df = pd.DataFrame({
        'Title': title_list,
        'Review': review_list,
        'Writer': writer_list,
        'Category': category_list,
        'Update Date': update_list
    })
    
    driver.quit()
    return df

if __name__ == "__main__":
    # Example of running the function
    df = Web_scraping(max_click_nextpage=8)
