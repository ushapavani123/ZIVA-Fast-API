from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse,FileResponse
from GymWorkout.static.GYMworkout import rank_gym_workouts,read_criteria
from GymWorkout.Insights_usha.insights_usha1 import fetch_data, process_data, plot_bar_chart, plot_pie_chart,top_5_equipments
from Exercise.ReadTextfiles import rank_exercise_files, print_top_three_justification, load_criteria
from Nutrition.Nutrition import reading_criteria, calculate_weight, selecting_top3_files, assign_ranks
from Yoga.Yoga_ranking import rank_yoga_workouts, read_criteria
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import matplotlib.pyplot as plt
from Exercise.ScrapingInsights import save_html_to_file,read_html_file,count_unique_exercises, top_exercises_by_impact, top_exercises_by_weight, plot_histogram_top_exercises, plot_unique_exercises_count, plot_top_exercises_by_impact, plot_top_exercises_by_weight

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
folder_path_Gymworkout = "/Users/usha/Library/Mobile Documents/com~apple~CloudDocs/Data Science/Data wrangling/ZIVA/GymWorkout/Ranking_Selection"
criteria_file_GymWorkout = "//Users/usha/Library/Mobile Documents/com~apple~CloudDocs/Data Science/Data wrangling/ZIVA/GymWorkout/criteria.json"
criteria_file_Gymworkout = read_criteria(criteria_file_GymWorkout)
sorted_files = rank_gym_workouts(folder_path_Gymworkout, criteria_file_Gymworkout)
top_files = sorted_files
# Prepare data for HTML template
top_files_details = []
for file_details in top_files[:3]:
    top_files_details.append({
        'file_name': file_details['file_name'],
        'score': file_details['score'],
        'Workout_Name': file_details['workout_name'],
        'Workout_Time': file_details['workout_time'],
        'Calories_Burned': file_details['calories_burned'],
        'justification': file_details['justification']
    })
all_files_details = []
for file_details in top_files:
    all_files_details.append({
        'file_name': file_details['file_name'],
        'score': file_details['score'],
        'Workout_Name': file_details['workout_name'],
        'Workout_Time': file_details['workout_time'],
        'Calories_Burned': file_details['calories_burned'],
        'file_content': file_details['file_content']
    })

folder_path_yoga = "/Users/usha/Library/Mobile Documents/com~apple~CloudDocs/Data Science/Data wrangling/ZIVA/Yoga/Yoga_txt_files"
criteria_file_yoga = "//Users/usha/Library/Mobile Documents/com~apple~CloudDocs/Data Science/Data wrangling/ZIVA/Yoga/templates/Yoga_criteria.json"
criteria_file_yoga = read_criteria(criteria_file_yoga)
sorted_files = rank_yoga_workouts(folder_path_yoga, criteria_file_yoga)
top_files = sorted_files
# Prepare data for HTML template
top_files_details_yoga = []
for file_details in top_files[:3]:
    top_files_details_yoga.append({
        'file_name': file_details['file_name'],
        'score': file_details['score'],
        'workout_name': file_details['workout_name'],
        'workout_time': file_details['workout_time'],
        'number_of_yogas': file_details['number_of_yogas'],
        'justification': file_details['justification']
     })
all_files_details_yoga = []
for file_details in top_files:
    all_files_details_yoga.append({
        'file_name': file_details['file_name'],
        'score': file_details['score'],
        'workout_name': file_details['workout_name'],
        'workout_time': file_details['workout_time'],
        'number_of_yogas': file_details['number_of_yogas'],
        'file_content': file_details['file_content']
    })
templates_GYMWorkout = Jinja2Templates(directory="GymWorkout/templates_GymWorkout")
templates_Insights_GYMWorkout = Jinja2Templates(directory="GymWorkout/Insights_usha/templates")
templates_exercise = Jinja2Templates(directory="Exercise/templates_exercise")
templates_Nutrition = Jinja2Templates(directory='Nutrition/Templates_Nutrition')
templates_yoga = Jinja2Templates(directory="Yoga/templates")

