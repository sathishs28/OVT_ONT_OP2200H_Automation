from selenium.webdriver.common.by import By


class LoginPage:
    Home_Page_Logo_XPATH = "//tr[@valign='top']//td//a//img"
    Login_Username_XPATH = "//input[@name='username']"
    Login_Password_XPATH = "//input[@name='password']"
    Click_Login_Button_XPATH = "//input[@name='save']"
    Click_Logout_Button_XPATH = "//input[@value='Logout']"
    Login_Error_Message_XPATH = "/html/body/blockquote/table/tbody/tr[1]/td/h4"

    def __init__(self, driver):
        self.driver = driver

    def home_page_logo(self):
        return self.driver.find_element(By.XPATH, self.Home_Page_Logo_XPATH)

    def set_username(self, username):
        self.driver.find_element(By.XPATH, self.Login_Username_XPATH).clear()
        self.driver.find_element(By.XPATH, self.Login_Username_XPATH).send_keys(username)

    def set_password(self, password):
        self.driver.find_element(By.XPATH, self.Login_Password_XPATH).clear()
        self.driver.find_element(By.XPATH, self.Login_Password_XPATH).send_keys(password)

    def click_login(self):
        self.driver.find_element(By.XPATH, self.Click_Login_Button_XPATH).click()

    def get_login_element(self):
        return self.driver.find_element(By.XPATH, self.Click_Login_Button_XPATH)

    def click_logout(self):
        self.driver.find_element(By.XPATH, self.Click_Logout_Button_XPATH).click()

    def get_logout_element(self):
        return self.driver.find_element(By.XPATH, self.Click_Logout_Button_XPATH)

    def login_error(self):
        return self.driver.find_element(By.XPATH, self.Login_Error_Message_XPATH).text

    def login(self, username, password):
        self.set_username(username)
        self.set_password(password)
        self.click_login()
