# PowerSchoolSendProgressReports
When finished, this program will manually send progress reports to parents based on a tab delimited list of parents and students

This program require the Selenium module for Python:
pip install selenium

The WebDriver for Chrome is also required:
https://sites.google.com/a/chromium.org/chromedriver/

Rename the config.ini.example file to config.ini and put in your site's settings.

The tab delimited input should have the column names in the first row and have the following columns:
FIRSTNAME	LASTNAME	EMAIL	LAST_SENT_DATE	GUARDIANID	STUDENT_NAME	GRADE_LEVEL
