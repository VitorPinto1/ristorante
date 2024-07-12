import subprocess
import time
import os
import requests
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import logging

logging.basicConfig(level=logging.INFO)

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
        driver.get("http://127.0.0.1:5000/login/login")
        name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "inputName"))
        )
        name_input.send_keys("testuser")

        # Wait for the password input element to be present and enter the password
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "inputPassword"))
        )
        password_input.send_keys("Testuser1#")
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "userReservation"))
        )
        driver.get("http://127.0.0.1:5000/reservation/reservation")
        try:
            name_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "inputNameUser"))
            )
        except:
            name_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "inputName"))
            )
        people_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "inputPeople"))
        )
        select_people = Select(people_input)
        select_people.select_by_visible_text("7")
        people_input.send_keys(Keys.TAB)
        date_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "inputDate"))
        )
        driver.execute_script("arguments[0].value = '2024-08-30';", date_input)
        date_input.send_keys(Keys.TAB)
        time_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "inputTime"))
        )
        driver.execute_script("arguments[0].value = '16:00';", time_input)
        reservation_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        actions = ActionChains(driver)
        actions.move_to_element(reservation_button).click().perform()

        # Wait for the confirmation button to be present, indicating a successful reservation
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "buttonConfirmation"))
        )
        print("Reservation test succeeded!")

    except Exception as e:
        error_message = traceback.format_exc()
        logging.error(f"Test failed : {error_message}")
        print(f"Test failed : {error_message}")
    finally:
        driver.quit()
finally:
    server.terminate()
