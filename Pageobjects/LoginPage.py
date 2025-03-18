from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Login_object:
    def __init__(self, driver):
        self.driver = driver
        self.username_field = (By.NAME, "userName")    # Locator for username input
        self.password_field = (By.NAME, "password")      # Locator for password input
        self.btn_login = (By.NAME, "submit")             # Locator for login button

    def setUserName(self, username):
        username_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.username_field)
        )
        username_element.clear()
        username_element.send_keys(username)

    def setPassword(self, password):
        password_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.password_field)
        )
        password_element.clear()
        password_element.send_keys(password)

    def clickLogin(self):
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.btn_login)
        )
        login_button.click()
