import subprocess
import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

os.environ['FLASK_ENV'] = 'test'

def wait_for_server(url, timeout=30):
    start_time = time.time()
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.ConnectionError:
            pass
        if time.time() - start_time > timeout:
            raise TimeoutError("Timed out waiting for the server to start")
        time.sleep(1)
server = subprocess.Popen(["python", "app.py"])
try:
    wait_for_server("http://127.0.0.1:5000/login/login")
    driver = webdriver.Chrome()
    try:
        # Navigate to the login page
        driver.get("http://127.0.0.1:5000/login/login")
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "inputName"))
        )
        email_input.send_keys("testuser")

        # Wait for the password input element to be present and enter the password
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "inputPassword"))
        )
        password_input.send_keys("Fail12345#")
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()

        # Wait for the alert message element to be present, indicating a login attempt result
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "alertMessage"))
        )
        print("Test login successful. Unable to log in")
    except Exception as e:
        print(f"Test failed : {e} - The error may be related to a connection issue or the absence of the element.")
    finally:
        driver.quit()
finally:
    server.terminate()
