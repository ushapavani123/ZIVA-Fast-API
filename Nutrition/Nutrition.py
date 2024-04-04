import os


# Function to read criteria from file
def reading_criteria(criteria_file):
    criteria = {}
    with open(criteria_file, 'r') as file:
        for line in file:
            criterion, weight = line.strip().split(': ')
            criteria[criterion] = int(weight)
    return criteria


# Function to calculate rank for a file based on criteria
def calculate_weight(file_path, criteria):
    calories = 0
    protein = 0
    fiber = 0

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('Calories:'):
                value = line.split(': ')[1].strip().split(' ')[0].replace('g', '')
                calories = float(value)
            elif line.startswith('Protein:'):
                value = line.split(': ')[1].strip().split(' ')[0].replace('g', '')
                protein = float(value)
            elif line.startswith('Fiber:'):
                value = line.split(': ')[1].strip().split(' ')[0].replace('g', '')
                fiber = float(value)

    return calories, protein, fiber


# Function to select top files based on rank
def selecting_top3_files(folder_path, criteria):
    files_ranking = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        score = calculate_weight(file_path, criteria)
        files_ranking.append({
            "filename": filename,
            "score": score
        })

    return files_ranking


# Function to assign ranks to files based on scores
def assign_ranks(files_ranking):
    files_ranking.sort(key=lambda x: x['score'][0], reverse=True)
    ranked_files = [(rank + 1, file_info['filename'], file_info['score']) for rank, file_info in enumerate(files_ranking)]
    return ranked_files



# Main function
def main():
    # Folder containing text files
    folder_path = r'/Users/usha/Library/Mobile Documents/com~apple~CloudDocs/Data Science/Data wrangling/ProjectDW/Nutrition/text_files'

    # File containing criteria
    criteria_file = r'/Users/usha/Library/Mobile Documents/com~apple~CloudDocs/Data Science/Data wrangling/ProjectDW/Nutrition/criteria_Nutrition.txt'

    # Read criteria
    criteria = reading_criteria(criteria_file)

    # Select top files
    files_ranking = selecting_top3_files(folder_path, criteria)

    # Assign ranks to files
    ranked_files = assign_ranks(files_ranking)

    # Print files with their rank
    print("Files with their rank:")
    for rank, file_name, score in ranked_files:
        print(f"Rank {rank}: {file_name} ")

    # Print top 3 files with their rank
    print("Top 3 files with their rank:")
    for rank, file_name, score in ranked_files[:3]:
        print(f"Rank {rank}: {file_name} ")
        print("Justification:")
        # Get the file path
        file_path = os.path.join(folder_path, file_name)
        # Calculate calories, protein, and fiber for the current file
        calories, protein, fiber = calculate_weight(file_path, criteria)
        print(f"This {file_name} file is ranked {rank} with {calories} calories, {protein} grams of protein and {fiber} grams of fiber")


if __name__ == "__main__":
    main()
