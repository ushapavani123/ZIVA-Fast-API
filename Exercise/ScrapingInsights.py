import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np

def save_html_to_file(url, file_path):
    """
    Fetches the HTML content from the specified URL and saves it to the specified file path.
    Args:
        url (str): The URL of the webpage to fetch HTML content from.
        file_path (str): The file path where the HTML content will be saved.
    Returns:
        str: The file path where the HTML content is saved, or None if the request failed.
    """
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the HTML content
        html_content = response.text

        # Open the file in write mode and save the HTML content
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_content)

        print("HTML content saved to:", file_path)
        return file_path
    else:
        print("Failed to retrieve the webpage.")
        return None


def read_html_file(file_path):
    """
    Reads the HTML content from the specified file using BeautifulSoup.
    Args:
        file_path (str): The file path of the HTML file to read.
    Returns:
        pandas.DataFrame: The DataFrame containing parsed HTML content with an additional 'Impact' column.
        And also filling the missing values with the mode for impact columns
    """
    # Open the HTML file and read its contents
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find Exercise and calories burned table
    exercise_table = soup.find("table")

    # Extract table headers
    headers = [header.text.strip() for header in exercise_table.find_all("tr")[0] if header.text.strip()]

    # Extract table rows
    rows = exercise_table.find_all("tr")

    # Extract data from rows
    data = []
    for row in rows[1:]:
        cells = row.find_all("td")
        row_data = [re.sub(r'\s+', ' ', cell.text.strip()) for cell in cells]

        # Move words after the first comma to the 'Impact' column
        exercise_parts = row_data[0].split(',', 1)
        if len(exercise_parts) > 1:
            row_data[0] = exercise_parts[0].strip()
            row_data.append(exercise_parts[1].strip())
        else:
            row_data.append('')  # If no word after the first comma, append an empty string to 'Impact'

        data.append(row_data)

    # Create pandas DataFrame
    df = pd.DataFrame(data, columns=headers + ['Impact'])

    # Remove the comma at the end of values in the 'Exercise & Calories Burned per Hour' column
    df['Exercise & Calories Burned per Hour'] = df['Exercise & Calories Burned per Hour'].str.rstrip(',')

    # Remove rows where the value in the 'Exercise & Calories Burned per Hour' column is 'Exercise & Calories Burned per Hour'
    df = df[df['Exercise & Calories Burned per Hour'] != 'Exercise & Calories Burned per Hour']

    # Convert weight column to numeric
    df['130 lbs'] = pd.to_numeric(df['130 lbs'].str.replace(r'\D+', ''), errors='coerce')  # Extract numerical values and handle errors
    df['155 lbs'] = pd.to_numeric(df['155 lbs'].str.replace(r'\D+', ''), errors='coerce')
    df['180 lbs'] = pd.to_numeric(df['180 lbs'].str.replace(r'\D+', ''), errors='coerce')
    df['205 lbs'] = pd.to_numeric(df['205 lbs'].str.replace(r'\D+', ''), errors='coerce')
    # Fill missing values in the 'Impact' column with 'general'
    df['Impact'] = df['Impact'].fillna('general')

    # Replace values not in impact_keywords with random values from impact_keywords
    impact_keywords = ['high', 'low', 'fast', 'slow', 'very light', 'light', 'moderate', 'vigorous', 'very vigorous',
                       'general']
    df['Impact'] = df['Impact'].apply(lambda x: random.choice(impact_keywords) if x not in impact_keywords else x)

    # Display the DataFrame
    print(df)

    return df

def display_unique_exercises(df):
    """
    Displays unique values from the column 'Exercise & Calories Burned per Hour' in the DataFrame.
    Args:
        df (pandas.DataFrame): The DataFrame containing exercise data.
    Returns:
        None
    """
    unique_exercises = df['Exercise & Calories Burned per Hour'].unique()
    for exercise in unique_exercises:
        print(exercise)

def count_unique_exercises(df):
    """
    Counts the number of unique values in the column 'Exercise & Calories Burned per Hour' in the DataFrame.
    Args:
        df (pandas.DataFrame): The DataFrame containing exercise data.
    Returns:
        int: The number of unique exercises.
    """
    unique_exercises_count = df['Exercise & Calories Burned per Hour'].nunique()
    return unique_exercises_count

