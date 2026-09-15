# Imports all the necessary python packages
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# Filename to import the analyzed stories from the previous task
filename = "data\\trends_updated.csv"

# Python function to setup the environment and load the data
def setup(filename):
    # Loads the data from the CSV file into a pandas DataFrame
    df = pd.read_csv(filename)
    print(df.head())

    if not os.path.exists("outputs"):
        os.mkdir("outputs")
    return df


def chart1(df):
    # Gets the top 10 stories based on their scores by sorting the DataFrame
    top10 = df.sort_values(by="score", ascending=False).head(10)
    plt.figure()
    # A horizontal bar chart is created using the top 10 stories.
    # The X-axis represents the scores of the stories, and the Y-axis represents the titles of the stories (truncated to 50 characters for better visualization).
    plt.barh(top10["title"].str[:50], top10["score"], color="steelblue")
    # Adds the X-axis label to render as "Scores"
    plt.xlabel("Scores")
    # Y-axis label to render as "Story Title"
    plt.ylabel("Story Title")
    # Adds the title to the chart as "Top 10 stories by score"
    plt.title("Top 10 stories by score")
    # Saves the chart as a PNG file in the outputs folder with the name "chart1_top_stories.png"
    plt.savefig("outputs/chart1_top_stories.png")
    # Displays the chart on the screen
    plt.show()
    return top10


def chart2(df):
    # Counts the number of stories in each category using value_counts() method
    category_counts = df["category"].value_counts()
    plt.figure()
    # Creates a barchart using the category labels on the X-axis and their corresponding counts on the Y-axis.
    sns.barplot(x=category_counts.index, y=category_counts.values, palette="viridis")
    plt.xlabel("Category")
    plt.ylabel("Number of Stories")
    plt.title("Number of stories per category")
    # Rotates the X-axis labels by 45 degrees to avoid overlapping with others
    plt.xticks(rotation=45)
    plt.savefig("outputs/chart2_categories.png")
    # show() method is used to display the chart on the screen
    plt.show()
    return category_counts

def chart3(df):
    plt.figure()
    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]
    # A scatter plot is created to visualize the relationship between the scores of the stories and the number of comments they received.
    # The hue parameter is used to differentiate between popular and not popular stories based on the "is_popular" column,
    # Where popular stories are colored green and not popular stories are colored red.
    sns.scatterplot(data=df,
        x="score",
        y="num_comments",
        hue="is_popular",
        palette={True: "green", False: "red"}
    )
    plt.xlabel("Score")
    plt.ylabel("Number of comments")
    plt.title("Score vs Comments (Green=Popular, Red=Not Popular)")
    # Adds a legend to the plot with the title "Is Popular" to indicate which color corresponds to popular and not popular stories.
    plt.legend(title="Is Popular")
    plt.savefig("outputs/chart3_scatter.png")
    plt.show()


    return popular, not_popular


def chart4(df):
    plt.figure(figsize=(8, 6))

    # Select numerical columns for correlation
    numeric_columns = df.select_dtypes(include="number")

    # Calculate correlation between numerical columns
    correlation = numeric_columns.corr()

    # Create the heatmap
    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5
    )

    plt.title("Correlation Heatmap")

    # Save the heatmap
    plt.savefig("outputs/chart4_heatmap.png")

    # Display the heatmap
    plt.show()

    return correlation

# A python function to create a dashboard by combining the above four charts into a single figure
def dashboard(df, top10, cat_counts, popular, not_popular, correlation):
    # Creates a figure with 2 rows and 2 columns to hold the four charts
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))

    # The first chart is a horizontal bar chart of the top 10 stories by score, which is plotted on the first subplot (axs[0, 0]).
    axs[0, 0].barh(top10["title"].str[:50], top10["score"])
    axs[0, 0].set_title("Top Stories")
    axs[0, 0].set_xlabel("Scores")
    axs[0, 0].set_ylabel("Story Title")

    # The second chart is a bar chart of the number of stories per category, which is plotted on the second subplot (axs[0, 1]).
    axs[0, 1].bar(cat_counts.index, cat_counts.values)
    axs[0, 1].set_title("Categories")
    axs[0, 1].set_xlabel("Category")
    axs[0, 1].set_ylabel("Number of Stories")
    axs[0, 1].tick_params(axis='x', rotation=45)

    # The third chart is a scatter plot of scores vs number of comments, with different colors for popular and not popular stories, which is plotted on the third subplot (axs[1, 0]).
    sns.scatterplot(
        data=df,
        x="score",
        y="num_comments",
        hue="is_popular",
        palette={True: "green", False: "red"},
        ax=axs[1, 0]
    )
    axs[1, 0].set_title("Score vs Comments (Green=Popular, Red=Not Popular)")
    axs[1, 0].set_xlabel("Score")
    axs[1, 0].set_ylabel("Number of comments")
    axs[1, 0].legend(title="Is Popular")

    # The fourth chart is a heatmap on axs[1, 1]
    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5,
        ax=axs[1, 1]
    )
    axs[1, 1].set_title("Correlation Heatmap")

    # Overall dashboard title
    fig.suptitle(
        "TrendPulse Dashboard",
        fontsize=16
    )

    # Adjust layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust rect to prevent suptitle overlap

    # Save dashboard
    plt.savefig("outputs/dashboard.png")

    plt.show()

    plt.close()


# The main function to execute the entire visualization process
def main():
    df = setup(filename)
    top10 = chart1(df)
    cat_counts = chart2(df)
    popular, not_popular = chart3(df)
    correlation = chart4(df)
    dashboard(df, top10, cat_counts, popular, not_popular, correlation)

# The main function is called to execute the entire process
if __name__ == "__main__":
    main()