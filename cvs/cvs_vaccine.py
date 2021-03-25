# Prerequisit: selenium and chromedriver
# On Mac:
# Pip3 install -U selenium
# brew  install chromedriver



import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

chromedriver_location='/usr/local/bin/chromedriver'
initial_url='https://www.cvs.com/immunizations/covid-19-vaccine?icid=cvs-home-hero1-banner-1-link2-coronavirus-vaccine#'

state='California'


chromeOptions = webdriver.ChromeOptions() 
chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) 
chromeOptions.add_argument("--headless") 
chromeOptions.add_argument("--no-sandbox") 
chromeOptions.add_argument("--disable-setuid-sandbox") 

chromeOptions.add_argument("--remote-debugging-port=0")  

chromeOptions.add_argument("--disable-dev-shm-using") 
chromeOptions.add_argument("--disable-extensions") 
chromeOptions.add_argument("--disable-gpu") 
chromeOptions.add_argument("start-maximized") 
chromeOptions.add_argument("disable-infobars")
chromeOptions.add_argument(r"user-data-dir=.\cookies\\test") 

driver = webdriver.Chrome(chromedriver_location, options=chromeOptions)  
driver.get(initial_url);
time.sleep(3) 

try:
	CA=driver.find_element(By.XPATH,'/html/body/div[3]/div/div[1]/a');
	CA.click();
	time.sleep(5);
except NoSuchElementException:
	pass

try:
	CA=driver.find_element_by_link_text(state);
	CA.click();
except NoSuchElementException:
	driver.quit();


time.sleep(2) 

CA_text=driver.find_element(By.XPATH,'/html/body/div[2]/div/div[13]/div/div/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[6]/div/div')
print(CA_text.text)

driver.quit()