def top_exercises_by_impact(df, impact):
    """
    Retrieves the top exercises for the specified impact keyword.

    Args:
        df (pandas.DataFrame): The DataFrame containing exercise data.
        impact (str): The impact keyword.

    Returns:
        list: A list containing the top exercises for the specified impact.
    """
    # Filter DataFrame for the specified impact
    filtered_df = df[df['Impact'] == impact]

    # Sort exercises by calories burned
    sorted_df = filtered_df.sort_values(by='130 lbs', ascending=False)

    # Get top exercises (maximum 3)
    top_exercises = sorted_df['Exercise & Calories Burned per Hour'].unique()[:3].tolist()

    return top_exercises

def top_exercises_by_weight(df, weight):
    """
    Retrieves the top exercises based on the weight.

    Args:
        df (pandas.DataFrame): The DataFrame containing exercise data.
        weight (str): The weight for which calories burned are provided.

    Returns:
        list: A list containing the top exercises based on weight.
    """
    # Convert weight to column name
    weight_column_name = f'{weight}'

    # Sort exercises by calories burned (descending order)
    sorted_df = df.sort_values(by=weight_column_name, ascending=False)
    print(sorted_df.head())
    # Get top exercises
    top_exercises = sorted_df['Exercise & Calories Burned per Hour'].unique()[:3].tolist()
    return top_exercises

def plot_top_exercises_by_impact(df, impact, weight):
    """
    Plots a bar graph for the top 3 exercises based on the specified impact and weight.

    Args:
        df (pandas.DataFrame): The DataFrame containing exercise data.
        impact (str): The impact keyword.
        weight (str): The weight for which calories burned are provided.

    Returns:
        figure
    """
    # Call the function to retrieve top exercises based on the impact
    top_exercises = top_exercises_by_impact(df, impact)

    # Prepare data for plotting
    exercises = top_exercises#[f"Exercise {i}" for i in range(1, len(top_exercises) + 1)]
    calories_burned = [df[df['Exercise & Calories Burned per Hour'] == exercise][weight].values[0] for exercise in top_exercises]

    # Plot the bar graph
    fig = plt.figure(figsize=(10, 6))
    plt.bar(exercises, calories_burned, alpha=0.7)
    plt.xlabel('Exercises')
    plt.ylabel('Calories Burned')
    plt.title(f'Top 3 Exercises for Impact: {impact} (Weight: {weight})')
    plt.xticks(rotation=45)
    plt.tight_layout()
    #plt.show()
    return fig

