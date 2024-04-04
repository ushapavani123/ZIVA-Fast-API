# Ensure these libraries are installed in your Python environment
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def fetch_and_parse_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all('table')
        return tables  # This can be modified to return parsed data in a desired format (e.g., DataFrame)
    else:
        return None
def table_to_dataframe(table):
    # Assuming 'table' is a BeautifulSoup object containing a single <table>
    rows = table.find_all('tr')
    header = [th.text for th in rows[0].find_all('th')]
    data = [[td.text for td in tr.find_all('td')] for tr in rows[1:]]
    df = pd.DataFrame(data, columns=header)
    return df


def calculate_average_calories_by_category(data):
    """
    Calculate the average calories burned for each category and weight, and return the results.

    Parameters:
    - data: pandas DataFrame containing the cleaned dataset with columns for Category and calorie burns for 125, 155, and 185-pound individuals.

    Returns:
    - A dictionary where each key is a category and each value is another dictionary with average calorie burns for 125, 155, and 185-pound individuals.
    """
    results = {}
    for category in data['Category'].unique():
        category_means = data[data['Category'] == category][
            ['125-pound person', '155-pound person', '185-pound person']].mean().to_dict()
        results[category] = category_means

    return results

# Example usage with a hypothetical 'clean_data' DataFrame
# averages = calculate_average_calories_by_category(clean_data)
# Now, 'averages' can be passed to a template for rendering in HTML

