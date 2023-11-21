### This is an Automation project for ONT web application testing ###

Requirement:
    To run this automation project, you need to install the following packages and plugins

    1. selenium - Selenium Libraries
    2. pytest - Pytest for Unittest framework
    3. pytest-html - It's for generating html report
    4. pytest-xdist - Run tests parallel
    5. openpyxl - MS Excel support
    6. allure-pytest - to generate allure reports

*** For Fresh Setup in New PC ***

Step 1. Share Your Code and install Python V3.11 or higher version
    1. https://github.com/sathishs28/OVT_ONT_OP2200H_Automation.git

    2. And install the Python V3.11 or higher version

Step 2. Set Up a Virtual Environment:
    1. Open a terminal or command prompt on the other PC.

    2. Navigate to your project directory using the cd command:
        cd path/to/your/project

    3. Create a new virtual environment:
        python -m venv venv

    4. Activate the virtual environment:
        venv\Scripts\activate

Step 3. Install Project Dependencies:
    pip install -r requirements.txt

Step 4. Run Your Python Project:
    Edit and run -> run.bat  (Open the run.bat -> It's run automatically)

    1. Before run the automation "run.bat" configure the project and device details in Configuration (folder) - config.ini
    2. Set the marks desired test cases (from each module - test cases)
    3. After run the run.bat file with specified single cmd (there have multiple cmds based on the project test cases).





