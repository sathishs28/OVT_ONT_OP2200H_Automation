import pytest
from Utilities.ReadProperties import ReadConfig
from PageObjects.Login_Page import LoginPage
from PageObjects.Admin_Page import AdminPage
from selenium.webdriver.common.alert import Alert

snap_path = "./ScreenShots/"


class Test_006_Password_Change:
    device_URL = ReadConfig.get_device_url()
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()

    @pytest.mark.Sanity
    @pytest.mark.Regression
    def test_password_change(self, setup, logger):
        logger.info("************* Test_006_Password_Change :: test_password_change *************")
        try:
            self.driver = setup
            self.driver.get(self.device_URL)

            # Login Device
            self.lp = LoginPage(self.driver)
            self.lp.login(self.username, self.password)

            # Navigate to Admin Page
            self.ap = AdminPage(self.driver)
            self.ap.click_admin_mainmenu()
            self.ap.click_admin_submenu()
            self.ap.click_password_change()

            # Change Password
            new_password = "Ovt"
            self.ap.switch_iframe()
            self.ap.select_username(self.username)
            self.ap.send_old_password(self.password)
            self.ap.send_new_password(new_password)
            self.ap.send_conform_password(new_password)
            self.ap.click_apply_btn()
            act_status = "Change password successfully! Please login with new password."

            # Wait for the pop-up to appear
            alert = Alert(self.driver)
            # print("Alert Text:", alert.text) # Access the text of the alert
            got_status = alert.text
            if act_status == got_status:
                alert.accept()  # Accept the alert (click OK)
                logger.info(f"******** Status - {got_status} *******")
                logger.info(f"******** Trying to login with New Password - '{new_password}' *******")
                # Login device with new password
                self.lp.login(self.username, new_password)
                act_dash_title = ReadConfig.get_dashboard_title()  # Actual dashboard title
                # Verify the HTML title & Logout button is present or not after success login
                dash_title = self.driver.title
                if act_dash_title == dash_title:
                    logger.info("******* New Password Login & Logout Test case is completed & Success *******")
                    logger.info("******* Test Password Change Test case is Passed *******")
                    # Revert the Newly Changed password into default
                    # Navigate to Admin Page
                    self.ap = AdminPage(self.driver)
                    self.ap.click_admin_mainmenu()
                    self.ap.click_admin_submenu()
                    self.ap.click_password_change()

                    # Change Password
                    new_password = "Ovt"
                    self.ap.switch_iframe()
                    self.ap.select_username(self.username)
                    self.ap.send_old_password(new_password)
                    self.ap.send_new_password(self.password)
                    self.ap.send_conform_password(self.password)
                    self.ap.click_apply_btn()
                    alert.accept()  # Accept the alert (click OK)
                    logger.info("******* FYI - Newly Changed password Reverted into default last used password *******")
                    self.driver.close()
                    assert True
                else:
                    logger.error("******* New Password Login Failed *******")
                    logger.error("Login Failed Error from Webpage:" + self.lp.login_error())
                    self.driver.save_screenshot(snap_path + "test_login_new_password_failed.png")
                    logger.error("******* Test Password Change Test case is Failed *******")
                    self.driver.close()
                    assert False
                return
            else:
                self.driver.save_screenshot(snap_path + "test_password_change_error.png")
                logger.error("******* Test Password Change Test case is Stopped *******")
                logger.error(f"******** Status - {got_status} *******")
                alert.accept()  # Accept the alert (click OK)
                self.driver.switch_to.default_content()
                self.lp.click_logout()
                self.driver.close()
                assert False
        except Exception as e1:
            self.driver.save_screenshot(snap_path + "test_password_change_issue.png")
            logger.error("******** test_password_change Test case is stopped - Refer belo logs *******")
            logger.error(f"Page load failed: {str(e1)}")
            self.driver.switch_to.default_content()
            self.lp.click_logout()
            self.driver.close()
            assert False

    @pytest.mark.Sanity
    @pytest.mark.Regression
    def test_password_change_wrong_old_password(self, setup, logger):
        logger.info("************* Test_006_Password_Change :: test_password_change_wrong_old_password *************")
        try:
            self.driver = setup
            self.driver.get(self.device_URL)

            # Login Device
            self.lp = LoginPage(self.driver)
            self.lp.login(self.username, self.password)

            # Navigate to Admin Page
            self.ap = AdminPage(self.driver)
            self.ap.click_admin_mainmenu()
            self.ap.click_admin_submenu()
            self.ap.click_password_change()

            # Change Password
            wrong_old_password = "Wrong@13r34"
            new_password = "Ovt"
            self.ap.switch_iframe()
            self.ap.select_username(self.username)
            self.ap.send_old_password(wrong_old_password)
            self.ap.send_new_password(new_password)
            self.ap.send_conform_password(new_password)
            self.ap.click_apply_btn()
            error_status = "ERROR: wrong password!"
            if error_status == self.ap.get_pw_change_error_status():
                logger.info("******* Error status got & Try to login in with new password *******")
                logger.info("******* Expected - App shouldn't login with new password *******")
                self.driver.switch_to.default_content()
                self.lp.click_logout()
                self.lp.click_af_logout_ok_btn()
                if self.lp.get_login_element().is_displayed():
                    # Try to Log-in Device
                    self.lp.login(self.username, new_password)
                    error = "ERROR: bad password!"
                    if error == self.lp.login_error():
                        logger.info("******* Expected - Webpage not login *******")
                        logger.info("******* test_password_change_wrong_old_password Test case is Passed *******")
                        self.driver.close()
                        assert True
                    else:
                        self.driver.save_screenshot(snap_path + "test_pw_change_wrong_old_password_login_error.png")
                        logger.error("******* Webpage is logined unexpectedly *******")
                        logger.error("******* test_password_change_wrong_old_password Test case is Failed *******")
                        self.lp.click_logout()
                        self.driver.close()
            else:
                self.driver.save_screenshot(snap_path + "test_password_change_wrong_old_password_error.png")
                logger.error("******** test_password_change Test case is failed somthing went wrong *******")
                self.driver.close()
                assert False
        except Exception as e1:
            self.driver.save_screenshot(snap_path + "test_password_change_wrong_old_password_issue.png")
            logger.error("******** test_password_change_wrong_old_password Test case is stopped - Refer belo logs "
                         "*******")
            logger.error(f"Page load failed: {str(e1)}")
            self.driver.switch_to.default_content()
            self.lp.click_logout()
            self.driver.close()
            assert False
