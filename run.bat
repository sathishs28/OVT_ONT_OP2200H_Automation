Rem ### This is for Automation run Script ###
@echo off

rem Activate the virtual environment
call venv\Scripts\activate

Rem ##########  Run the pytest command  ##########
Rem ### Sanity Test in Chrome ###
Rem pytest -v -s -m "Sanity" --html=Reports/report.html/ TestCases --browser chrome

Rem ### Regression Test Chrome ###
Rem pytest -v -s -m "Regression" --html=Reports/report.html/ TestCases --browser chrome

Rem ### Default browser is edge
pytest -v -s -m "Testing" --html=Reports/report.html/ TestCases --browser edge

Rem Note: U want to run Sanity or Regression... Un command the pytest cmd -> Remove "Rem"
rem Deactivate the virtual environment
deactivate

