import json
import os
import re

def load_criteria(criteria_file):
    """
    Load criteria from a JSON file.

    Parameters:
        criteria_file (str): The file path of the JSON file containing criteria.

    Returns:
        list: A list of criteria dictionaries.
    """
    with open(criteria_file, "r") as file:
        criteria_data = json.load(file)
    return criteria_data["criteria"]

def parse_exercise_file(file_path):
    """
    Parse an exercise file and extract relevant information.

    Parameters:
        file_path (str): The file path of the exercise file to parse.

    Returns:
        dict: Exercise information extracted from the file.
    """
    with open(file_path, "r") as file:
        exercise_data = file.read()

    exercise_info = {}
    # Extracting intensity, using regular expressions searching for word "Intensity" in the file
    intensity_match = re.search(r'Intensity:\s*(\w+)', exercise_data)
    if intensity_match:
        exercise_info["Intensity"] = intensity_match.group(1)

    # Extracting target muscle groups, using regular expressions searching for the words "target muscle groups" in the file
    muscle_groups_match = re.search(r'Target Muscle Groups:\s*([\w\s,]+)', exercise_data)
    if muscle_groups_match:
        muscle_groups = muscle_groups_match.group(1).split(", ")
        exercise_info["Target Muscle Groups"] = tuple(muscle_groups)

    # Extracting duration, using regular expressions searching for word "Duration" in the file
    duration_match = re.search(r'Duration:\s*([\w\s.-]+)', exercise_data)
    if duration_match:
        exercise_info["Duration"] = duration_match.group(1)

    # Extracting benefits, using regular expressions searching for word "benefits" in the file
    benefits_match = re.search(r'Benefits:\s*([\w\s,]+)', exercise_data)
    if benefits_match:
        exercise_info["Benefits"] = benefits_match.group(1).split(", ")

    # Extracting calories burned, using regular expressions searching for words "calories burned" in the file
    calories_match = re.search(r'Calories Burned:\s*Approximately\s*(\d+-\d+)\s*calories\s*per\s*hour', exercise_data)
    if calories_match:
        exercise_info["Calories Burned"] = calories_match.group(1)

    return exercise_info

def calculate_score(exercise_data, criteria):
    """
    Calculate the score for each exercise file based on the criteria.

    Parameters:
        exercise_data (dict): Exercise information extracted from the file.
        criteria (list): A list of criteria dictionaries.

    Returns:
        int: The score calculated for the exercise.
    """
    score = 0
    for criterion in criteria:
        if criterion["name"] in exercise_data:
            weight_dict = criterion["weights"]
            value = exercise_data[criterion["name"]]
            if isinstance(value, list):
                value = tuple(value)
            if value in weight_dict:
                score += weight_dict[value]
    return score

def rank_exercise_files(exercise_folder_path, criteria):
    """
    Rank exercise files based on the criteria.

    Parameters:
        exercise_folder_path (str): The folder path containing exercise files.
        criteria (list): A list of criteria dictionaries.

    Returns:
        list: Exercise files ranked based on criteria.
    """
    exercise_files = [file for file in os.listdir(exercise_folder_path) if file.endswith(".txt")]
    ranked_files = []
    for file_name in exercise_files:
        file_path = os.path.join(exercise_folder_path, file_name)
        exercise_data = parse_exercise_file(file_path)
        score = calculate_score(exercise_data, criteria)

        # Justification for each exercise file
        justification = f"This file scored well due to its {exercise_data['Intensity']} intensity, targeting {', '.join(exercise_data['Target Muscle Groups'])} muscle groups, recommended duration of {exercise_data['Duration']}, {', '.join(exercise_data['Benefits'])} benefits" #and, {', '.join(exercise_data['Calories Burned'])}, significant calorie burning potential."
        if 'Calories Burned' in exercise_data:
            justification += f", and {''.join(exercise_data['Calories Burned'])} significant calorie burning potential."
        else:
            justification += "."
        # Append exercise data, score, and justification to the ranked files list
        ranked_files.append(
            {"file_name": file_name, "score": score, "exercise_data": exercise_data, "justification": justification})

    ranked_files.sort(key=lambda x: x["score"], reverse=True)
    return ranked_files
'''
def print_top_three_justification(top_three_files):
    """
    Print detailed justification for the top three exercise files.

    Parameters:
        top_three_files (list): The top three exercise files ranked based on criteria.
    """
    print("Detailed Justification for Top Three Exercise Files:")
    for i, file_data in enumerate(top_three_files, start=1):
        print(f"\n{i}. {file_data['file_name']}") # - Score: {file_data['score']}")
        print("Justification:", file_data['justification'])
'''
def print_top_three_justification(top_three_files):
    """
    Generate detailed justification for the top three exercise files.

    Parameters:
        top_three_files (list): The top three exercise files ranked based on criteria.

    Returns:
        list: Detailed justification for the top three exercise files.
    """
    justification_list = []
    for i, file_data in enumerate(top_three_files, start=1):
        justification = {
            "rank": i,
            "file_name": file_data['file_name'],
            "justification": file_data['justification']
        }
        justification_list.append(justification)
    return justification_list

def main():
    """
    Main function to load criteria, rank exercise files, and print results.
    """
    # Load criteria
    criteria = load_criteria("/Users/usha/Library/Mobile Documents/com~apple~CloudDocs/Data Science/Data wrangling/ProjectDW/Exercise/criteria_Exercise.json")

    # Rank exercise files
    exercise_folder_path = "/Users/usha/Library/Mobile Documents/com~apple~CloudDocs/Data Science/Data wrangling/ProjectDW/Exercise/Ranking_Selection_Exercise"
    ranked_files = rank_exercise_files(exercise_folder_path, criteria)

    # Print ranked exercise files with ranks and scores
    print("Exercise files ranked based on criteria with ranks and scores:")
    for rank, exercise in enumerate(ranked_files, start=1):
        print(f"Rank: {rank}, File: {exercise['file_name']}, Score: {exercise['score']}")

    # Select top three files
    top_three_files = ranked_files[:3]

    # Print detailed justification for top three files
    print_top_three_justification(top_three_files)

if __name__ == "__main__":
    main()

