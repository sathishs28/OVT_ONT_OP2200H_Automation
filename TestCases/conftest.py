import pytest
import logging
import os
from selenium import webdriver
from datetime import datetime
from pytest_metadata.plugin import metadata_key
from Utilities.ReadProperties import ReadConfig


@pytest.fixture()
def setup(browser):
    if browser == "chrome":
        driver = webdriver.Chrome()
        driver.maximize_window()
        # Implicitly wait time is 10s - This is for Common global for all elements (Dynamic performs)
        driver.implicitly_wait(15)
        print("\n" "##### Chrome Browser is launching..... #####")
        # logger.info("******* Test Cases are testing under Chrome Browser *******")
    elif browser == "firefox":
        driver = webdriver.Firefox()
        driver.implicitly_wait(10)  # Implicitly wait time is 10 sec
        driver.maximize_window()
        print("\n" "##### Firefox Browser is launching.....#####")
        # logger.info("******* Test Cases are testing under Firefox Browser *******")
    elif browser == "edge":
        driver = webdriver.Edge()
        driver.implicitly_wait(10)  # Implicitly wait time is 10 sec
        driver.maximize_window()
        print("\n" "##### Microsoft Edge Browser is launching.....#####")
        # logger.info("******* Test Cases are testing under Firefox Browser *******")
    else:
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)  # Implicitly wait time is 10 sec
        driver.maximize_window()
        print("\n" "##### Default - Chrome Browser is launching.....#####")
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
    project_name, tester = ReadConfig.test_details()    # Get Test Details from config.ini
    session.config.stash[metadata_key]["Project Name"] = project_name
    session.config.stash[metadata_key]["Tester"] = tester


# It is hooked for delete/Modify Environment info to HTML Report
@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    metadata.pop("JAVA_HOME", None)
    metadata.pop("Plugins", None)
    metadata.pop("Packages", None)
    metadata.pop("Python", None)
