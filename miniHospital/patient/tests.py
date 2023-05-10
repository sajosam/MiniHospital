from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = 'E:\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(PATH)

driver.get('http://127.0.0.1:8000/accounts/login/')
email = driver.find_element(By.ID, 'email1')
password = driver.find_element(By.ID, 'password')
email.send_keys('saajosaam@gmail.com')
password.send_keys('Admin@000')
login_button = driver.find_element(By.ID, 'btn')
login_button.click()

if driver.current_url == 'http://127.0.0.1:8000/':
    print('Login successful')
else:
    print('Login failed')

# Locate the dropdown button and click to open the dropdown
dropdown_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'drop')))
dropdown_button.click()

# Wait for the dropdown menu to be visible
dropdown_menu = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, 'drop')))

# Locate and click on the "presc" link within the dropdown menu
presc_link = dropdown_menu.find_element(By.ID, 'presc')
presc_link.click()

if driver.current_url == 'http://127.0.0.1:8000/viewPresc/':
    print('Prescription page opened')
else:
    print('Prescription page not opened')

driver.quit()
