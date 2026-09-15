# All the necessary packages are imported
import json
import pandas as pd
import os
import sqlite3


# Filename to import the collected stories from the previous task.
filename = r"data\trends_20260413.json"

# Python function to load the collected stories from the JSON file.
def load_stories(filename):

    conn = sqlite3.connect("stories.db")
    cur = conn.cursor()

    query = "SELECT * FROM STORIES"
    data = pd.read_sql_query(query, conn)

    conn.close()

    df = pd.DataFrame(data)
    # Returns the dataframe
    return df

# Python function to perform data processing on the loaded stories.
def process_stories(df):

    # To remove the duplicate stories based on the 'post_id' column.
    # This ensures that we have only unique stories in our dataset.
    df = df.drop_duplicates(subset="post_id")
    # Prints the length of dataframe after removing duplicates
    print(f"After removing duplicates: {len(df)}")

    # Removes the stories from the dataframe which have null values either in 'post_id', 'title' or 'score' columns.
    df = df.dropna(subset=["post_id", "title", "score"])
    # Prints the length of dataframe after removing the stories with null values in above mentioned columns.
    print(f"After dropping nulls: {len(df)}")

    # pandas provide a built-in method to convert the data type of a column to numeric.
    # errors="coerce" argument is used to convert any non-numeric values to NaN, which are then handled in the next line.
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    # Similarly, we convert the 'num_comments' column to numeric and handle non-numeric values by converting them to NaN.
    df["num_comments"] = df["num_comments"].fillna(0).astype(int)

    # Drops the records with score less than 5.
    df = df[df["score"] >= 5]
    # Prints the length of dataframe after removing the stories with score less than 5.
    print(f'After removing low scores: {len(df)}')
    print()

    # Remove any leading or trailing whitespace characters from the 'title' column using the built-in str.strip() method
    df["title"] = df["title"].str.strip()

    return df

# A python function to save the cleaned stories into CSV file
def save_cleaned_stories(df, filename):
    # checks if a folder named data is already present of not. If not, then it creates a folder named data
    if not os.path.exists("data"):
        os.mkdir("data")

    # Saves the cleaned dataframe into a csv file using the built-in to_csv() method.
    df.to_csv(filename)

    # Prints the total nnumber of rows saved to the CSV file.
    print(f"Saved {len(df)} rows to {filename}")
    print()


# Pythons main function. Handles everything
def main():

    # Calls the function 'load_stories' to load the collected stories from the JSON file and the resultis stored in the variable 'df'
    df = load_stories(filename)

    # processes the loaded stories and loads the cleaned stories into the variable 'clean_df'
    clean_df = process_stories(df)

    # File name to save the cleaned stories in CSV format
    file = r"data/trends_clean.csv"
    # Calls the function to save the cleaned stories into a CSV file
    save_cleaned_stories(clean_df, file)

    # Prints the summary of the cleaned stories by showing the count of stories in each category.
    print("Stories per category: ")
    print(clean_df["category"].value_counts())


# The main function is called to execute the entire process
if __name__ == "__main__":
    main()