from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = 'E:\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(PATH)

driver.get('http://127.0.0.1:8000/accounts/login/')
email = driver.find_element(By.ID, 'email1')
password = driver.find_element(By.ID, 'password')
email.send_keys('admin@gmail.com')
password.send_keys('admin')
login_button = driver.find_element(By.ID, 'btn')
login_button.click()

if driver.current_url == 'http://127.0.0.1:8000/admin/dashboard/':
    print('Login successful')
else:
    print('Login failed')


presc_link = driver.find_element(
    By.XPATH, '//*[@id="content-main"]/div[6]/table/tbody/tr[3]/th/a')
presc_link.click()

btnn = driver.find_element(By.ID, 'id_form-0-leaveStatus')
btnn.click()

btnn = driver.find_element(By.CLASS_NAME, 'default')
btnn.click()

if driver.current_url == 'http://127.0.0.1:8000/admin/dashboard/leave/leavemodel/':
    print('leave approved')
else:
    print('leave not approved')

driver.quit()
