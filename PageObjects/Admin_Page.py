from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class AdminPage:
    """ Below Elements for Navigates to Admin page """
    CLICK_ADMIN_MAINMENU_XPATH = "//*[text()='Admin']"
    CLICK_ADMIN_SUBMENU_XPATH = "//a[@href='#']"

    """ Below Elements for Firmware update """
    READ_FIRMWARE_VER_XPATH = "//*[@id='header']/div[1]/table[3]/tbody/tr/td"
    CLICK_FIRMWARE_UPG_XPATH = "//*[text()='Firmware Upgrade']"

    SWITCH_WAN_INNER_NAME = "contentIframe"

    SEND_CHOOSE_FILE_XPATH = "//input[@name='binary']"
    CLICK_UPGRADE_XPATH = "//input[@name='send']"

    GET_FW_UPGRADING_PROCESS_DATA_XPATH = "//div[@id='progress-boader']"

    """ Below Elements for Password Change """
    CLICK_PASSWORD_XPATH = "//*[text()='Password']"
    SELECT_USERNAME_XPATH = "//select[@name='userMode']"
    SEND_OLD_PASSWORD_XPATH = "//input[@name='oldpass']"
    SEND_NEW_PASSWORD_XPATH = "//input[@name='newpass']"
    SEND_CONFORM_PASSWORD_XPATH = "//input[@name='confpass']"
    CLICK_APPLY_BTN_XPATH = "//input[@name='save']"
    GET_ERROR_STATUS_TAG = "h4"

    def __init__(self, driver):
        self.driver = driver

    def get_firmware_ver(self):
        return self.driver.find_element(By.XPATH, self.READ_FIRMWARE_VER_XPATH).text

    def click_admin_mainmenu(self):
        self.driver.find_element(By.XPATH, self.CLICK_ADMIN_MAINMENU_XPATH).click()

    def click_admin_submenu(self):
        self.driver.find_element(By.XPATH, self.CLICK_ADMIN_SUBMENU_XPATH).click()

    """ Below Methods for Firmware upgrade """

    def click_firmware_upg(self):
        self.driver.find_element(By.XPATH, self.CLICK_FIRMWARE_UPG_XPATH).click()

    def switch_iframe(self):
        iframe = self.driver.find_element(By.NAME, self.SWITCH_WAN_INNER_NAME)
        self.driver.switch_to.frame(iframe)

    def send_choose_file(self, fw_file_path):
        self.driver.find_element(By.XPATH, self.SEND_CHOOSE_FILE_XPATH).send_keys(fw_file_path)

    def click_upgrade(self):
        self.driver.find_element(By.XPATH, self.CLICK_UPGRADE_XPATH).click()

    def verify_progress_bar_ele(self):
        return self.driver.find_element(By.XPATH, self.GET_FW_UPGRADING_PROCESS_DATA_XPATH)

    def get_fw_upg_progress_status(self):
        return self.driver.find_element(By.XPATH, self.GET_FW_UPGRADING_PROCESS_DATA_XPATH).text

    """ Below Methods for Password Change """

    def click_password_change(self):
        self.driver.find_element(By.XPATH, self.CLICK_PASSWORD_XPATH).click()

    def select_username(self, username):
        list_username = Select(self.driver.find_element(By.XPATH, self.SELECT_USERNAME_XPATH))
        list_username.select_by_visible_text(username)

    def send_old_password(self, old_password):
        self.driver.find_element(By.XPATH, self.SEND_OLD_PASSWORD_XPATH).clear()
        self.driver.find_element(By.XPATH, self.SEND_OLD_PASSWORD_XPATH).send_keys(old_password)

    def send_new_password(self, new_password):
        self.driver.find_element(By.XPATH, self.SEND_NEW_PASSWORD_XPATH).clear()
        self.driver.find_element(By.XPATH, self.SEND_NEW_PASSWORD_XPATH).send_keys(new_password)

    def send_conform_password(self, conform_password):
        self.driver.find_element(By.XPATH, self.SEND_CONFORM_PASSWORD_XPATH).clear()
        self.driver.find_element(By.XPATH, self.SEND_CONFORM_PASSWORD_XPATH).send_keys(conform_password)

    def click_apply_btn(self):
        self.driver.find_element(By.XPATH, self.CLICK_APPLY_BTN_XPATH).click()

    def get_pw_change_error_status(self):
        return self.driver.find_element(By.TAG_NAME, self.GET_ERROR_STATUS_TAG).text