def plot_top_exercises_by_weight(df, weight):
    """
    Plots a line graph for the top exercises based on the specified weight.

    Args:
        df (pandas.DataFrame): The DataFrame containing exercise data.
        weight (str): The weight for which calories burned are provided.

    Returns:
        figure
    """
    # Filter the DataFrame for the specified weight
    weight_column = f'{weight}'
    df_weight = df[['Exercise & Calories Burned per Hour', weight_column]]

    # Sort exercises by calories burned
    df_weight_sorted = df_weight.sort_values(by=weight_column, ascending=False)

    # Get top exercises and corresponding calories burned
    top_exercises = df_weight_sorted['Exercise & Calories Burned per Hour'].head(3)
    calories_burned = df_weight_sorted[weight_column].head(3)

    # Plot the line graph
    fig = plt.figure(figsize=(10, 6))
    plt.plot(top_exercises, calories_burned, marker='o', linestyle='-', color='g')
    plt.xlabel('Exercises')
    plt.ylabel('Calories Burned per Hour')
    plt.title(f'Top Exercises by Weight: {weight}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    #plt.show()
    return fig


def plot_unique_exercises_count(df):
    """
    Plots a pie chart to display the count of number of unique exercises in high, moderate, and low impact.

    Args:
        df (pandas.DataFrame): The DataFrame containing exercise data.

    Returns:
        figure
    """
    # Filter the DataFrame for high, moderate, and low impact categories
    df_high = df[df['Impact'] == 'high']
    df_moderate = df[df['Impact'] == 'moderate']
    df_low = df[df['Impact'] == 'low']

    # Get the count of unique exercises in each category
    count_high = df_high['Exercise & Calories Burned per Hour'].nunique()
    count_moderate = df_moderate['Exercise & Calories Burned per Hour'].nunique()
    count_low = df_low['Exercise & Calories Burned per Hour'].nunique()

    # Plot the pie chart
    labels = ['High Impact', 'Moderate Impact', 'Low Impact']
    counts = [count_high, count_moderate, count_low]
    colors = ['skyblue', 'salmon', 'lightgreen']
    explode = (0.1, 0, 0)  # explode the 1st slice (High Impact)

    fig = plt.figure(figsize=(10, 6))
    plt.pie(counts, labels=labels, colors=colors, explode=explode, autopct='%1.1f%%', startangle=140)
    plt.title('Count of Unique Exercises by Impact Category')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    #plt.show()
    return fig

def plot_histogram_top_exercises(df):
    """
    Plots a histogram to display the top 3 unique exercises in each weight category based on the highest calories burned.

    Args:
        df (pandas.DataFrame): The DataFrame containing exercise data.

    Returns:
        figure
    """
    # Define weight columns
    weight_columns = ['130 lbs', '155 lbs', '180 lbs', '205 lbs']

    # Initialize colors for each weight category
    colors = ['lightblue', 'salmon', 'lightpink', 'lavender']

    # Initialize figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # Set position of bars on x-axis
    bar_width = 0.2
    index = np.arange(3)  # Adjusted index for 3 bars

    # Iterate over each weight category
    for i, weight_column in enumerate(weight_columns):
        # Sort DataFrame by calories burned in the current weight column
        sorted_df = df.sort_values(by=weight_column, ascending=False)

        # Get top 3 unique exercises and their corresponding calories burned
        top_exercises = sorted_df['Exercise & Calories Burned per Hour'].head(3).tolist()
        calories_burned = sorted_df[weight_column].head(3).tolist()

        # Plot bars for each exercise
        ax.bar(index + i * bar_width, calories_burned, bar_width, color=colors[i], label=weight_column)

    # Set labels and title
    ax.set_xlabel('Exercise')
    ax.set_ylabel('Calories Burned')
    ax.set_title('Top 3 Unique Exercises by Weight Category')
    ax.set_xticks(index + 1.5 * bar_width)
    ax.set_xticklabels(top_exercises)  # Using top exercises as x-axis labels
    ax.legend()

    # Show plot
    plt.tight_layout()
    #plt.show()
    return fig


'''
# Call the function to read HTML file and create DataFrame
url = "https://hr.uky.edu/wellness/exercise-calories-burned-hour"
file_path = "exercise_calories_burned_hour.html"
save_html_to_file(url, file_path)
df = read_html_file(file_path)
display_unique_exercises(df.tail())
unique_count = count_unique_exercises(df)
print("Number of unique exercises:", unique_count)

# Get user input for impact
impact = input("Enter the impact keyword (e.g., 'high', 'low', 'general'): ")

# Call the function to display top exercises based on the impact
top_exercises = top_exercises_by_impact(df, impact)
print(f"Top exercises for '{impact}':")
for i, exercise in enumerate(top_exercises, start=1):
    print(f"{i}. {exercise}")

# Get user input for weight
weight = input("Enter your weight column (e.g., '130 lbs', '155 lbs', '180 lbs', '205 lbs'): ")

# Call the function to retrieve top exercises based on weight
top_exercises = top_exercises_by_weight(df, weight)

# Display the top exercises
print(f"Top exercises for weight '{weight}':")
for i, exercise in enumerate(top_exercises, start=1):
    print(f"{i}. {exercise}")

# Plot the graph for the top 3 exercises based on the impact and weight
plot_top_exercises_by_impact(df, impact, weight)

# Plot the graph for the top exercises based on the weight
plot_top_exercises_by_weight(df, weight)

# Plot the pie chart for count of unique exercises by impact category
plot_unique_exercises_count(df)

# Plot histogram for top 3 unique exercises by weight category
plot_histogram_top_exercises(df)
'''