# Importing necessary packages
import pandas as pd
import numpy as np

# Filename to import the cleaned stories from the previous task
filename = r"data/trends_clean.csv" # Changed path separator from \ to /

# Python function to load data from CSV file
def load_and_explore_data(filename):

    # Load the cleaned data from CSV file into pandas DataFrame
    df = pd.read_csv(filename)
    # Drops the unnecessary column "Unnamed: 0"
    df.drop("Unnamed: 0", axis=1, inplace=True)
    # df.shape give the number of rows and columns in the dataframe.
    print(f"Loaded data: {df.shape}")
    print("\nFirst 5 rows:")
    # head() method prints the first 5 rows of the dataframe
    print(df.head())

    # Calculates the mean score and average number of comments for the stories
    avg_score = df["score"].mean()
    avg_comments = df["num_comments"].mean()
    print(f"\nAverage score: {round(avg_score, 2)}")
    print(f"Average comments: {round(avg_comments, 2)}")

    # Finally returns the DataFrame
    return df


def basic_analysis(df):

    # Calculates the mean, median, and standard deviation of the scores of the stories using built-in numpy functions.
    mean = np.mean(df["score"])
    median = np.median(df["score"])
    std = np.std(df["score"])

    # Gets maximum and minimum scores from the "score" column
    max_score = np.max(df["score"])
    min_score = np.min(df["score"])

    # Gets the category which has the most number of stories and the count of stories in that category using value_counts() method of pandas.
    most_stories = df["category"].value_counts().idxmax()
    # Gets the count of stories in the category which has the most number of stories using value_counts() method of pandas.
    count_category = df["category"].value_counts().max()

    # Gets the story with the highest number of comments using idxmax() method of pandas to get the index of the row with maximum comments and then using iloc to get that row as a Series.
    most_commented_story = df.iloc[df["num_comments"].idxmax()]
    # Prints the title and number of comments of the most commented story
    print(most_commented_story['title'], most_commented_story['num_comments'])

    # Finally, we print all the above calculated statistics in a readable format
    print("\n--- NumPy Stats ---")
    print("Mean score   :", round(mean))
    print("Median score :", round(median))
    print("Std deviation:", round(std))
    print("Max score    :", max_score)
    print("Min score    :", min_score)
    print(f"\nMost stories in category: {most_stories} ({count_category} stories)")
    print(f"Most commented story: {most_commented_story['title']} — {most_commented_story['num_comments']} comments")

# A python function to add new columns to the dataframe
def add_new_columns(df):
    df["engagement"] = df["num_comments"] / (df["score"] + 1)
    avg_score = df["score"].mean()
    df["is_popular"] = df["score"] > avg_score
    return df

# A python function to save the updated dataframe into a new CSV file
def save_updated_data(df, filename):
    df.to_csv(filename, index=False)
    print(f"\nSaved to {filename}")

# Python main function to handle everything
def main():
    df = load_and_explore_data(filename)
    basic_analysis(df)
    updated_df = add_new_columns(df)
    save_updated_data(updated_df, r"data\trends_updated.csv")

# To call the main function when this script is run directly
if __name__ == "__main__":
    main()