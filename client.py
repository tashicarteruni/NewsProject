import requests
from datetime import date as dt

url = None

# Create a session object
session = requests.Session()

def check_login_status(url):

    if url is None:
        print("URL is not set. Please log in first.")
        return False

    # Define the URL of the endpoint to check login status
    check_status_url = url + '/api/check_status'

    # Send a GET request to the endpoint using the session
    response = session.get(check_status_url)

    # Check the response status code
    if response.status_code == 200:
        # Extract username from the response JSON data
        username = response.json().get('username')
        if username:
            return True
        else:
            return False
    else:
        print("Failed to check login status.")
        return False


def login(url_input):
    global session  # Declare session as global so it can be modified inside the function

    if check_login_status(url):
        print("You are already logged in.")
        return True

    # Define the login URL
    login_url = url_input.strip('/') + '/api/login'

    # Prompt the user to enter username and password
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Define the login data with user-provided username and password
    login_data = {
        'username': username,
        'password': password
    }

    # Send the POST request to the login endpoint with data in the request body using the session
    response = session.post(login_url, data=login_data)

    # Check the response status code
    if response.status_code == 200:
        print("Login successful!")
        # Extract username from the response JSON data
        data = response.json()
        username = data.get('username')
        if username:
            print(f"You are logged in as {username}.")
        else:
            print("You are logged in, but the username is unknown.")
        return True
    else:
        print("Login failed!")
        print("Error:", response.text)  # Print the error message
        return False

def logout():
    global session  # Declare session as global so it can be modified inside the function

    if not check_login_status():
        print("You are already logged out.")
        return True

    # Define the logout URL
    logout_url = 'http://127.0.0.1:8000/api/logout'

    # Send the POST request to the logout endpoint using the session
    response = session.post(logout_url)

    # Check the response status code
    if response.status_code == 200:
        print("Logout successful!")
        return True
    else:
        print("Logout failed!")
        return False

def post_story(url):
    global session
    # Define the predefined options for category and region
    CATEGORY_CHOICES = ['pol', 'art', 'tech', 'trivia']
    REGION_CHOICES = ['uk', 'eu', 'w']

    # Define the URL of the endpoint to post a story
    post_story_url = url + '/api/stories'

    # Prompt the user to enter story details
    headline = input("Enter the headline of the story: ")

    # Validate category input
    while True:
        category = input(f"Enter the category of the story ({', '.join(CATEGORY_CHOICES)}): ").lower()
        if category in CATEGORY_CHOICES:
            break
        else:
            print("Invalid category. Please choose from:", ', '.join(CATEGORY_CHOICES))

    # Validate region input
    while True:
        region = input(f"Enter the region of the story ({', '.join(REGION_CHOICES)}): ").lower()
        if region in REGION_CHOICES:
            break
        else:
            print("Invalid region. Please choose from:", ', '.join(REGION_CHOICES))

    details = input("Enter the details of the story: ")

    story_data = {
        'headline': headline,
        'category': category,
        'region': region,
        'details': details
    }

    response = session.post(post_story_url, json=story_data)

    print (response.text)

def get_stories(input):
    commands = input.split(' ')
    id = ''
    date = '*'
    category = '*'
    region = '*'

    for type in commands:
        if "-id" in type:
            id = type.split("=")[1].strip("'")
        elif "-date" in type:
            date = type.split("=")[1]
            date = region[1:-1]
        elif "-cat" in type:
            category = type.split("=")[1]
            category = category[1:-1]
        elif "-reg" in type:
            region = type.split("=")[1]
            region = region[1:-1]

    url_list = []
    response = requests.get("https://newssites.pythonanywhere.com/api/directory")
    response_data = response.json()

    if id:
        print("ID!!!!!!!!!!!!!!!     -     " + id)
        print(response_data)
        for agency in response_data:
            if agency["agency_code"] == id.upper():
                url_list.append(agency["url"])
    else:
        for agency in response_data:
            url_list.append(agency["url"])

    for url in url_list:
        response = session.get( url + "/api/stories?story_cat=" + category + "&story_region=" + region + "&story_date" + date)
        
        print(response.text)

        if response.status_code == 200:
            stories = response.json()
            for story in stories["stories"]:
                print("Headline:    " + story['headline'])
                print("Date:        " + story['story_date'])
                print("Category:    " + story['story_cat'])
                print("Author:  " + str(story['author']))
                print("Region:  " + story['story_region'])
                print("Details: " + story['story_details'])
        else:
            print("The story could not be properly resolved")

def list():
    response = requests.get("http://newssites.pythonanywhere.com/api/directory")
    directory_agencies = response.json()
    for agency in directory_agencies:
        print("Name:    ", agency['agency_name'])
        print("URL:     ", agency['url'])
        print("ID:      ", agency['agency_code'])
        print("")
                
def delete(key):
    global session
    response = session.delete( url + key )
    print (response.text)

def main():
    global url

    while True:
        # Provide a menu of options

        # If user is logged in
        if check_login_status(url):
            print("Menu: (Usage)")
            print("1. Log out - 'logout'")
            print("2. Post a Story - 'post'")
            print("3. Get Stories - 'news [-id=] [-cat=] [-reg=] [-date=]'")
            print("4. List Agencies - 'list'")
            print("5. Delete Story - 'delete (story_key)'")
            print("6. Quit - 'quit'")
            print("")

        # If user is logged out
        else:
            print('You are logged out')
            print("Menu: (Usage)")
            print("1. Log in - 'login url'")
            print("2. Quit 'quit'")
            print("")

        choice = input("Enter your choice: ").strip().lower()

        # Deal with choices

        # If user is logged in
        if check_login_status(url):
            if choice == 'logout':
                logout()
            elif choice == 'post':
                post_story(url)
            elif choice.startswith('news'):
                get_stories(choice[5:].strip())  # Pass the input after 'news' command
            elif choice == 'list':
                list()
            elif choice.startswith('delete'):
                delete(input("Enter the story ID to delete: "))
            elif choice == 'quit':
                print("Goodbye!")
                print("")
                break
            else:
                print("Invalid choice. Please try again.")
                print("")

        # If user is logged out
        else:
            if choice.startswith('login'):
                url = choice.split(' ')[1]
                print("")
                login(url)
                print("")
            elif choice == 'quit':
                print("")
                print("Goodbye!")
                print("")
                break
            else:
                print("")
                print("Invalid choice. Please try again.")
                print("")

if __name__ == "__main__":
    main()
