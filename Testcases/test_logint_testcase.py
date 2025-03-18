import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pageobjects.LoginPage import Login_object
from utilies.readConfigData import ReadConfig
from utilies import customLogger
from utilies import excelUtils
from selenium import webdriver

def create_driver_instance(browser="edge"):
    """
    Create and return a new WebDriver instance based on the given browser.
    Adjust options or executable paths as needed.
    """
    if browser.lower() == "edge":
        return webdriver.Edge()
    elif browser.lower() == "chrome":
        return webdriver.Chrome()
    else:
        raise ValueError(f"Browser '{browser}' is not supported.")

class TestLogin:
    base_url = ReadConfig.getCommonData("commonData", "base_url")
    userName = ReadConfig.getCommonData("commonData", "userName")
    password = ReadConfig.getCommonData("commonData", "password")
    logger = customLogger.get_logger("LoginPage")
    # Define the Excel file path (adjust if needed)
    path = "C:\\Users\\Laptop 01\\PycharmProjects\\hybrid framework\\testdata\\Logindata4.xlsx"
    @pytest.mark.sanity
    @pytest.mark.smoke
    def test_verifying_homepage_title(self, setup):
        """
        Test case to verify that the homepage title matches the expected title.
        """
        self.logger.info("-------TC01 verifying homepage title-------")
        self.driver = setup
        self.driver.get(self.base_url)

        # Get expected homepage title from config
        expected_title = ReadConfig.getCommonData("message", "home-title")
        WebDriverWait(self.driver, 10).until(EC.title_is(expected_title))

        actual_title = self.driver.title
        self.logger.info("------getting title=" + actual_title)

        # Save screenshot for evidence
        screenshot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Screenshot", "home_title.png")
        self.driver.save_screenshot(screenshot_path)

        if actual_title == expected_title:
            self.logger.info("----successful homepage title---")
            assert True
        else:
            self.logger.info("----failed homepage title---")
            assert False, f"Expected title '{expected_title}' but got '{actual_title}'"

        self.driver.close()
    @pytest.mark.smoke

    def test_login_page_validation(self, setup):
        """
        Test case to validate the login page by logging in with credentials from the config.
        """
        self.logger.info("-------TC02 Login page validation-------")
        self.logger.info("Verifying Login Page")
        self.driver = setup
        self.driver.get(self.base_url)

        login_page = Login_object(self.driver)

        # Wait for username field to be present
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "userName"))
        )
        self.logger.info("------providing username -----")
        print(f"Username: {self.userName}")
        print(f"Password length: {len(self.password) * '*'}")  # Masked

        login_page.setUserName(self.userName)
        self.logger.info("------providing password -----")
        login_page.setPassword(self.password)
        login_page.clickLogin()

        # Get expected login title from config and verify it
        expected_title = ReadConfig.getCommonData("message", "Login-title")
        WebDriverWait(self.driver, 20).until(EC.title_contains("Mercury Tours"))
        actual_title = self.driver.title
        self.logger.info("------getting title=" + actual_title)

        print(f"Expected title: {expected_title}")
        print(f"Actual title: {actual_title}")

        if actual_title == expected_title:
            screenshot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Screenshot", "Login_title.png")
            self.driver.save_screenshot(screenshot_path)
            self.logger.info("----successful Login page title---")
            assert True
        else:
            screenshot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Screenshot", "Login_title.png")
            self.driver.save_screenshot(screenshot_path)
            self.logger.info("----failed Login page title---")
            assert False

        self.driver.close()
    @pytest.mark.regression
    def test_excel_login_page_validation(self):
        """
        Excel-driven test case:
        Reads test data from an Excel file (worksheet 's1') and validates the login page for each row.
        A new driver instance is created for each data row.
        """
        rows_count = excelUtils.getRowCount(self.path, "s1")
        lst_status = []
        for r in range(2, rows_count + 1):
            excel_username = excelUtils.readData(self.path, "s1", r, 1)
            excel_password = excelUtils.readData(self.path, "s1", r, 2)
            expected_result = excelUtils.readData(self.path, "s1", r, 3)

            self.logger.info(f"-------TC03 Login page validation (Row {r}) -------")
            self.logger.info("Verifying Login Page using Excel data")

            # Create a fresh driver instance per iteration
            driver = create_driver_instance(browser="edge")
            driver.get(self.base_url)
            login_page = Login_object(driver)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "userName"))
            )
            self.logger.info("------providing username from Excel-----")
            login_page.setUserName(excel_username)
            self.logger.info("------providing password from Excel-----")
            login_page.setPassword(excel_password)
            login_page.clickLogin()

            expected_title = ReadConfig.getCommonData("message", "Login-title")
            WebDriverWait(driver, 20).until(EC.title_contains("Mercury Tours"))
            actual_title = driver.title
            self.logger.info(f"Row {r}: Expected title: {expected_title} | Actual title: {actual_title}")

            # Validate result based on Excel expected outcome (pass/fail)
            if actual_title == expected_title and expected_result.lower() == "pass":
                self.logger.info(f"Row {r}: Successful login title as expected.")
                lst_status.append("Pass")
            elif actual_title != expected_title and expected_result.lower() == "fail":
                self.logger.info(f"Row {r}: Failed login title as expected.")
                lst_status.append("Pass")
            else:
                self.logger.info(f"Row {r}: Test did not match the expected result.")
                lst_status.append("Fail")

            driver.quit()  # End the session for this iteration

        # Assert overall success if all rows passed.
        if "Fail" in lst_status:
            self.logger.info("Some Excel login tests failed: " + str(lst_status))
            assert False, "One or more Excel login tests failed."
        else:
            self.logger.info("All Excel login tests passed.")
            assert True
