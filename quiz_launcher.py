import requests
import os
from datetime import datetime, timedelta

# Retrieve API token / URI from file
# the main function will call this for a 'config.txt' file in the same directory
# it should have fields for API token, base URI and course ID.
# BASE_URI=https://umsystem.instructure.com/api/v1
def get_api_details(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__)) 
    file_path = os.path.join(script_dir, file_name) 

    with open(file_path, 'r') as file:
        lines = file.readlines()
        details = {}
        for line in lines:
            key, value = line.strip().split('=')
            details[key] = value
        return details['API_TOKEN'], details['BASE_URI'], details['COURSE_ID']

# makes a get request for the list of quizzes, and displays the list
# index is incremented by 1 to avoid 0 index in the list
def get_quizzes(api_token, base_uri, course_id):
    url = f"{base_uri}/courses/{course_id}/quizzes"
    headers = {'Authorization': f"Bearer {api_token}"}
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        quizzes = response.json()
        for i, quiz in enumerate(quizzes):
            print(f"{i + 1}: {quiz['title']}")
        return quizzes
    else:
        print(f"Failed to retrieve quizzes: {response.status_code}")
        return None

# let the user select a quiz by number
def get_user_quiz_choice(quizzes):
    if not quizzes:
        return None
    quiz_number = int(input("Enter the number of the quiz you want to open: "))
    if 1 <= quiz_number <= len(quizzes):
        selected_quiz = quizzes[quiz_number - 1]
        return selected_quiz['id'], selected_quiz['title']
    else:
        print("Invalid choice.")
        return None

# open the selected quiz for the specified time
def open_quiz(api_token, base_uri, course_id, quiz_id, quiz_title, target_time):
    url = f"{base_uri}/courses/{course_id}/quizzes/{quiz_id}"
    headers = {'Authorization': f"Bearer {api_token}"}
    
    now = datetime.utcnow()
    unlock_at = now.isoformat() + 'Z'
    lock_at = (now + timedelta(minutes=target_time)).isoformat() + 'Z'
    
    payload = {
        'quiz': {
            'unlock_at': unlock_at,
            'lock_at': lock_at,

            # also changes the displayed due date; meaning that the quiz entry shouldn't be flagged as a late submission
            # may not be desirable always, for example if allowing a student to submit late we may want the submission to be flagged as late
            'due_at': lock_at
        }
    }
    
    response = requests.put(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print(f"Quiz '{quiz_title}' is now open for {target_time} minutes.")
    else:
        print(f"Failed to open quiz: {response.status_code}")

def main():
    # Read API details
    api_token, base_uri, course_id = get_api_details('config.txt')

    # Get quizzes and display them
    quizzes = get_quizzes(api_token, base_uri, course_id)
    
    if quizzes:
        # User selects a quiz
        selected_quiz = get_user_quiz_choice(quizzes)
        
        if selected_quiz:
            quiz_id, quiz_title = selected_quiz
            
            target_time = int(input("Enter the number of minutes to keep the quiz open: "))
            open_quiz(api_token, base_uri, course_id, quiz_id, quiz_title, target_time)
        else:
            print("No valid quiz selected.")
    else:
        print("No quizzes available.")

if __name__ == "__main__":
    main()
