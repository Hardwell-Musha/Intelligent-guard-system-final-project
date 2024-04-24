from selenium import webdriver
import time

# Initialize Chrome WebDriver
driver = webdriver.Chrome(executable_path="C:\\BrowserDrivers\\chromedriver.exe")

# Open the login page
driver.get("http://localhost:3000/login")

# Maximize the window to ensure the title is visible
driver.maximize_window()

# Print the title of the page
print(driver.title)

# Wait for 5 seconds (adjust as needed)
time.sleep(5)

# Close the browser window
driver.quit()
