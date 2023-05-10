from selenium import webdriver
from selenium.webdriver.common.by import By
PATH = 'E:\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(PATH)
driver.get('http://127.0.0.1:8000/accounts/login/')
email = driver.find_element(By.ID, 'email1')
password = driver.find_element(By.ID, 'password')
email.send_keys('johnson@gmail.com')
password.send_keys('Doctor@000')
login_button = driver.find_element(By.ID, 'btn')
login_button.click()
if driver.current_url == 'http://127.0.0.1:8000/doctor/':
    print('login successful')
else:
    print('login failed')
driver.get('http://127.0.0.1:8000/doctor/viewAppo')
driver.get('http://127.0.0.1:8000/doctor/viewpatient/23')
if driver.current_url == 'http://127.0.0.1:8000/doctor/viewpatient/23':
    print('appointment view successful')
else:
    print('appointment view failed')
driver.quit()
