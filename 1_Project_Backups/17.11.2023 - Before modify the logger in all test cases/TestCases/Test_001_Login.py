import pytest
from Utilities.CustomLogger import LogGen

from PageObjects.Login_Page import LoginPage
from Utilities.ReadProperties import ReadConfig

# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

snap_path = "./ScreenShots/"
# snap_absolute_path = os.path.abspath(snap_relative_path)
# snap_absolute_path = "C:\\Users\\OVT_DekTech\\PycharmProjects\\OVT_ONT_OP2200H_Automation\\ScreenShots\\"

# act_lp_title = ReadConfig.get_login_page_title()  # Actual Login page title
act_dash_title = ReadConfig.get_dashboard_title()  # Actual dashboard title


class Test_001_Login:
    device_URL = ReadConfig.get_device_url()
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()

    logger = LogGen.loggen()  # Logen2 Class -> method - loggen2() stored in object

    @pytest.mark.sanity
    def test_homepage(self, setup):  # Here setup is a fixtures from "/testCases/congtest.py" file
        self.logger.info("********************* Test_001_Login :: Test Homepage *********************")
        self.logger.info("******* Homepage Test case is started & Verifying *******")
        try:
            self.driver = setup
            self.driver.set_page_load_timeout(30)  # Set a 10-second page load timeout
            self.driver.get(self.device_URL)
            self.lp = LoginPage(self.driver)  # lp -> LoginPage object stored in lp object
            # lp_title = self.driver.title
            logo_element = self.lp.home_page_logo()
            if logo_element.is_displayed():
                assert True
                self.logger.info("******* Homepage Test case is completed *******")
                self.logger.info("******* Homepage Test case is success *******")
                self.driver.close()
            # elif lp_title == act_lp_title:
            #     self.driver.save_screenshot(snap_path + "test_homepage_logo_missing.png")
            #     self.logger.error("******* Homepage is Loaded but Logo is not present *******")
            #     self.driver.close()
            #     assert False
            else:

                self.driver.save_screenshot(snap_path + "test_homepage_error.png")
                # self.logger.error("******* Homepage Title & Logo is not found *******")
                self.logger.error("************** Homepage Test case is failed **************")
                self.driver.close()
                assert False
            self.driver.quit()
        except Exception as e1:
            self.driver.save_screenshot(snap_path + "test_homepage_issue.png")
            self.logger.warning("************** Homepage Test case is failed - Webpage is not loaded (Refer belo logs "
                                "**************")
            self.logger.warning(f"Page load failed: {str(e1)}")
            self.driver.close()
            assert False

    @pytest.mark.sanity
    @pytest.mark.regression
    def test_login(self, setup):  # Here setup is a fixtures from "/testCases/congtest.py" file
        self.logger.info("********************* Test_001_Login :: Test Login *********************")
        self.logger.info("******* Login Test case is started & Verifying *******")
        self.driver = setup
        self.driver.get(self.device_URL)
        # wait = WebDriverWait(self.driver, 10)  # wait variable is assigned for individual element wait time
        self.lp = LoginPage(self.driver)
        self.lp.set_username(self.username)
        self.lp.set_password(self.password)
        self.lp.click_login()
        dash_title = self.driver.title
        # login_button_element = self.lp.get_login_element()
        # logout_button_element = self.lp.get_logout_element()
        try:
            # Verify the HTML title & Logout button is present or not after success login
            if act_dash_title == dash_title and self.lp.get_logout_element():
                self.lp.click_logout()
                self.driver.close()
                self.logger.info("******* Login & Logout Test is completed *******")
                self.logger.info("******* Login & Logout Test is success *******")
                assert True
            elif act_dash_title == dash_title:
                self.logger.error("******* Login success but logout button is not present *******")
                self.logger.error("******* Login Test case is failed *******")
                self.driver.save_screenshot(snap_path + "test_login_Logout_button_not_present.png")
                self.driver.close()
                assert False
            else:
                self.logger.error("******* Login Test case is failed *******")
                self.logger.error("Login Failed Error from Webpage:" + self.lp.login_error())
                self.driver.save_screenshot(snap_path + "test_login_failed.png")
                self.driver.close()
                assert False
            # self.logger.info("******* Login Test case is stopped & Done *******")
        except Exception as e2:
            self.driver.save_screenshot(snap_path + "test_login_error.png")
            self.logger.warning("************** Login Test case is stopped unexpected error - Webpage is not loaded ("
                                "Refer belo logs **************")
            self.logger.warning(f"Page load failed: {str(e2)}")
            self.driver.close()
            assert False
