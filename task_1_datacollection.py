import requests
import time
import json
import datetime
import pandas as pd
import sqlite3 # Added import for sqlite3
import os

# Base URL
BASE_URL = "https://hacker-news.firebaseio.com/v0"
HEADERS = {"User-Agent": "TrendPulse/1.0"}

# Created a dictionary with all 5 categories as keys and matching keywords as list of values
# This dictionary is later used for assigning the category of each story based on the keywords that are present in the title of the story
CATEGORIES = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

# A constant variable to ensure each category will have atmost 25 stories only
CATEGORY_MAX = 25

# Python function that fetches the top stories
def fetch_ids_of_top_stories():
    print("Extracting the data from the given API..........")

    try:
        url = f"{BASE_URL}/topstories.json" # Corrected URL
        response = requests.get(url, headers=HEADERS)
        # After making a request to the given API/URL checks if it failed using raise_for_status()
        # If failed, then jumps to except block to handle it gracefully
        # Else parse JSON
        response.raise_for_status()
        return response.json()[:1500]
    # If any run-time error(Exception more formally) arises, then it would be gracefully handled by the except block
    # then this block returns whatever we managed to fetch
    except Exception as A:
        print(f"An exception occured: {A}")
        return []


# A python function that retrieves the details of each story based on the story ID
def fetch_each_story(story_id):

    # All the details of stories are stored in this path. Iterating through the IDs of each story, fetching the details of each story.
    url = f"{BASE_URL}/item/{story_id}.json" # Corrected URL

    try:
        # For each iteration, only the details of one story is fetched, and then immediately returned to the invoker
        response = requests.get(url, headers=HEADERS)

        response.raise_for_status()
        return response.json()

    # If at all no story details are present with the given ID, then nothing will be returned
    except Exception as A:
        print(f"Error fetching story with ID {story_id}: {A}")
        return None



# A python function to categorize each story
def categorization(title):
    # Converting the title of the story to lower case
    title = title.lower()
    if not title:
        return []

    matched = []

    # Iterating through the keys, values of list in the CATEGORIES dictionary
    for category, keywords in CATEGORIES.items():

        # Iterating through the list of keywords for each category
        for keyword in keywords:

            # Checking if any of the keywords are present in the title of the story
            if keyword in title:

                # If present, then the category is added to the list of matched categories for that story
                matched.append(category)
                break

    return matched


def collect_stories(story_ids):
    # A dictionary with all categories as keys with all the values initialized to 0 to keep track of the number of stories per category
    category_counts = {cat : [] for cat in CATEGORIES.keys()}

    print("Fetching individual story details")

    # An empty list to store the details of all the storie that are successfully fetched
    fetched_stories = []

    # Iterating through the list of story IDs, fetching the details of each story
    for story_id in story_ids:

        # Extracting the ID of story
        story = fetch_each_story(story_id)
        if story and story.get("type") == "story" and story.get("title"):

            # If the storu is successfully fetched, and if its type is story and having a title for it
            # then it is added to the list of fetched stories
            fetched_stories.append(story)

    print(f"Fetched {len(fetched_stories)} valid stories.") # Moved print outside loop for efficiency

    # Iterating through the categories one by one
    for category in CATEGORIES.keys():

        # Iterating through the story_ids one by one
        for story in fetched_stories:

            # Checking if the number of stories collected for that particular category has reached the maximum limit of 25 or not.
            if len(category_counts[category]) >= CATEGORY_MAX:
                # If it has reached the limit, then we break out the loop and move to the next category
                break

            # Gets the list of associated categories for that stories based on the title
            matched_categories = categorization(story.get("title"))

            # If the category of the story matches with the current category that we are iterating
            if category in matched_categories:

                # then we add the details of that story to the list of stories for that category in the category_counts dictionary
                category_counts[category].append({
                    "post_id": story.get("id"),
                    "title": story.get("title"),
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", ""),
                    "collected_at": datetime.datetime.now().isoformat(),
                })

        # Finally we print the number of stories collected for each category
        print(f"{category}: {len(category_counts[category])} stories collected.")

        # Before moving to the next category, we wait for 2 seconds to avoid hitting the API rate limits
        # And not to overload the servers with too many requests in a short span of time
        time.sleep(2)

    all_stories = [story for stories in category_counts.values() for story in stories]
    return all_stories


# A python function to save the collected stories in a JSON file
def save_to_db(filename, stories):
    conn = sqlite3.connect(filename)
    cur = conn.cursor()

    query = "CREATE TABLE IF NOT EXISTS stories (post_id INTEGER, title TEXT, category TEXT, score INTEGER, num_comments INTEGER, author TEXT, collected_at DATETIME)"

    cur.execute(query)

    for story in stories:
        cur.execute("""
            INSERT INTO stories
            (post_id, title, category, score, num_comments, author, collected_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            story.get("post_id"),
            story.get("title"),
            story.get("category"),
            story.get("score", 0),
            story.get("num_comments", 0),
            story.get("author", ""),
            datetime.datetime.fromisoformat(story.get("collected_at")).strftime("%Y-%m-%d %H:%M:%S")
        ))

    conn.commit()

    cur.close()

    print(f"Saved to database named {filename}")



# Main function. Handles everything
def main():

    # Calls the function 'fetch_ids_of_top_stories' and the result (Stories IDs) are stored in the variable story_ids
    story_ids = fetch_ids_of_top_stories()

    # If no stories are fetched, then error message is printed and the program is exited gracefully without any further execution
    if not story_ids:
        print("No story IDs fetched. Exiting.")
        return

    # Details of all the stories are collected by calling the function 'collect_stories' and passing the story IDs as an argument.
    # The result (Details of all the stories) are stored in the variable 'stories'
    stories = collect_stories(story_ids)

    # This method saved the all the extracted stories in a JSON file and gets the filename where the stories are saved
    file = "stories.db"
    save_to_db(file, stories)


    # Prints the total number of stories collected and saved into the JSON file.
    print(f"Collected {len(stories)} stories. Saved to the {file}")

# The main function is called to execute the entire process
if __name__ == "__main__":
    main()
    print("\n--- Checking for stories.db ---")
    current_directory_files = os.listdir('.')
    print(f"Files in current directory: {current_directory_files}")
    if 'stories.db' in current_directory_files:
        print("stories.db found!")
    else:
        print("stories.db not found.")