import os
import time
import pytest
from pathlib import Path
from selenium.webdriver.common.alert import Alert
from Utilities.ReadProperties import ReadConfig
from PageObjects.Login_Page import LoginPage
from PageObjects.Admin_Page import AdminPage

snap_path = "./ScreenShots/"

# Relative path
firmware_relative_path = "./Firmware/img.tar"
# Convert to an absolute path
fw_file_path = os.path.abspath(firmware_relative_path)  # From Upload file element getting an absolute path only


class Test_000_Firmware_Upgrade:
    device_URL = ReadConfig.get_device_url()
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()

    @pytest.mark.Sanity
    @pytest.mark.Regression
    def test_firmware_upgrade(self, setup, logger):
        logger.info("************* Test_000_Firmware_Upgrade :: test_firmware_upgrade *************")
        try:
            self.driver = setup
            self.driver.get(self.device_URL)

            # Login Device
            self.lp = LoginPage(self.driver)
            self.lp.login(self.username, self.password)

            # Navigate to Admin Page
            self.ap = AdminPage(self.driver)
            bf_fw_ver = self.ap.get_firmware_ver()
            # print(bf_fw_ver)
            logger.info(f"******** Current device running firmware version - {bf_fw_ver} **************")
            self.ap.click_admin_mainmenu()
            self.ap.click_admin_submenu()
            self.ap.click_firmware_upg()
            logger.info("******** test_firmware_upgrade Test case is starting ********")

            # New Firmware file upload and click upgrade
            # Verify the firmware file is present or not
            def is_file_present(file_path):
                return Path(file_path).is_file()

            if is_file_present(fw_file_path):
                logger.info(f"******** test_firmware_upgrade the fw file '{fw_file_path}' is present *******")
                logger.info("******** test_firmware_upgrade - New firmware is going to update ********")
                self.ap.switch_iframe()  # Switch to Inner frame of another HTML document
                self.ap.send_choose_file(fw_file_path)
                self.ap.click_upgrade()
                # Wait for the pop-up to appear
                alert = Alert(self.driver)
                # Access the text of the alert
                # print("Alert Text:", alert.text)
                # Accept the alert (click OK)
                alert.accept()
                time.sleep(8)
                # Check the FW Upgrading status bar element
                if self.ap.verify_progress_bar_ele().is_displayed():
                    logger.info("******** Firmware upgrading process is starting *******")
                    # self.ap.get_fw_upg_progress_status()
                    i = 0
                    while i <= 99:
                        i = int(self.ap.get_fw_upg_progress_status().rstrip('%'))
                        logger.info(f"******** Firmware upgrading - {i}% **************")
                        time.sleep(1)
                    logger.info("******** Firmware upgraded - 100% Successfully *******")
                    # After updated verify the latest firmware version
                    # self.driver.close()
                    self.driver.refresh()
                    # Verify the homepage
                    self.lp = LoginPage(self.driver)  # lp -> LoginPage object stored in lp object
                    logo_element = self.lp.home_page_logo()
                    if logo_element.is_displayed():
                        logger.info("******* Homepage is loaded *******")
                    else:
                        logger.error("******* Homepage is not loaded - Something wrong *******")
                        self.driver.save_screenshot(snap_path + "test_firmware_upgrade_af_upg_homepage_error.png")
                        return
                    # Login and get the latest-updated firmware version
                    self.lp.login(self.username, self.password)
                    af_fw_ver = self.ap.get_firmware_ver()
                    if bf_fw_ver != af_fw_ver:
                        logger.info(f"******* Latest updated firmware version - {af_fw_ver} *******")
                        logger.info("******** test_firmware_upgrade Test case is completed & Success ********")
                        self.lp.click_logout()
                        self.driver.close()
                        assert True
                    else:
                        logger.error(f"******* Latest updated firmware is still same - Check Firmware *******")
                        logger.error("******** test_firmware_upgrade Test case is Failed ********")
                        self.driver.save_screenshot(snap_path + "test_firmware_upgrade_after_upg_ver_issue.png")
                        self.lp.click_logout()
                        self.driver.close()
                        assert False
                else:
                    self.driver.save_screenshot(snap_path + "test_firmware_upgrade_progress_status_error.png")
                    logger.info("******** Firmware upgrading process is not showing *******")
                    return
            else:
                logger.error(f"******* test_firmware_upgrade the fw file '{fw_file_path}' is not present *******")

                logger.error("******** test_firmware_upgrade Test case is stopped ********")
                self.driver.switch_to.default_content()
                self.lp.click_logout()
                self.driver.close()
                assert False
            self.driver.quit()
        except Exception as e1:
            self.driver.save_screenshot(snap_path + "test_firmware_upgrade_issue.png")
            logger.error("******** test_firmware_upgrade Test case is stopped - Refer belo logs *******")
            logger.error(f"Page load failed: {str(e1)}")
            self.driver.switch_to.default_content()
            self.lp.click_logout()
            self.driver.close()
            assert False
