from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --------------------------
# CONFIGURATION
# --------------------------
LSF_URL = "https://lsf.berea.edu/main/search"
NAV_URL = "https://b9general-prod.berea.edu:8443/applicationNavigator/seamless"
USERNAME = "your_username"
PASSWORD = "your_password"

STUDENT_NAME = input("Enter the student's full name: ").strip()

# --------------------------
# INITIALIZE DRIVER
# --------------------------
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

# --------------------------
# STEP 1: Open LSF search page
# --------------------------
driver.get(LSF_URL)
time.sleep(3)  # allow JS to render fully

# --------------------------
# STEP 2: Switch to iframe if exists
# --------------------------
iframes = driver.find_elements(By.TAG_NAME, "iframe")
if iframes:
    print(f"Found {len(iframes)} iframe(s), switching to first")
    driver.switch_to.frame(iframes[0])
else:
    print("No iframe detected, continuing in main page")

# --------------------------
# STEP 3: Open dropdown (always click)
# --------------------------
dropdown_button = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "button.dropdown-toggle[data-id='search']"))
)
driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_button)
time.sleep(0.3)
driver.execute_script("arguments[0].click();", dropdown_button)
time.sleep(0.5)
print("Dropdown opened")

# --------------------------
# STEP 4: Type student name
# --------------------------
search_input = wait.until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.bs-searchbox input.form-control"))
)
search_input.clear()
search_input.send_keys(STUDENT_NAME)
time.sleep(2)  # wait for suggestions to populate

# --------------------------
# STEP 5: Click first suggestion automatically
# --------------------------
first_result = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "ul.dropdown-menu.inner li a span.text"))
)
driver.execute_script("arguments[0].click();", first_result)
time.sleep(1)

# --------------------------
# STEP 6: Extract student ID from URL
# --------------------------
student_url = driver.current_url
student_id = student_url.split("/")[-1]
print(f"🎓 Student ID found: {student_id}")

# --------------------------
# STEP 7: Open Navigator and login
# --------------------------
driver.switch_to.default_content()  # exit iframe if needed
driver.get(NAV_URL)
try:
    username_box = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_box = driver.find_element(By.NAME, "password")
    username_box.send_keys(USERNAME)
    password_box.send_keys(PASSWORD)
    password_box.send_keys(Keys.RETURN)
    print("🔑 Logged into Navigator")
except:
    print("ℹ️ Already logged in or no login form found")

# --------------------------
# STEP 8: Search student in Navigator
# --------------------------
search_box_nav = wait.until(
    EC.presence_of_element_located((By.NAME, "searchField"))  # adjust selector if needed
)
search_box_nav.clear()
search_box_nav.send_keys(student_id)
search_box_nav.send_keys(Keys.RETURN)
print(f"🔍 Searched student {student_id} in Navigator")

# --------------------------
# DONE
# --------------------------
input("Press ENTER to quit...")
driver.quit()
