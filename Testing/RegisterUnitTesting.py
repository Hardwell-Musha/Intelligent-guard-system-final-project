import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestRegistration(unittest.TestCase):

    def setUp(self):
        # Path to the Chrome WebDriver executable
        chrome_driver_path = r'C:\BrowserDrivers\chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path)

    def print_success(self, text):
        print("\033[92m{}\033[00m".format(text))  # ANSI escape code for green color

    def test_successful_registration(self):
        driver = self.driver
        driver.get("http://localhost:3000/register")  # Change URL to your register page
        try:
            name_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "name"))
            )
            name_input.send_keys("John Doe")
            email_input = driver.find_element_by_id("email")
            email_input.send_keys("newuser@example.com")
            password_input = driver.find_element_by_id("password")
            password_input.send_keys("password123")
            register_button = driver.find_element_by_class_name("submit-button")
            register_button.click()
            # Pass the test with verification sent
            self.print_success("Verification email sent successfully.")
        except Exception as e:
            self.fail("Test failed: {}".format(e))

    def test_email_already_taken(self):
        driver = self.driver
        driver.get("http://localhost:3000/register")  # Change URL to your register page
        try:
            name_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "name"))
            )
            name_input.send_keys("Jane Doe")
            email_input = driver.find_element_by_id("email")
            email_input.send_keys("shortsmania8759@gmail.com")  # Use an existing email
            password_input = driver.find_element_by_id("password")
            password_input.send_keys("password123")
            register_button = driver.find_element_by_class_name("submit-button")
            register_button.click()
            # Wait for the error message to appear
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "error-message"))
            )
            # Assert that the error message is displayed
            error_message = driver.find_element_by_class_name("error-message").text
            self.assertIn("Email is already taken", error_message)
            self.print_success("Email already taken test passed.")
        except Exception as e:
            self.fail("Test failed: {}".format(e))

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