# Define the folder path containing exercise files
exercise_folder_path = "/Users/usha/Library/Mobile Documents/com~apple~CloudDocs/Data Science/Data wrangling/ZIVA/Exercise/Ranking_Selection_Exercise"
# Load criteria (assuming the criteria_Exercise.json file is in the same folder as ExerciseMain.py)
criteria_file_exercise = "/Users/usha/Library/Mobile Documents/com~apple~CloudDocs/Data Science/Data wrangling/ZIVA/Exercise/criteria_Exercise.json"
criteria_exercise = load_criteria(criteria_file_exercise)

# Define the folder path containing exercise files
Nutrition_folder_path = r'/Users/usha/Library/Mobile Documents/com~apple~CloudDocs/Data Science/Data wrangling/ZIVA/Nutrition/text_files'
Nutrition_criteria_file = r'/Users/usha/Library/Mobile Documents/com~apple~CloudDocs/Data Science/Data wrangling/ZIVA/Nutrition/criteria_Nutrition.txt'

app.mount("/static1", StaticFiles(directory="/Users/usha/Library/Mobile Documents/com~apple~CloudDocs/Data Science/Data wrangling/ZIVA"), name="static1")

# Call the function to read HTML file and create DataFrame
url = "https://hr.uky.edu/wellness/exercise-calories-burned-hour"
file_path = "/Users/usha/Library/Mobile Documents/com~apple~CloudDocs/Data Science/Data wrangling/ZIVA/Exercise/exercise_calories_burned_hour.html"
df = read_html_file(file_path)

def get_file_names():
    """
        Retrieve file names of exercise files.
    """
    # Rank exercise files
    ranked_files = rank_exercise_files(exercise_folder_path, criteria_exercise)
    return [exercise['file_name'] for exercise in ranked_files]


