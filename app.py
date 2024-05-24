import streamlit as st
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://www.google.com/search?q=google+silks+saree&oq=google+silks+saree&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIJCAEQABgNGIAEMgoIAhAAGA8YFhgeMgwIAxAAGAgYDRgPGB4yDQgEEAAYhgMYgAQYigUyDQgFEAAYhgMYgAQYigUyCggGEAAYgAQYogQyCggHEAAYgAQYogQyCggIEAAYogQYiQUyCggJEAAYgAQYogTSAQgzOTc2ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8"
XPATH = '//*[@id="rso"]/div[3]/div/div/div[1]/div/div/span/a/h3'
TIMEOUT = 20

st.title("Test Selenium")
st.markdown("You should see some random Football match text below in about 21 seconds")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(
    options=chrome_options,
    service=service,
)
driver.get(URL)

try:
    WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, XPATH,))
    )

except TimeoutException:
    st.warning("Timed out waiting for page to load")
    driver.quit()

time.sleep(10)
elements = driver.find_elements(By.XPATH,XPATH)
st.write([el.text for el in elements])
driver.quit()
