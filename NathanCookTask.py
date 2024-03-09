import json
import os
import requests

# URL for data retrieval
base_url = "https://jsonplaceholder.typicode.com/"
# List of resources on jsonplaceholder
resources_available = ["posts", "comments", "albums", "photos", "todos", "users"]

# Writes data to new json file
def write_to_file(data, filename):
    try:
        with open(filename + ".json", 'w') as f:
            f.write(json.dumps(data, indent = 1))
    except Exception as e:
        print("Error: ", e)
# Appends data to existing file
def append_to_file(data, filename):
    try:
        if os.path.exists(filename + ".json"):
            with open(filename + ".json", 'a') as f:
                f.write(json.dumps(data, indent = 1))
    except Exception as e:
        print("Error: ", e)

# Read data from a file
def read_file(filename):
    try:    
        with open(filename, 'r') as f:
            data = json.load(f)
        return(data)
    except FileNotFoundError:
        print(filename + " not found")
        return
    except Exception as e:
        print("Error: ", e)
        return

# Prints json file contents to console
def print_file_contents(filename):
    try:
        with open(filename + ".json", 'r') as file:
            data = json.load(file)
            print(json.dumps(data, indent = 1))
            print("\n")
    except FileNotFoundError:
        print(filename + " not found")
    except Exception as e:
        print("Error: ", e)
        

# Gets supplied resource from jsonplaceholder  
def get_resources(resource):
    try:
        response = requests.get(base_url + resource)
        data = json.loads(response.text)
        return data
    except requests.exceptions.RequestException as e:
        print("Request error: ", e)
    except Exception as e:
        print("Error: ", e)
def create_user_list():
    try:    
        # Create a dictionary of "username" : "id"
        user_data = read_file('users.json')
        user_list_dictionary = {users['username']: users['id'] for users in user_data}
        return user_list_dictionary
    except Exception as e:
        print("Error: ", e)

# Categorizes posts by user
def categorization(user_list_dictionary):
    try:
        # Sort posts by userId
        post_data = read_file('posts.json')
        sorted_posts = sorted(post_data, key=lambda userId: userId['id'])

        # Iterate over sorted posts, write to array, then write arrays to json file
        username_posts = {}
        for post in sorted_posts:
            username = [username for username, id in user_list_dictionary.items() if id == post['userId']][0]
            if username not in username_posts:
                username_posts[username] = []
            username_posts[username].append(post)

        for username, data in username_posts.items():
            filename = username
            write_to_file(data, filename)
        return user_list_dictionary
    except FileNotFoundError:
        print(filename + " not found")
        return
    except Exception as e:
        print("Error: ", e)
        return

# Filter tasks to show incomplete tasks
def incomplete_tasks_by_user(user_list):
    try:
        # Create list for users with incomplete tasks 
        todo_list = {}
        # Read in todos file data
        task_list = read_file('todos.json')
        # Filter todos for only "completed": false
        tasks_todo = [task for task in task_list if not task["completed"]]

        # Iterate through incomplete tasks grouping them by username based on userid
        for task in tasks_todo:
            user_id = task["userId"]
            username = [username for username, todo_user_id in user_list.items() if todo_user_id == user_id][0]
            # Add user if not already in todo list
            if user_id not in todo_list:
                todo_list[user_id] = {"username": username, "tasks": []}
            todo_list[user_id]["tasks"].append(task)
        write_to_file(todo_list, "todo_list")
        print_file_contents("todo_list")
    except Exception as e:
        print("Error: ", e)

# Search json file for keyword
def keyword_search(filename, keyword):
    try:
        results = []
        with open(filename, 'r') as f:
            data = json.load(f)

            # Convert keyword to all lower case
            keyword_lower = keyword.lower()

            # Iterate through file contents looking for keyword
            for word in data:
                # Convert dict to string
                word_to_string = str(word)
                # Searches files for keyword, converts int to str for search comparison
                if keyword_lower in str(word_to_string.lower()):
                    results.append(word)
        return results, filename
    except FileNotFoundError:
        print(filename + " not found")
        return
    except Exception as e:
        print("Error: ", e)
        return

# Search original resources files for keyword provided by user and prints to console
# Will display both partial matches and phrases
# Will constantly loop as long as user if choosing Y for searching
def user_search_input():
    try:
        while True:
            user_selection = input('Would you like to search for keywords or user information? (Y/N)\n')
            # If user doesn't want to search exit
            if user_selection.upper() != 'Y':
                break

            keyword = input('What would you like to search for?\n')
            # Search files from resources_available array
            for filename in resources_available:
                results, found_in_file = keyword_search(filename + ".json", keyword)
                results_count = len(results)
                if results_count > 0:
                    print("\n")
                    # File where data was found, coloured green to make it more distinguishable 
                    print('\033[92m' "File: " + found_in_file + '\033[0m')
                    print(json.dumps(results, indent = 1))
                else:
                    print("No results found in " + found_in_file)
    except Exception as e:
        print("Error: ", e)

# GET all resources available on jsonplaceholder and write them to a file
print("Getting data from https://jsonplaceholder.typicode.com/\n")
for resources in resources_available:
    data = get_resources(resources)
    print("Creating json file for " + resources)
    write_to_file(data, resources)

# Categorize posts by user
print("\nCategorizing posts by user")
user_list = create_user_list()
categorization(user_list)

# Display categorized posts in console
for filename, _ in user_list.items():
    # Print user posts belong to in green to make in more distinguishable  
    print('\033[92m' "Posts for " + filename + '\033[0m')
    print_file_contents(filename)

# Filter and display incomplete tasks by user
incomplete_tasks_by_user(user_list)

# Allow user to search for any keywords or details
user_search_input()

