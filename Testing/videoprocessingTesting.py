import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestVideoUpload(unittest.TestCase):

    def setUp(self):
        # Initialize the Selenium WebDriver
        self.driver = webdriver.Chrome(executable_path="C:\\BrowserDrivers\\chromedriver.exe")
        self.driver.get("http://localhost:3000")  # Replace with your React app URL

    def tearDown(self):
        # Close the browser after each test
        self.driver.quit()

    def test_automatic_video_upload(self):
        # Find the upload button
        upload_button = self.driver.find_element_by_class_name("upload-button")

        # Assert that the upload button is visible
        self.assertTrue(upload_button.is_displayed())

        # Find the file input element
        file_input = self.driver.find_element_by_id("video-file")

        # Upload a video file
        file_input.send_keys(r"C:\Users\ARX56\OneDrive\Desktop\InteligentGuardReact\InteligentGuardReact\Testing\temp.mp4")

        try:
            # Wait for file upload to complete
            WebDriverWait(self.driver, 180).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "upload-button"))
            )

            # Wait indefinitely for the Download Processed Video button to become visible
            download_button = WebDriverWait(self.driver, 0).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "download-button"))
            )

            # Assert that the download button is visible
            self.assertTrue(download_button.is_displayed())

            # Print success message in the terminal
            print("Video processing successful!")

        except:
            # Print error message if the button does not appear
            print("Failed to find the Download Processed Video button.")

if __name__ == '__main__':
    unittest.main()