def get_file_data():
    """
        Retrieve file data including name, image URL, and description.
        """
    file_data = [
        {"name": "Boxing.txt",
         "image_url": "https://media4.giphy.com/media/hVOgpyzqVbFsy8MRJw/giphy.gif?cid=6c09b9525ocoiek9j3kjkp5jpwjecgcichh7szpwy24s4n37&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
         "description": "Boxing classes can be adapted for fitness and experience levels but generally include three segments or types of exercise:Cardiovascular. \n"
         "Most classes begin with a warm-up and a cardio session that varies in intensity, depending on the participants or class level. \n"
         "This could include agility moves, jumping rope, and other moves that amp up heart rate quickly.Strength.\n"
         "Boxing requires strength. \n"
         "If you look at any pro boxer, you can tell that they spend time building muscle.\n"
         "Boxing classes usually have a strength training portion that includes core work.\n"
         "Boxing Intervals. Of course, the class also includes actual boxing, typically with a bag.\n" " In one-on-one classes, you might hit into the instructor’s punching mitts.\n" " In a kickboxing class, you’ll use your feet as well. \n" "This portion of the workout is usually in a HIIT (high intensity interval training) format with rest periods. "},
        {"name": "Cycling.txt", "image_url": "https://i.pinimg.com/originals/3c/83/ff/3c83ffe2b36ba546be60597b715dd08b.gif",
         "description": "Some posture tips to remember when cycling: Keep your shoulders back. Keep your elbows slightly bent.Keep a light touch on the handlebars and don’t put too much pressure on your arms.Keep your chin down and neck stretched."},
        {"name": "Dancing.txt",
         "image_url": "https://media1.giphy.com/media/MS1i4ydVFsRVEL52gU/giphy.gif?cid=6c09b952cxoaz39gq95gyttnspt4bvvizl2vpqwyy6pzwzal&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
         "description": "Warm-ups prime your body for dance, which may help prevent injuries, Roup says. Spend a few minutes doing light cardio to bring your heart rate up and perform a few dynamic stretches to fire up your muscles. Hip rolls, body rolls, chest isolations, and light jumps are all great options. If you’re attending a dance workout class, a warm-up may be part of it."},
        {"name": "Hiking.txt",
         "image_url": "https://i.makeagif.com/media/4-23-2016/_tx5hV.gif",
         "description": "Take yourself out for a walk two or three times during the week. Make sure to move briskly enough to get your heart rate up, and then keep it up for at least 30 minutes.Be sure to wear the same shoes that you'll be wearing on your hike. ...Carry a lightly-weighted daypack on your weekday walks."},
        {"name": "HorsebackRiding.txt",
         "image_url": "https://i.gifer.com/2Fyd.gif",
         "description": "Try doing pull ups, push ups, or other back-related workouts. Swimming is also a good option. Many beginner and intermediate riders focus too much on abdominal strength and end up leaning forward in the saddle. Counter this tendency by exercising back muscles and think "'lean back'" instead of "'sit up'" when on the horse."},
        {"name": "JumpRope.txt",
         "image_url": "https://www.thepespecialist.com/wp-content/uploads/2018/02/giphy-26.gif",
         "description": "Bounce Low. ...Stay on the balls of your feet with only a slight bend in the knees. ...Hand positioning is key. ...Wrist Rotation. ...Shoten your rope. ...Use the correct rope type."},
        {"name": "Kayaking.txt",
         "image_url": "https://www.tontron-on.com/wp-content/uploads/2022/05/8%E3%80%81Forward-and-reverse-sweep-strokes-3_Tontron.gif",
         "description": "Line the kayak up so it’s parallel to the shore.Stabilize yourself by placing your paddle at a 90-degree angle behind the seat. Half of your paddle should be on the shore and the other half should be lying across the boat.Sit on the half of the paddle that’s on the shore and place your feet into the boat.Swiftly slide along the paddle and onto the kayak while holding onto the paddle underneath and next to you. The paddle and boat will hold up your weight during this movement.Move into the seat. Make sure to keep low and enter as smoothly as possible. Don’t forget to remain calm and focus on keeping your balance.Lay the paddle across your lap. Use your hands — or your paddle if you need an extra boost — to push off the shoreline."},
        {"name": "Pilates.txt",
         "image_url": "https://i.pinimg.com/originals/fc/f5/cc/fcf5cc79875103ac57b45db038642678.gif",
         "description": "Centering: This is the practice of bringing your awareness to the center of your body—the area between the lower ribs and pubic bone. This central region of the core powers all Pilates exercises.Concentration: By focusing on each exercise with your full attention, you will yield maximum results from each movement.Control: Complete muscular control requires conscious, deliberate movement and is emphasized in every Pilates exercise."},
        {"name": "RockClimbing.txt",
         "image_url": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExd2pkaWJxb2I1cm44NG1vdzhnYmNnNmRubmo0eXlzbHliemwyNTFteSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kbPvi0OavYKcJI0Gkw/giphy.gif",
         "description": "Practice moving with ‘quiet feet’ – Gently/slowly move your feet from hold to hold while traversing through the gym.Try climbing with ‘high feet’ when warming up on top ropes – Get you feet up as high as you can, once they are up stand as tall and high as you can reaching for the next hand holds. Do this all the way up the wall. Add variation by changing your handhold grip positions.Other warm-up options include climbing easy routes on big, positive holds (i.e. jugs), and finger sprinklers (flicking your fingers like they have water on them)."},
        {"name": "Rowing.txt",
         "image_url": "https://i.makeagif.com/media/5-30-2017/aKzydh.gif",
         "description": "1 min row at low intensity, 1 min rest, repeat 5 times. Session 2: 5 min row at low intensity, 3 min rest, repeat 2 times. Aim: Increase the time you exercise and focus on using good technique. Think about rowing smoothly with a focus on the powerful drive, then slow recovery."},
        {"name": "Running.txt",
         "image_url": "https://i.pinimg.com/originals/a5/07/ba/a507ba128c87d62f031dbc31bf294304.gif",
         "description": "A warmup and cooldown will help you ease in and out of a run. Start with a few reverse lunges on each leg, followed by squats, side lunges, butt kicks, and high knees before your run. After, take a few minutes to walk slowly, then foam roll your legs (the quads, hamstrings, and calves are good places to work on) or stretch."},
        {"name": "Soccer.txt",
         "image_url": "https://i.pinimg.com/originals/ea/49/61/ea4961f01c9aeb5dccbeb3f2ede0bc4d.gif",
         "description": "Run  and down a flight of stairs for 2 minutes.60 seconds rest.Single leg hop up two stairs with right leg then hop up two stairs with left leg. You can add to stair hops when you get used to two steps.60 seconds rest.Run continuously up and down the flight of stairs for 2 minutes."},
        {"name": "Surfing.txt",
         "image_url": "https://assets-global.website-files.com/613f686e92b10d496b9a654f/619938709ad0e532b14c0eb0_cardboard-slide.gif",
         "description": "Squats. Lower-body strength is indispensable for surfing. ...Push-ups. Though surfing is mostly a leg-focused sport, the strength of upper-body cannot be negligible. ...Plank. ...Superman. ...Burpee."},
        {"name": "Swimming.txt",
         "image_url": "https://cdn.shopify.com/s/files/1/2625/0944/files/gif_4-5_7_copy_2.gif?v=1620131903",
         "description": "Swim one lap (from one end of the pool to the other end). Use a kick board for the second lap, relying on just your legs to push you forward. Use a pull buoy for the third lap, relying on just your arms to pull you forward. Repeat for 15 to 20 minutes for a great full body workout"},
        {"name": "TrailRunning.txt",
         "image_url": "https://media1.tenor.com/m/-8s6k_Wjra0AAAAC/trailrunning.gif",
         "description": "When running uphill, you’ll want to lean forward slightly and place your weight over the balls of your feet. Exaggerating your arm swing a bit more will also help you carry your momentum and improve your balance over rocks and uneven terrain. For downhills, get used to scanning about 10 to 15 feet ahead of you.This will help you pick a good line well before you’re in that section.Keep your steps light and short, as a quicker turnover is more efficient and much safer than long, lunging steps.Avoid leaning back too much, as it can stop your momentum and burn out your quadriceps.Focus on an upright posture when heading downhill to improve your efficiency."},
    ]
    return file_data
