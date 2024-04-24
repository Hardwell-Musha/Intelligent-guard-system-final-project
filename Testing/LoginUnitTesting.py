import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLogin(unittest.TestCase):

    def setUp(self):
        # Path to the Chrome WebDriver executable
        chrome_driver_path = r'C:\BrowserDrivers\chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path)

    def print_green(self, text):
        print("\033[92m{}\033[00m".format(text))  # ANSI escape code for green color

    def test_successful_login(self):
        driver = self.driver
        driver.get("http://localhost:3000/login")  
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys("shortsmania8759@gmail.com")
        password_input = driver.find_element_by_id("password")
        password_input.send_keys("62541781")
        login_button = driver.find_element_by_class_name("submit-button")
        login_button.click()
        # Wait for the page to navigate
        WebDriverWait(driver, 20).until(
            EC.url_to_be("http://localhost:3000/")
        )
        # Assert that the URL has changed to the dashboard page
        self.assertEqual(driver.current_url, "http://localhost:3000/")
        self.print_green("Successful login test passed.")

    def test_invalid_credentials(self):
        driver = self.driver
        driver.get("http://localhost:3000/login")
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys("invalid@example.com")
        password_input = driver.find_element_by_id("password")
        password_input.send_keys("invalidpassword")
        login_button = driver.find_element_by_class_name("submit-button")
        login_button.click()
        # Wait for the error message to appear
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "error-message"))
        )
        # Assert that the error message is displayed
        error_message = driver.find_element_by_class_name("error-message").text
        self.assertIn("auth/invalid-credential", error_message)
        self.print_green("Invalid credentials test passed.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
