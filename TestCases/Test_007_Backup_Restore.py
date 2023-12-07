import os
import time
import pytest
import requests
from selenium.webdriver.common.by import By
from PageObjects.Login_Page import LoginPage
from PageObjects.Admin_Page import AdminPage
from Utilities.ReadProperties import ReadConfig
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

snap_path = "./ScreenShots/"
download_dir_relative = "./Backups/"
download_path = os.path.abspath(download_dir_relative)


def get_list_files():
    try:
        files = [f for f in os.listdir(download_path)]
        return files
    except FileNotFoundError:
        print(f"Directory not found: {download_path}")
        return []


class Test_007_Backup_Restore:
    device_URL = ReadConfig.get_device_url()
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()

    # Default login credentials
    default_url, default_username, default_password = ReadConfig.default_login_credentials()

    """ Class-level variable to track the result of backup & restore test cases
        Note: Below these two methods are not test cases """
    test_1_backup_config_file_failed = False
    test_2_reset_configuration_failed = False

    @pytest.fixture
    def test_1_backup_config_file_result(self, request):
        yield
        self.__class__.test_1_backup_config_file_failed = request.node.session.testsfailed > 0

    @pytest.fixture
    def test_2_reset_configuration_result(self, request):
        yield
        self.__class__.test_2_reset_configuration_failed = request.node.session.testsfailed > 0

    """ Below methods are Test cases script """

    @pytest.mark.Sanity
    @pytest.mark.Regression
    @pytest.mark.Smoke
    def test_1_backup_config_file(self, setup, logger, test_1_backup_config_file_result):
        logger.info("************* Test_007_Backup_Restore :: test_1_backup_config_file *************")
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
            self.ap.click_backup_restore_opt()

            # Backup the current running config file
            bf_len_backup = len(get_list_files())  # Get the length of backup directory
            self.ap.switch_iframe()  # Switch to iframe
            self.ap.click_backup_btn()  # This element is in iframe
            logger.info("******* Backup current configuration is started & Clicked backup button... *******")
            # Processing and waiting for downloading...
            max_wait_time = 60  # Set wait time in seconds
            i = 0
            while i <= max_wait_time:
                af_backup_files = get_list_files()
                af_len_backup = len(af_backup_files)
                if bf_len_backup != af_len_backup:
                    latest_file = max(af_backup_files, key=lambda f: os.path.getctime(os.path.join(download_path, f)))
                    if latest_file.endswith(".xml"):
                        logger.info(f"Latest Downloaded file in Backup folder...{latest_file}")
                        logger.info("******* test_1_backup_config_file Test case is Passed *******")
                        assert True
                        break
                    elif latest_file.endswith(".crdownload"):
                        logger.info(f"New downloading file in progress...{latest_file}")
                    else:
                        logger.info(f"Unknown File detected in Backup folder...{latest_file}")
                time.sleep(1)
                i += 1

            # Verify the below condition if the maximum wait time is reached
            backup_files = get_list_files()
            if i > max_wait_time:
                get_latest_file = max(backup_files, key=lambda f: os.path.getctime(os.path.join(download_path, f)))
                if bf_len_backup == len(backup_files):
                    logger.error(f"Timeout reached ({max_wait_time} seconds). And Downloading is not started...")
                    logger.error("******* test_1_backup_config_file Test case is Failed *******")
                elif bf_len_backup != len(backup_files):
                    logger.error(f"Timeout reached ({max_wait_time} seconds). And Downloading is not Completed...")
                    logger.error(f"This is last partially downloading file ({get_latest_file}). And Downloading is not "
                                 f"Completed...")
                    logger.error("******* test_1_backup_config_file Test case is Failed *******")
                assert False

            # Switch back from iframe
            self.driver.switch_to.default_content()
            self.lp.click_logout()
            self.driver.close()
        except Exception as e1:
            self.driver.save_screenshot(snap_path + "test_1_backup_config_file_page_issue.png")
            logger.error("******** test_1_backup_config_file Test case is stopped - Refer belo logs *******")
            logger.error(f"Page load failed: {str(e1)}")
            self.driver.switch_to.default_content()
            self.lp.click_logout()
            self.driver.close()
            assert False

    @pytest.mark.Sanity
    @pytest.mark.Regression
    @pytest.mark.Smoke
    # @pytest.mark.skipif("not test_1_backup_config_file", reason="Skipping if test_1_backup_config_file failed")
    def test_2_reset_configuration(self, setup, logger, test_2_reset_configuration_result):
        # For Skipping the test case if the directory is empty and if test_1_backup_config_file Fail
        if not get_list_files():
            pytest.skip(f"***** Device Configuration Backup Directory is empty (no such file) - {download_path}")
        elif self.__class__.test_1_backup_config_file_failed:
            pytest.skip('Skipping Test case - test_2_reset_configuration. Because test_1_backup_config_file Failed')

        logger.info("************* Test_007_Backup_Restore :: test_2_reset_configuration *************")
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
            self.ap.click_backup_restore_opt()

            # Reset the current running configuration
            # Before reset the configuration verify the latest config backup is there or not
            logger.info("******* Verifying the latest backup configuration file present or not *******")
            get_latest_file = max(get_list_files(), key=lambda f: os.path.getctime(os.path.join(download_path, f)))
            if get_latest_file.endswith(".xml"):
                logger.info(f"******* Latest backup configuration file is there. File - {get_latest_file} *******")
                logger.info("******* test_2_reset_configuration Test case is starting *******")
                self.ap.switch_iframe()  # Switch to iframe
                self.ap.click_reset_btn()

                # Wait for the pop-up to appear
                alert = Alert(self.driver)
                alert.accept()
                reset_status = self.ap.get_status_af_reset_btn_click()
                logger.info(f"******* After click reset button, Refer below status *******\nStatus:-\n{reset_status}")
                time.sleep(60)  # This sleep time for performing the device resetting & N/w est. to PC (It's mandatory)

                # After factory-reset, verify the Homepage in New Tab (Open to the default web URL)
                wait = WebDriverWait(self.driver, 10)  # Set up an explicit wait with a max timeout of 10 secs
                loop_count, delay = 5, 1  # 1st variable is no.of time loop & 2nd variable is delay time in secs
                for _ in range(loop_count):
                    logger.info(f"****** After test_reset_config, {_ + 1}st Try to open the Webpage using Default IP "
                                f"******")
                    try:
                        self.driver.get(self.default_url)
                        # Waiting for Home page logo & Login Button element (Explicit wait setup)
                        wait.until(EC.presence_of_element_located((By.XPATH, self.lp.Home_Page_Logo_XPATH)))
                        wait.until(EC.presence_of_element_located((By.XPATH, self.lp.Click_Login_Button_XPATH)))

                        if self.lp.home_page_logo().is_displayed() and self.lp.get_login_element().is_displayed():
                            logger.info("******* Webpage is loaded successfully  *******")
                            logger.info("******* After test_reset_config Homepage & Login Element Test success *******")
                            break
                    except requests.ConnectionError:
                        logger.error("******* Failed to establish Webpage connection *******")
                    except Exception as e:
                        logger.error(f"An error occurred: {e}")
                    if _ == loop_count - 1:
                        logger.error("******* Reloaded the Webpage, It is Not opening (Failed)...! *******")
                        logger.error("******* After test_2_reset_configuration Test case is Failed *******")
                        self.driver.close()
                        assert False
                    time.sleep(delay)
                    logger.info("******* Re-tyring to open the Webpage... *******")

                # Then, Try to Log in Device using default credentials and verify the logout element
                self.lp.login(self.default_username, self.default_password)
                if self.lp.get_logout_element().is_displayed():
                    assert True
                    logger.info("******* After test_reset_config Login Test success *******")
                    logger.info("******* After test_2_reset_configuration Test Case is Passed *******")
                    self.lp.click_logout()
                    self.driver.close()
                else:
                    logger.error("******* After test_reset_config Login test Failed *******")
                    logger.error("******* After test_2_reset_configuration Test case is Failed *******")
                    self.driver.close()
                    assert False
            else:
                logger.error("******* Latest backup configuration file is not there...! *******")
                logger.error("******* test_2_reset_configuration Test Case is not completed *******")
                self.driver.switch_to.default_content()
                self.lp.click_logout()
                self.driver.close()
                assert False
        except Exception as e2:
            self.driver.save_screenshot(snap_path + "test_2_reset_configuration_page_issue.png")
            logger.error("******** test_2_reset_configuration Test case is stopped - Refer belo logs *******")
            logger.error(f"Page load failed: {str(e2)}")
            self.driver.switch_to.default_content()
            self.lp.click_logout()
            self.driver.close()
            assert False

    @pytest.mark.Sanity
    @pytest.mark.Regression
    @pytest.mark.Smoke
    def test_3_restore_configuration(self, setup, logger):
        # For Skipping the test case if the directory is empty and if test_2_reset_configuration Fail
        if not get_list_files():
            pytest.skip(f"***** Device Configuration Backup Directory is empty (no such file) - {download_path}")
        elif self.__class__.test_1_backup_config_file_failed:
            pytest.skip('Skipping Test case - test_2_reset_configuration. Because test_1_backup_config_file Failed')
        elif self.__class__.test_2_reset_configuration_failed:
            pytest.skip('Skipping Test case - test_3_restore_configuration. Because test_2_reset_configuration Failed')

        logger.info("************* Test_007_Backup_Restore :: test_3_restore_configuration *************")
        try:
            # Note: After factory reset the device, use default login credentials
            self.driver = setup
            self.driver.get(self.default_url)

            # Login Device
            self.lp = LoginPage(self.driver)
            self.lp.login(self.default_username, self.default_password)

            # Navigate to Admin Page
            self.ap = AdminPage(self.driver)
            self.ap.click_admin_mainmenu()
            self.ap.click_admin_submenu()
            self.ap.click_backup_restore_opt()

            # Restore the last backup configuration file (.xml)
            get_latest_file = max(get_list_files(), key=lambda f: os.path.getctime(os.path.join(download_path, f)))
            logger.info("******* Verifying the last backup file is present or not *******")
            if get_latest_file.endswith(".xml"):
                logger.info(f"******* The last backup file is there, File - {get_latest_file} *******")
                self.ap.switch_iframe()
                self.ap.choose_send_backup_file(download_path + "/" + get_latest_file)
                self.ap.click_restore_btn()
                reset_status = self.ap.get_status_af_reset_btn_click()
                logger.info(f"******* After click reset button, Refer below status *******\nStatus:-\n{reset_status}")
                time.sleep(60)  # This sleep time for performing the device restoring the last backup (It's mandatory)

                # After restore the backup, verify the backup configuration
                wait = WebDriverWait(self.driver, 10)  # Set up an explicit wait with a max timeout of 10 secs
                loop_count, delay = 5, 1  # 1st variable is no.of time loop & 2nd variable is delay time in secs
                for _ in range(loop_count):
                    logger.info(f"****** After test_reset_config, {_ + 1}st Try to open the Webpage using Device "
                                f"configured IP ******")
                    try:
                        self.driver.get(self.device_URL)
                        # Waiting for Home page logo & Login Button element (Explicit wait setup)
                        wait.until(EC.presence_of_element_located((By.XPATH, self.lp.Home_Page_Logo_XPATH)))
                        wait.until(EC.presence_of_element_located((By.XPATH, self.lp.Click_Login_Button_XPATH)))

                        if self.lp.home_page_logo().is_displayed() and self.lp.get_login_element().is_displayed():
                            logger.info("******* Webpage is loaded successfully  *******")
                            logger.info(
                                "******* After test_restore_config Homepage & Login Element Test success *******")
                            break
                    except requests.ConnectionError:
                        logger.error("******* Failed to establish Webpage connection *******")
                    except Exception as e:
                        logger.error(f"An error occurred: {e}")
                    if _ == loop_count - 1:
                        logger.error("******* Reloaded the Webpage, It is Not opening (Failed)...! *******")
                        logger.error("******* After test_3_restore_configuration Test case is Failed *******")
                        self.driver.close()
                        assert False
                    time.sleep(delay)
                    logger.info("******* Re-tyring to open the Webpage... *******")

                # Try to Log-in Device using last backup config credentials and verify the logout element
                self.lp.login(self.username, self.password)
                if self.lp.get_logout_element().is_displayed():
                    assert True
                    logger.info("******* After test_restore_config Login Test success *******")
                    logger.info("******* After test_3_restore_configuration Test Case is Passed *******")
                    self.lp.click_logout()
                    self.driver.close()
                else:
                    logger.error("******* After test_restore_config Login test Failed *******")
                    logger.error("******* After test_3_restore_configuration Test case is Failed *******")
                    self.driver.close()
                    assert False
            else:
                logger.error("******* Latest backup configuration file is not there...! *******")
                logger.error("******* test_3_restore_configuration Test Case is not completed *******")
                self.driver.switch_to.default_content()
                self.lp.click_logout()
                self.driver.close()
                assert False
        except Exception as e1:
            self.driver.save_screenshot(snap_path + "test_3_restore_configuration_page_issue.png")
            logger.error("******** test_3_restore_configuration Test case is stopped - Refer belo logs *******")
            logger.error(f"Page load failed: {str(e1)}")
            self.driver.switch_to.default_content()
            self.lp.click_logout()
            self.driver.close()
            assert False