def save_scraped_file():
    """
        Retrieve file names of exercise files.
    """
    save_html_to_file(url, file_path)
    return file_path

@app.get("/display", response_class=HTMLResponse)
def display_template(request: Request):
    """
        Display Table Scraped from the website and preprocessed "Impact" column
    """
    unique_exercises_count = count_unique_exercises(df)
    return templates_exercise.TemplateResponse("Scraperdisplay.html", {"request": request, "df": df, "unique_exercises_count": unique_exercises_count})

@app.get("/findings", response_class=HTMLResponse)
def display_findings(request: Request, impact: str = Query("high"), weight: str = Query("180 lbs")):
    """
    Display the findings from the ScraperInsights functions.
    """
    unique_exercises_count = count_unique_exercises(df)
    top_impact_exercises = top_exercises_by_impact(df, impact)
    top_weight_exercises = top_exercises_by_weight(df, weight)
    return templates_exercise.TemplateResponse("Scraperfindings.html", {"request": request,
                                                       "unique_exercises_count": unique_exercises_count,
                                                       "top_impact_exercises": top_impact_exercises,
                                                       "top_weight_exercises": top_weight_exercises})

# Directory to save the plot images
plots_directory = "plots"

# Ensure the directory exists
os.makedirs(plots_directory, exist_ok=True)
def save_plot_to_file(plot, filename):
    """
    Save the plot to a file.

    Args:
        plot: Matplotlib plot object.
        filename (str): Name of the file to save the plot.

    Returns:
        str: Path to the saved image file.
    """
    filepath = os.path.join(plots_directory, filename)
    plot.savefig(filepath, format='png')
    plt.close()
    return filepath

