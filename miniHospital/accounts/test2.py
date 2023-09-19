from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
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
    By.XPATH, '//*[@id="content-main"]/div[3]/table/tbody/tr[2]/th/a')
presc_link.click()
btnn = driver.find_element(By.XPATH, '//*[@id="content-main"]/ul/li[2]/a')
btnn.click()
select_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'id_file_format'))
)
select = Select(select_element)
select.select_by_value('0')
btnn = driver.find_element(By.CLASS_NAME, 'default')
btnn.click()
if driver.current_url == 'http://127.0.0.1:8000/admin/dashboard/doctor/doctor/export/?':
    print('Export completed')
else:
    print('Export not completed')
driver.quit()
