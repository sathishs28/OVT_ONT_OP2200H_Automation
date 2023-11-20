from selenium.webdriver.common.by import By


class AdminPage:
    READ_FIRMWARE_VER_XPATH = "//*[@id='header']/div[1]/table[3]/tbody/tr/td"

    CLICK_ADMIN_MAINMENU_XPATH = "//*[text()='Admin']"
    CLICK_ADMIN_SUBMENU_XPATH = "//a[@href='#']"
    CLICK_FIRMWARE_UPG_XPATH = "//*[text()='Firmware Upgrade']"

    SWITCH_WAN_INNER_NAME = "contentIframe"

    SEND_CHOOSE_FILE_XPATH = "//input[@name='binary']"
    CLICK_UPGRADE_XPATH = "//input[@name='send']"

    GET_FW_UPGRADING_PROCESS_DATA_XPATH = "//div[@id='progress-boader']"

    def __init__(self, driver):
        self.driver = driver

    def get_firmware_ver(self):
        return self.driver.find_element(By.XPATH, self.READ_FIRMWARE_VER_XPATH).text

    def click_admin_mainmenu(self):
        self.driver.find_element(By.XPATH, self.CLICK_ADMIN_MAINMENU_XPATH).click()

    def click_admin_submenu(self):
        self.driver.find_element(By.XPATH, self.CLICK_ADMIN_SUBMENU_XPATH).click()

    def click_firmware_upg(self):
        self.driver.find_element(By.XPATH, self.CLICK_FIRMWARE_UPG_XPATH).click()

    def switch_iframe(self):
        iframe = self.driver.find_element(By.NAME, self.SWITCH_WAN_INNER_NAME)
        self.driver.switch_to.frame(iframe)

    def send_choose_file(self, fw_file_path):
        # fw_file_path = "./Firmware/img.tar"
        # self.driver.find_element(By.XPATH, self.CLICK_ADMIN_MAINMENU_XPATH).clear()
        self.driver.find_element(By.XPATH, self.SEND_CHOOSE_FILE_XPATH).send_keys(fw_file_path)

    def click_upgrade(self):
        self.driver.find_element(By.XPATH, self.CLICK_UPGRADE_XPATH).click()

    def verify_progress_bar_ele(self):
        return self.driver.find_element(By.XPATH, self.GET_FW_UPGRADING_PROCESS_DATA_XPATH)

    def get_fw_upg_progress_status(self):
        return self.driver.find_element(By.XPATH, self.GET_FW_UPGRADING_PROCESS_DATA_XPATH).text