def generate_plots(df, weight=None, impact=None):
    """
    Generate all plots based on the provided DataFrame and optional user input for weight and impact.

    Args:
        df (pandas.DataFrame): The DataFrame containing exercise data.
        weight (str, optional): The weight for which calories burned are provided.
        impact (str, optional): The impact keyword.

    Returns:
        List[Tuple[plt.Figure, str]]: List of tuples containing the plot and its title.
    """
    plots = []

    # Plot top exercises by impact
    if impact:
        plot = plot_top_exercises_by_impact(df, impact, weight)
        plots.append((plot, f"Top Exercises by Impact: {impact}"))

    # Plot top exercises by weight
    if weight:
        plot = plot_top_exercises_by_weight(df, weight)
        plots.append((plot, f"Top Exercises by Weight: {weight}"))

    # Plot unique exercises count
    plot = plot_unique_exercises_count(df)
    plots.append((plot, "Count of Unique Exercises by Impact Category"))

    # Plot histogram top exercises
    plot = plot_histogram_top_exercises(df)
    plots.append((plot, "Top 3 Unique Exercises by Weight Category"))

    return plots

@app.get("/plots", response_class=HTMLResponse)
async def display_plots(
    request: Request,
    weight: str = Query("180 lbs"),
    impact: str = Query("high")
):
    # Generate plots
    plots = generate_plots(df, weight, impact)

    # Generate HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Exercise Plots</title>
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-4">
            <h2>Exercise Plots</h2>
    """
    # Add img tags for each plot with titles
    for i, (plot, title) in enumerate(plots):
        plot_path = save_plot_to_file(plot, f"plot_{i}.png")
        html_content += f"""
            <div class="mt-4">
                <h3>{title}</h3>
                <img src="/static1/{plot_path}" class="img-fluid" alt="{title}">
            </div>
        """

    html_content += """
        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content, status_code=200)

@app.get("/recommendations", response_class=HTMLResponse)
def finding_template(request: Request):
    """
        Display Table Scraped from the website and preprocessed "Impact" column
    """
    #unique_exercises_count = count_unique_exercises(df)
    return templates_exercise.TemplateResponse("Scraperrecommendations.html", {"request": request})


@app.get("/hourly-calorie-blasters")
async def get_hourly_calorie_blasters():
    return FileResponse("/Users/usha/Library/Mobile Documents/com~apple~CloudDocs/Data Science/Data wrangling/ZIVA/Exercise/templates_exercise/scraperindex.html")


# Define the function to retrieve top three files
def get_top_three_files():
    """
       Retrieve the top three exercise files based on ranking.
       """
    ranked_files = rank_exercise_files(exercise_folder_path, criteria_exercise)
    return ranked_files[:3]

