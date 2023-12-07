import pytest
from PageObjects.Login_Page import LoginPage
from Utilities.ReadProperties import ReadConfig
from Utilities import Excel_Utillities

act_lp_title = ReadConfig.get_login_page_title()  # Actual Login page title
act_dash_title = ReadConfig.get_dashboard_title()  # Actual dashboard title

snap_path = "./ScreenShots/"


# snap_absolute_path = os.path.abspath(snap_relative_path)
# snap_absolute_path = "C:\\Users\\OVT_DekTech\\PycharmProjects\\OVT_ONT_OP2200H_Automation\\ScreenShots\\"


# This testing is performing... Login testing with data-driven testing (DDT) both positive & negative cases
class Test_002_Login_DDT:
    device_URL = ReadConfig.get_device_url()

    # Username & Password are getting from the TestData folder of Data_Driven_Test.xlsx file

    # Here setup & logger is a fixtures from "/testCases/congtest.py" file
    # Test-1
    @pytest.mark.Regression
    def test_login_both_username_password_valid(self, setup, logger):
        logger.info("************* Login_Test_DDT_002 :: 1-test_login_both_username_password_valid **************")
        logger.info("******* login_both_username_password_valid test case is started & Verifying *******")
        self.driver = setup
        self.driver.get(self.device_URL)
        self.lp = LoginPage(self.driver)
        username = Excel_Utillities.read_data("Login", 2, 3)
        password = Excel_Utillities.read_data("Login", 2, 4)
        self.lp.set_username(username)
        self.lp.set_password(password)
        self.lp.click_login()
        dash_title = self.driver.title
        try:
            if act_dash_title == dash_title:  # Verify the logout XPATH
                logger.info("******* Valid Login Test case is completed *******")
                logger.info("******* Valid Login Test case is success *******")
                self.lp.click_logout()
                self.driver.close()
                assert True
            else:
                self.driver.save_screenshot(snap_path + "login_both_username_password_valid.png")
                logger.error("****** TS002 :: test_login_both_username_password_valid test case is failed *******")
                self.driver.close()
                assert False
        except Exception as e2:
            self.driver.save_screenshot(snap_path + "test_login_both_username_password_valid test case_error.png")
            logger.error("************** TS002 :: test_login_both_username_password_valid test case is stopped "
                         "unexpected error - Refer belo logs **************")
            logger.error(f"Page load failed: {str(e2)}")
            self.driver.close()
            assert False

    # Here setup is a fixtures from "/testCases/congtest.py" file
    # Test-2
    @pytest.mark.Regression
    def test_login_valid_username_invalid_password(self, setup, logger):
        logger.info(
            "************** Login_Test_DDT_002 :: 2-test_login_valid_username_invalid_password ***************")
        logger.info(
            "******* test_login_valid_username_invalid_password test case is started & Verifying *******")
        self.driver = setup
        self.driver.get(self.device_URL)
        self.lp = LoginPage(self.driver)
        username = Excel_Utillities.read_data("Login", 3, 3)
        password = Excel_Utillities.read_data("Login", 3, 4)
        self.lp.set_username(username)
        self.lp.set_password(password)
        dash_title = self.driver.title
        self.lp.click_login()
        error = "ERROR: bad password!"
        try:
            if error == self.lp.login_error():
                logger.info("******* TS002 :: test_login_valid_username_invalid_password test case is Passed "
                            "*******")
                self.driver.close()
                assert True
            elif act_dash_title == dash_title:
                logger.error("******* test_login_valid_username_invalid_password test case is Failed *******")
                self.driver.save_screenshot(snap_path + "test_login_valid_username_invalid_password_valid.png")
                self.lp.click_logout()
                self.driver.close()
                assert False
            else:
                logger.error("******* TS002 :: test_login_valid_username_invalid_password test case is Stopped "
                             "*******")
                self.driver.close()
                assert False
        except Exception as e2:
            self.driver.save_screenshot(snap_path + "test_login_valid_username_invalid_password test case_error.png")
            logger.error("************** TS002 :: test_login_valid_username_invalid_password test case is "
                         "stopped unexpected error - Refer belo logs **************")
            logger.error(f"Page load failed: {str(e2)}")
            self.driver.close()
            assert False

    # Here setup is a fixtures from "/testCases/congtest.py" file
    # Test-3
    @pytest.mark.Regression
    def test_login_invalid_username_valid_password(self, setup, logger):
        logger.info("******* Login_Test_DDT_002 :: 3-test_login_invalid_username_valid_password *******")
        logger.info(
            "******* test_login_invalid_username_valid_password test case is started & Verifying *******")
        self.driver = setup
        self.driver.get(self.device_URL)
        self.lp = LoginPage(self.driver)
        username = Excel_Utillities.read_data("Login", 4, 3)
        password = Excel_Utillities.read_data("Login", 4, 4)
        self.lp.set_username(username)
        self.lp.set_password(password)
        self.lp.click_login()
        dash_title = self.driver.title
        error = "ERROR: invalid username!"
        try:
            if error == self.lp.login_error():
                logger.info("******* TS002 :: test_login_invalid_username_valid_password test case is Passed "
                            "*******")
                self.driver.close()
                assert True
            elif act_dash_title == dash_title:
                logger.error("******* test_login_invalid_username_valid_password test case is Failed *******")
                self.driver.save_screenshot(snap_path + "test_login_invalid_username_valid_password.png")
                self.lp.click_logout()
                self.driver.close()
                assert False
            else:
                logger.error("******* TS002 :: test_login_invalid_username_valid_password test case is Stopped "
                             "*******")
                logger.error("Login Failed Error from Webpage:" + self.lp.login_error())
                self.driver.close()
                assert False
        except Exception as e2:
            self.driver.save_screenshot(snap_path + "test_login_invalid_username_valid_password test case_error.png")
            logger.error("************** TS002 :: test_login_invalid_username_valid_password test case is "
                         "stopped unexpected error - Refer belo logs **************")
            logger.error(f"Page load failed: {str(e2)}")
            self.driver.close()
            assert False

    # Here setup is a fixtures from "/testCases/congtest.py" file
    # Test-4
    @pytest.mark.Regression
    def test_both_username_password_invalid(self, setup, logger):
        logger.info(
            "************** Login_Test_DDT_002 :: 4-test_both_username_password_invalid ***************")
        logger.info("******* test_both_username_password_invalid test case is started & Verifying *******")
        self.driver = setup
        self.driver.get(self.device_URL)
        self.lp = LoginPage(self.driver)
        username = Excel_Utillities.read_data("Login", 5, 3)
        password = Excel_Utillities.read_data("Login", 5, 4)
        self.lp.set_username(username)
        self.lp.set_password(password)
        self.lp.click_login()
        dash_title = self.driver.title
        error1 = "ERROR: you have logined error three times, please relogin 1 minute later!"
        error2 = "ERROR: invalid username!"
        try:
            if error1 == self.lp.login_error() or error2 == self.lp.login_error():
                logger.info("******* TS002 :: test_both_username_password_invalid test case is Passed "
                            "*******")
                self.driver.close()
                assert True
            elif act_dash_title == dash_title:
                logger.error("******* test_both_username_password_invalid test case is Failed *******")
                self.driver.save_screenshot(snap_path + "test_both_username_password_invalid.png")
                self.lp.click_logout()
                self.driver.close()
                assert False
            else:
                logger.error("******* TS002 :: test_both_username_password_invalid test case is Stopped "
                             "*******")
                logger.error("Login Failed Error from Webpage:" + self.lp.login_error())
                self.driver.close()
                assert False
        except Exception as e2:
            self.driver.save_screenshot(snap_path + "test_both_username_password_invalid test case_error.png")
            logger.error("************** TS002 :: test_both_username_password_invalid test case is "
                         "stopped unexpected error - Refer belo logs **************")
            logger.error(f"Page load failed: {str(e2)}")
            self.driver.close()
            assert False
