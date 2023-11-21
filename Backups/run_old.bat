Rem ### This is for Automation run Script ###

Rem ### Sanity Test in Chrome ###
Rem pytest -v -s -m "sanity" --html=Reports\report.html TestCases\ --browser chrome

Rem ### Regression Test Chrome ###
Rem pytest -v -s -m "regression" --html=Reports/report.html/ TestCases --browser chrome


Rem ######################## This is for Internal Testing purpose ###########################

Rem pytest -v -s -m "sanity" --html=Reports\report.html TestCases\Test_Login_001.py --browser chrome
rem pytest -v -s -m "regression" --html=Reports\report.html TestCases\Test_Login_001.py --browser chrome
Rem pytest -v -s -m "sanity" --html=Reports\report.html TestCases\Test_Login_DDT_002.py --browser edge

Rem pytest -v -s -m "sanity" --html=Reports\report.html TestCases\Test_New_WAN_003.py --browser chrome

Rem pytest -v -s -m "sanity" --html=Reports\report.html TestCases\Test_004_Delete_WAN.py --browser chrome

Rem pytest -v -s -m "sanity" --html=Reports\report.html TestCases --browser chrome

Rem pytest -v -s -m "regression" --html=Reports\report.html TestCases --browser chrome

Rem pytest -v -s -m "smoke2" --html=.Reports\report.html TestCases --browser chrome

Rem pytest -v -s -m "smoke2" --html=.Reports\report.html\ .\TestCases\ --browser chrome

Rem pytest -v -s -m "sanity" --html=Reports/report.html/ TestCases --browser chrome

Rem pytest -v -s -m "regression" --html=Reports/report.html/ TestCases --browser chrome

pytest -v -s -m "Testing" --html=Reports/report.html/ TestCases --browser edge

Rem pytest -v -s TestCases\Test_New_WAN_003.py --browser chrome