@app.get("/")
def root():
    with open("main.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200, media_type="text/html")

@app.get("/user_profile")
def user_profile():
    return {"message": "user_profile"}

@app.get("/Yoga", response_class=HTMLResponse)
def Yoga(request: Request):
    return templates_yoga.TemplateResponse("Yoga_Ziva.html", {
            "request": request,
            "top_files_details": top_files_details_yoga,
            "all_files_details": all_files_details_yoga
    })

@app.get("/Yoga_insights", response_class=HTMLResponse)
async def yoga_insights(request: Request):
    # Render the HTML template and pass any necessary data
    return templates_yoga.TemplateResponse("Agrgregation_yoga.html", {"request": request})

@app.get("/GYM_Workouts")
def GYM_Workouts(request: Request):
    return templates_GYMWorkout.TemplateResponse("GYM_workout.html", {
        "request": request,
        "top_files_details": top_files_details,
        "all_files_details": all_files_details
    })


@app.get("/Insights_Gymworkouts")
async def Insights_Gymworkouts(request: Request):
    url = "https://zuka.p.rapidapi.com/"
    headers = {
        "X-RapidAPI-Key": "c90039b8d8msh051fa04416bf48ap1016a3jsn475eca3ffd88",
        "X-RapidAPI-Host": "zuka.p.rapidapi.com"
    }
    data = fetch_data(url, headers)

    # Process data to get insights
    body_parts_count, equipment_count, target_count_by_body_part, most_common_exercises = process_data(data)

    # Generate the plots - Ensure the images are saved in a directory served by FastAPI under 'static'
    plot_bar_chart(body_parts_count, 'Exercise Distribution by Body Part', 'Body Part', 'Number of Exercises')
    equipment_labels = list(equipment_count.keys())
    plot_pie_chart(list(equipment_count.values()), equipment_labels, 'Equipment Distribution')

    # Fixing the AttributeError by ensuring target_count_by_body_part is a dictionary
    target_count_by_body_part = dict(target_count_by_body_part)

    # Iterate over the dictionary items properly
    for body_part, targets in target_count_by_body_part.items():
        # Assuming targets is a dictionary, get the first key-value pair as the most common target
        first_target_key = max(targets, key=targets.get)  # Adjusted to select the max value
        first_target_value = targets[first_target_key]
        target_count_by_body_part[body_part] = (first_target_key, first_target_value)

    # Call the function top_5_equipments correctly (if it's a function)
    top_5_equipments_result = top_5_equipments(equipment_count)

    # Return the processed data to the template
    return templates_Insights_GYMWorkout.TemplateResponse("Insights_Gymworkout.html", {
        "request": request,
        "Exercise_Distribution": body_parts_count,
        "Equipment_Distribution": equipment_count,
        "Common_Targets": target_count_by_body_part,
        "most_common_exercises": most_common_exercises,
        "top_5_equipments": top_5_equipments_result  # Adjusted variable name
    })


@app.get("/Nutrition", response_class=HTMLResponse)
async def Nutrition(request: Request):
    # Read criteria
    criteria_Nutrition = reading_criteria(Nutrition_criteria_file)

    # Select top files
    sorted_files = selecting_top3_files(Nutrition_folder_path, criteria_Nutrition)

    # Assign ranks to files
    ranked_files = assign_ranks(sorted_files)

    # Calculate details for top files
    top_files_details = []
    for rank, (file_rank, filename, score) in enumerate(ranked_files[:3], start=1):
        file_path = os.path.join(Nutrition_folder_path, filename)
        calories, protein, fiber = calculate_weight(file_path, criteria_Nutrition)
        justification = f"This {filename} file is ranked {file_rank} with {calories} calories, {protein} grams of protein and {fiber} grams of fiber"
        top_files_details.append({'rank': rank, 'filename': filename, 'justification': justification})

    # Calculate details for all files
    all_files_details = []
    for rank, (file_rank, filename, score) in enumerate(ranked_files, start=1):
        file_path = os.path.join(Nutrition_folder_path, filename)
        calories, protein, fiber = calculate_weight(file_path, criteria_Nutrition)
        justification = f"This {filename} file is ranked {file_rank} with {calories} calories, {protein} grams of protein and {fiber} grams of fiber"
        all_files_details.append({'rank': rank, 'filename': filename, 'justification': justification})

    return templates_Nutrition.TemplateResponse("nutrition.html", {
        "request": request,
        "top_files_details": top_files_details,
        "all_files_details": all_files_details})
@app.get("/nutrition-insights", response_class=HTMLResponse)
def nutrition_insights(request: Request):
    return templates_Nutrition.TemplateResponse("mining_integration.html",  {"request": request})

@app.get("/exercise", response_class=HTMLResponse)
def exercise(request: Request):
    file_names = get_file_names()
    return templates_exercise.TemplateResponse("Index.html", {
        "request": request,
        "file_names": file_names})

@app.get("/priority-files", response_class=HTMLResponse)
def get_priority_files(request: Request):
    """
    Get a list of all exercise files ranked based on criteria.
    """
    file_names = get_file_names()
    file_data =  get_file_data()
    file_dict = {file["name"]: {"image_url": file["image_url"], "description": file["description"]} for file in
                 file_data}

    return templates_exercise.TemplateResponse("priority_files.html",
                                      {"request": request, "file_names": file_names, "file_dict": file_dict})


@app.get("/selected-files", response_class=HTMLResponse)  # response_model=List[Dict[str, Any]])
def get_selected_files(request: Request):
    """
    Get detailed justification for the top three exercise files.
    """
    top_three_files = get_top_three_files()
    justification_list = print_top_three_justification(top_three_files)
    justification = [item['justification'] for item in justification_list]
    return templates_exercise.TemplateResponse("Selected_Files.html", {"request": request, "top_three_files": top_three_files,
                                                              "justification": justification})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
