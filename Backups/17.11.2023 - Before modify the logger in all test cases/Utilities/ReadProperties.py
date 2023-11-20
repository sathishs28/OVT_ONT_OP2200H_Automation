import os
import configparser

relative = "./Configurations/config.ini"

path = os.path.abspath(relative)
config = configparser.RawConfigParser()
config.read(path)


class ReadConfig:

    @staticmethod
    def get_device_url():
        return config.get('Device_Login', "Device_URL")

    @staticmethod
    def get_username():
        return config.get("Device_Login", "username")

    @staticmethod
    def get_password():
        return config.get("Device_Login", "password")

    @staticmethod
    def get_login_page_title():
        return config.get("Device_HTML_Page_Title", "Login_Page")

    @staticmethod
    def get_dashboard_title():
        return config.get("Device_HTML_Page_Title", "Dashboard_Page")


"""
# Sample Test
    @staticmethod
    def get_device_credential():
        config = configparser.ConfigParser()
        config.read("config.ini")
        url = config.get("Device Login", "Device_URL")
        username = config.get("Device Login", "username")
        password = config.get("Device Login", "password")
        return url, username, password

"""

# print(ReadConfig.get_device_url())
# print(ReadConfig.get_password(), ReadConfig.get_username())

# print(ReadConfig.get_device_url(), "\n", ReadConfig.get_password(), "\n", ReadConfig.get_username())
# print(ReadConfig.get_dashboard_title())
