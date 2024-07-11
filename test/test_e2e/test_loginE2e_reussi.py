
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
        driver.get("http://127.0.0.1:5000/login/login")
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "inputName"))
        )
        email_input.send_keys("testuser")
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "inputPassword"))
        )
        password_input.send_keys("Testuser1#")
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "userReservation"))
        )

        print("Test de connexion réussi!")
    except Exception as e:
        print(f"Test échoué : {e} - L'erreur peut être liée à un problème de connexion ou à la non présence de l'élément.")
    finally:
        driver.quit()
finally:
    server.terminate()
