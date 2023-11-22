Rem ### This is for Automation run Script ###
@echo off

rem Activate the virtual environment
call venv\Scripts\activate

Rem ##########  Run the pytest command  ##########
Rem Note: You want to run Sanity or Regression... Un command the pytest cmd -> Remove "Rem"

Rem ### Sanity Test in Chrome ###
Rem pytest -v -s -m "Sanity" --html=Reports/report.html/ TestCases --browser edge

Rem ### Regression Test Chrome ###
Rem pytest -v -s -m "Regression" --html=Reports/report.html/ TestCases --browser edge

Rem ### Below cmd for Testing and R&D Purposes Default browser is edge
Rem pytest -v -s -m "Testing" --html=Reports/report.html/ TestCases --browser edge

Rem ### Below cmd for Sample run Default browser is edge
pytest -v -s -m "Sample" --html=Reports/report.html/ TestCases --browser edge

rem Deactivate the virtual environment
deactivate

