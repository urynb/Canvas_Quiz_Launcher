## Readme

This project contains python scripts designed to use the Canvas REST API and work as teaching aids.

### Functionality
The script (quiz_launcher.py) gets a list of quizzes from a course, and lets the user pick a particular quiz to be unlocked for a certain number of minutes from the command line.

### Config
The script relies on specific values in the attached text file, config.txt

API_TOKEN=

BASE_URI=https://umsystem.instructure.com/api/v1

COURSE_ID=

Course ID should use the ID of the desired course. API token should use your access token.
The attached config file has a course ID of a test course.

### Running
python3 quiz_launcher.py

Select a quiz from the list that shows up by its index number.
For example:

1: Test Quiz 1

2: Test Quiz 2

would want an entry of '1' to select Test Quiz 1

Enter a time in minutes to unlock the quiz for that duration (starting from the current time).
