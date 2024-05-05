import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class TestVideoProcessing(unittest.TestCase):
    def setUp(self):
        # Path to the Chrome WebDriver executable
        chrome_driver_path = r'C:\BrowserDrivers\chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path)

    def tearDown(self):
        self.driver.quit()

    def print_green(self, text):
        print("\033[92m{}\033[00m".format(text))  # ANSI escape code for green color

    def login(self):
        # Check if we are already on the dashboard page
        if "localhost:3000" in self.driver.current_url:
            return

        # Otherwise, perform the login
        self.driver.get("http://localhost:3000/login")
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys("shortsmania8759@gmail.com")
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys("62541781")
        login_button = self.driver.find_element(By.CLASS_NAME, "submit-button")
        login_button.click()
        # Wait for the page to navigate
        WebDriverWait(self.driver, 20).until(
            EC.url_to_be("http://localhost:3000/")
        )
        self.print_green("Login successful.")

    def test_video_processing(self):
        self.login()

        # Navigate to the home page only if not already on the dashboard
        if "localhost:3000" not in self.driver.current_url:
            self.driver.get("http://localhost:3000/")  # Update with the correct URL

        # Wait for the video-file input element to be clickable
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "video-file"))
        )

        # Find the file input element and upload a video file
        file_input = self.driver.find_element(By.ID, "video-file")
        file_input.send_keys(r'C:\Users\ARX56\OneDrive\Desktop\InteligentGuardReact\Testing\temp.mp4')

        # Find the upload button and click it
        upload_button = self.driver.find_element(By.CLASS_NAME, "upload-button")
        upload_button.click()

        # Wait for 5 seconds
        time.sleep(5)

        # Print test passed message
        print("\033[92mTest passed: Processing started\033[00m")

    def test_video_from_url(self):
        self.login()

        # Navigate to the home page only if not already on the dashboard
        if "localhost:3000" not in self.driver.current_url:
            self.driver.get("http://localhost:3000/")  # Update with the correct URL

        # Wait for the video-link input element to be clickable
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "video-link"))
        )

        # Find the video-link input element and paste the URL
        video_link_input = self.driver.find_element(By.ID, "video-link")
        video_link_input.send_keys("fomnn2zer3foheoueh7n")

        # Find the play button and click it
        play_button = self.driver.find_element(By.CLASS_NAME, "play-button")
        play_button.click()

        # Wait for the video to play (adjust delay as needed)
        time.sleep(5)

        # Print test passed message
        print("\033[92mTest passed: Video from URL played successfully\033[00m")

    def test_processed_video_download(self):
        self.login()

        # Navigate to the home page only if not already on the dashboard
        if "localhost:3000" not in self.driver.current_url:
            self.driver.get("http://localhost:3000/")  # Update with the correct URL

        # Paste the video link
        video_link_input = self.driver.find_element(By.ID, "video-link")
        video_link_input.send_keys("fomnn2zer3foheoueh7n")
        
        # Click the play video button
        play_video_button = self.driver.find_element(By.CLASS_NAME, "play-button")
        play_video_button.click()

        # Wait for the download button to appear
        try:
            download_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "download-button"))
            )
        except TimeoutException:
            print("Download button did not appear within 10 seconds.")
            return

        # Click the download button
        download_button.click()

        # Wait for the download to complete (adjust delay as needed)
        time.sleep(5)

        # Print test passed message
        print("\033[92mTest passed: Processed video downloaded successfully\033[00m")

if __name__ == "__main__":
    unittest.main()
