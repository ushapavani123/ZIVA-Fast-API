import os
import json
import re


# Function to read criteria from the criteria file
def read_criteria(criteria_file):
    with open(criteria_file, 'r') as file:
        criteria = json.load(file)
    return criteria

def extract_total_workout_time(file_content):
    total_workout_time_pattern = re.compile(r'Total Workout Time- (\d+) minutes')
    match = total_workout_time_pattern.search(file_content)
    if match:
        return int(match.group(1))
    return None

def extract_total_calories_burned(file_content):
    total_calories_burned_pattern = re.compile(r'Total Calories Burned- (\d+) calories')
    match = total_calories_burned_pattern.search(file_content)
    if match:
        return int(match.group(1))
    return None
def rank_gym_workouts(folder_path, criteria):
    files = os.listdir(folder_path)
    ranked_files = []

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            file_content = file.read()

        workout_time = extract_total_workout_time(file_content)
        calories_burned = extract_total_calories_burned(file_content)
        if workout_time is not None and calories_burned is not None:
            workout_time_score = 0
            calories_burned_score = 0

            for key, weight in criteria["Total Workout Time"].items():
                criteria_value = int(re.search(r'\d+', key).group())
                if workout_time <= criteria_value:
                    workout_time_score = weight
                    break

            for key, weight in criteria["Total Calories Burned"].items():
                criteria_value = int(re.search(r'\d+', key).group())
                if calories_burned <= criteria_value:
                    calories_burned_score = weight
                    break

            total_score = workout_time_score + calories_burned_score
            if total_score >= 11:
                justification = "High workout intensity"
            if total_score < 11 and total_score >= 10:
                justification = "Moderate workout intensity"
            elif total_score <10:
                justification = "Low workout intensity"
            ranked_files.append({
                'file_name': file_name,
                'score': total_score,
                'workout_name': extract_workout_name(file_content),
                'workout_time': workout_time,
                'calories_burned': calories_burned,
                'file_content': file_content,
                'justification':justification
            })

    sorted_files = sorted(ranked_files, key=lambda x: x['score'], reverse=True)
    return sorted_files
def extract_workout_name(file_content):
    workout_name_pattern = re.compile(r'name:\s*(.*)', re.IGNORECASE)
    match = workout_name_pattern.search(file_content)
    return match.group(1) if match else "Unknown Workout"

def print_all_files(sorted_files):
    All_files = "\nAll Files along with their scores:"
    for file_name, score in sorted_files:
        All_files += f"\n{file_name} - Score: {score}"
    return All_files















