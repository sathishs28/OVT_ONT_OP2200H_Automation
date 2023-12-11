import logging
import os
from datetime import datetime

import pytest
from pytest_metadata.plugin import metadata_key
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from Utilities.ReadProperties import ReadConfig

download_dir_relative = "./Backups/"
download_dir = os.path.abspath(download_dir_relative)


@pytest.fixture()
def setup(browser, wait_time=15):
    # browser = browser.lower()  # Convert to lowercase for case-insensitivity
    # Create the log directory if it doesn't exist
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    # Set up Common Browser options for handling file downloads
    common_options = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": True,
        "safebrowsing.enabled": True
    }
    # Following have webdriver setup - Input choose browser from pytest cmd "pytest --browser chrome"
    if browser == "chrome":
        options = ChromeOptions()
        options.add_experimental_option("prefs", common_options)
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        # Implicitly wait time is 10s - This is for Common global for all elements (Dynamic performs)
        driver.implicitly_wait(wait_time)
        print("\n" "##### Chrome Browser is launching..... #####")
        # logger.info("******* Test Cases are testing under Chrome Browser *******")
    elif browser == "firefox":
        firefox_options = FirefoxOptions()
        # Set preferences for file downloads
        firefox_options.set_preference("browser.download.folderList", 2)  # 0: Desktop, 1: Downloads, 2: Custom Location
        firefox_options.set_preference("browser.download.dir", download_dir)
        firefox_options.set_preference("browser.download.useDownloadDir", True)
        firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                       "application/octet-stream")  # MIME type to auto-download
        driver = webdriver.Firefox(options=firefox_options)
        driver.implicitly_wait(wait_time)  # Implicitly wait time is 10 sec
        driver.maximize_window()
        print("\n" "##### Firefox Browser is launching.....#####")
        # logger.info("******* Test Cases are testing under Firefox Browser *******")
    elif browser == "edge":
        driver = webdriver.Edge()
        driver.implicitly_wait(wait_time)  # Implicitly wait time is 10 sec
        driver.maximize_window()
        print("\n" "##### Microsoft Edge Browser is launching.....#####")
        # logger.info("******* Test Cases are testing under Firefox Browser *******")
    else:
        # Set preferences for file downloads (
        """ When using this edge browser with download set dir not completed fully.
            Getting pop-up when downloading a file, currently i can't find the fix for disable the pop-up
            Later will update.
            Note: Currently do not use the edge browser for downloading related test cases
        """
        edge_options = EdgeOptions()
        edge_options.add_experimental_option("prefs", common_options)
        driver = webdriver.Edge(options=edge_options)
        driver.implicitly_wait(wait_time)  # Implicitly wait time is 10 sec
        driver.maximize_window()
        print("\n" "##### Default - Edge Browser is launching.....#####")
        # logger.info("******* Test Cases are testing under IE (Default) *******")
    return driver


def pytest_addoption(parser):  # This function will get the value from CLI /hooks
    parser.addoption("--browser")


@pytest.fixture()
def browser(request):  # This will return the Browser value to set up method
    return request.config.getoption("--browser")


# ########### Below fixture is for generating log file ################ #

relative_log_path = "./Logs/"
log_path = os.path.abspath(relative_log_path)


@pytest.fixture(scope="session")
def logger(request, log_directory=log_path):
    # Create the log directory if it doesn't exist
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Extract the marker name from the command line options
    marker_name = request.config.getoption("-m")

    # Get the current date and time for the log filename
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = os.path.join(log_directory, f"Automation_{'' + marker_name if marker_name else ''}"
                                               f"_Test_Log_{current_datetime}.log")

    # Create a logger and configure it
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create a formatter for the log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create a file handler to write logs to the file
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)
    return logger


# ########### END ################ #

# Custom title for report generation (from the Marker - Test type)
def pytest_html_report_title(report):
    marker_name = report.config.getoption("-m") or 'default'
    report.title = f"{marker_name} - Automation Test Report"


# It is hooked for Adding Environment info to HTML Report
@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session):
    project_name, tester = ReadConfig.test_details()  # Get Test Details from config.ini
    session.config.stash[metadata_key]["Project Name"] = project_name
    session.config.stash[metadata_key]["Tester"] = tester


# It is hooked for delete/Modify Environment info to HTML Report
@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    metadata.pop("JAVA_HOME", None)
    metadata.pop("Plugins", None)
    metadata.pop("Packages", None)
    metadata.pop("Python", None)
