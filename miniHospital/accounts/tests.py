from selenium import webdriver
from selenium.webdriver.common.by import By
import time
driver = webdriver.Firefox()
# or any other webdriver of your choice
driver.get('http://127.0.0.1:8000/accounts/login/')
username = driver.find_element(By.ID, 'email')
password = driver.find_element(By.ID, 'password')
username.send_keys('johnson@gmail.com')
password.send_keys('Doctor@000')
login_button = driver.find_element(By.ID, 'btn')
login_button.click()
time.sleep(5)  # wait for 5 seconds for the page to load
if driver.current_url == 'http://localhost/lms/user/userhome.php':
    print('Login successful')
else:
    print('Login failed')
driver.quit()
