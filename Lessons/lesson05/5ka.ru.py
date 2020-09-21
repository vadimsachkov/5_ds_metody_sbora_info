from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome('./chromedriver.exe',options=chrome_options)

driver.get('https://5ka.ru/special_offers/')
pages = 0

while pages < 3:

    # button = driver.find_element_by_class_name('special-offers__more-btn')
    try:
        button = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'special-offers__more-btn'))
        )
        button.click()
        pages += 1
    except:
        print('Страиницы кончились')
        break

goods = driver.find_elements_by_class_name('sale-card')
for good in goods:
    print(good.find_element_by_class_name('sale-card__title').text)
