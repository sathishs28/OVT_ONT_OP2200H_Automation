import pytest

from PageObjects.Login_Page import LoginPage
from Utilities.ReadProperties import ReadConfig

snap_path = "./ScreenShots/"

act_dash_title = ReadConfig.get_dashboard_title()  # Actual dashboard title


class Test_001_Login:
    device_URL = ReadConfig.get_device_url()
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()

    @pytest.mark.Sanity
    @pytest.mark.Smoke
    @pytest.mark.Regression
    def test_homepage(self, setup, logger):  # Here setup is a fixtures from "/testCases/congtest.py" file
        logger.info("********************* Test_001_Login :: Test Homepage *********************")
        logger.info("******* Homepage Test case is started & Verifying *******")
        try:
            self.driver = setup
            self.driver.set_page_load_timeout(30)  # Set a 10-second page load timeout
            self.driver.get(self.device_URL)
            self.lp = LoginPage(self.driver)  # lp -> LoginPage object stored in lp object
            # lp_title = self.driver.title
            logo_element = self.lp.home_page_logo()
            if logo_element.is_displayed():
                assert True
                logger.info("******* Homepage Test case is completed *******")
                logger.info("******* Homepage Test case is success *******")
                self.driver.close()
            else:
                self.driver.save_screenshot(snap_path + "test_homepage_error.png")
                logger.error("************** Homepage Test case is failed **************")
                self.driver.close()
                assert False
            self.driver.quit()
        except Exception as e1:
            self.driver.save_screenshot(snap_path + "test_homepage_issue.png")
            logger.error("******** Homepage Test case is failed - Webpage is not loaded (Refer belo logs ********")
            logger.error(f"Page load failed: {str(e1)}")
            self.driver.close()
            assert False

    @pytest.mark.Sanity
    @pytest.mark.Regression
    @pytest.mark.Smoke
    def test_login(self, setup, logger):  # Here setup & logger is a fixtures from "/testCases/congtest.py" file
        logger.info("********************* Test_001_Login :: Test Login *********************")
        logger.info("******* Login Test case is started & Verifying *******")
        self.driver = setup
        self.driver.get(self.device_URL)
        self.lp = LoginPage(self.driver)
        self.lp.set_username(self.username)
        self.lp.set_password(self.password)
        self.lp.click_login()
        dash_title = self.driver.title
        try:
            # Verify the HTML title & Logout button is present or not after success login
            if act_dash_title == dash_title and self.lp.get_logout_element():
                self.lp.click_logout()
                self.driver.close()
                logger.info("******* Login & Logout Test is completed *******")
                logger.info("******* Login & Logout Test is success *******")
                assert True
            elif act_dash_title == dash_title:
                logger.error("******* Login success but logout button is not present *******")
                logger.error("******* Login Test case is failed *******")
                self.driver.save_screenshot(snap_path + "test_login_Logout_button_not_present.png")
                self.driver.close()
                assert False
            else:
                logger.error("******* Login Test case is failed *******")
                logger.error("Login Failed Error from Webpage:" + self.lp.login_error())
                self.driver.save_screenshot(snap_path + "test_login_failed.png")
                self.driver.close()
                assert False
        except Exception as e2:
            self.driver.save_screenshot(snap_path + "test_login_error.png")
            logger.error("******** Login Test case is stopped unexpected error - Webpage is not loaded ("
                         "Refer below logs ********")
            logger.error(f"Page load failed: {str(e2)}")
            self.driver.close()
            assert False
