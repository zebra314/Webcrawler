from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

PATH = 'C:/Users/kidal/Desktop/webcrawler/chromedriver.exe'

#chrome_options = webdriver.ChromeOptions() # open the web in incogito mode
#chrome_options.add_argument("--incognito")
#
#driver = webdriver.Chrome(PATH , chrome_options=chrome_options)

driver = webdriver.Chrome(PATH )
driver.get('https://www.google.com.tw/?hl=zh_TW') # open the website

search = driver.find_element(By.NAME,'q') 
search.send_keys('新竹 音樂' + Keys.RETURN)

# print(driver.title) 

# explicit wait 

# driver.quit() # close the website