import requests
import matplotlib.pyplot as plt
def fetch_data(url, headers):
    response = requests.get(url, headers=headers)
    return response.json()

def process_data(data):
    body_parts_count = {}
    equipment_count = {}
    target_count_by_body_part = {}
    most_common_exercises = {}

    for exercise in data['exercices']:
        body_part = exercise['bodyPart']
        equipment = exercise['equipment']
        exercise_name = exercise['name']
        target = exercise['target']

        # Count occurrences of each Bodypart
        body_parts_count[body_part] = body_parts_count.get(body_part, 0) + 1
        # Count occurrences of each Equipment
        equipment_count[equipment] = equipment_count.get(equipment, 0) + 1
        # Count occurrences of each target
        if body_part not in target_count_by_body_part:
            target_count_by_body_part[body_part] = {}
        target_count_by_body_part[body_part][target] = target_count_by_body_part[body_part].get(target, 0) + 1
        # Count occurrences of each exercise
        most_common_exercises[exercise_name] = most_common_exercises.get(exercise_name, 0) + 1

    return body_parts_count, equipment_count, target_count_by_body_part, most_common_exercises


def top_5_equipments(equipment_count):
    # Sort the equipment count dictionary by count in descending order
    sorted_equipment_count = sorted(equipment_count.items(), key=lambda x: x[1], reverse=True)

    # Extract the top 5 equipment and their counts
    top_5_equipment = sorted_equipment_count[:5]
    equipment_names = []
    counts = []
    for equipment, count in top_5_equipment:
        equipment_names.append(equipment)
        counts.append(count)

    return equipment_names, counts


def plot_bar_chart(data, title, xlabel, ylabel):
    plt.figure(figsize=(7, 5))
    plt.bar(data.keys(), data.values(), color='skyblue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{title}.png')
    plt.close()

def plot_pie_chart(data, labels, title):
    plt.figure(figsize=(7, 5))
    plt.pie(data, labels=labels, autopct='%1.1f%%', colors=plt.cm.tab20.colors)
    plt.title(title)
    plt.axis('equal')
    plt.savefig(f'{title}.png')
    plt.close()

def plot_line_chart(x_data, y_data, title, xlabel, ylabel):
    plt.figure(figsize=(8, 5))
    plt.plot(x_data, y_data, marker='o', linestyle='-', color='green')
    for i, count in enumerate(y_data):
        plt.text(x_data[i], count, str(count), ha='center', va='bottom')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{title}.png')
    plt.close()
