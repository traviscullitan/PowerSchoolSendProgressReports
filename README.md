# PowerSchoolSendProgressReports
This program manually sends progress reports from PowerSchool to parents based on a tab delimited list of parents and students

This program requires the Python 3 and the Selenium module:
pip install selenium

The WebDriver for Chrome is also required:
https://sites.google.com/a/chromium.org/chromedriver/

Rename the config.ini.example file to config.ini and put in your site's settings.

The tab delimited input should have the column names in the first row and have the following columns:

FIRSTNAME|LASTNAME|EMAIL|LAST_SENT_DATE|GUARDIANID|STUDENT_NAME
---|---|---|---|---|---
Joe|Doe|joe@parent.com|2018-1-1|500000|Doe, Jimmy Allan
Jane|Doe|jane@parent.com|2018-12-1|500001|Doe, Sarah Lynn

