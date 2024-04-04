from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import matplotlib.pyplot as plt
import uvicorn
import os
from starlette.staticfiles import StaticFiles
from ScrapingInsights import save_html_to_file,read_html_file,count_unique_exercises, top_exercises_by_impact, top_exercises_by_weight, plot_histogram_top_exercises, plot_unique_exercises_count, plot_top_exercises_by_impact, plot_top_exercises_by_weight

app = FastAPI()

# Mount the static directory to serve image files
app.mount("/static", StaticFiles(directory="/Users/purvamugdiya/PycharmProjects/Exercise/pythonProject1"), name="static")

# Initialize Jinja2Templates
templates = Jinja2Templates(directory="templates")

# Call the function to read HTML file and create DataFrame
url = "https://hr.uky.edu/wellness/exercise-calories-burned-hour"
file_path = "exercise_calories_burned_hour.html"
df = read_html_file(file_path)

'''
@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    """
        Render the home page with a list of file names.
        """
    #file_names = get_file_names()
    return templates.TemplateResponse("scraperindex.html", {"request": request})
'''
def save_scraped_file():
    """
        Retrieve file names of exercise files.
    """
    save_html_to_file(url, file_path)
    return file_path

@app.get("/display", response_class=HTMLResponse)
def finding_template(request: Request):
    """
        Display Table Scraped from the website and preprocessed "Impact" column
    """
    unique_exercises_count = count_unique_exercises(df)
    return templates.TemplateResponse("Scraperdisplay.html", {"request": request, "df": df, "unique_exercises_count": unique_exercises_count})

@app.get("/findings", response_class=HTMLResponse)
def display_findings(request: Request, impact: str = Query("high"), weight: str = Query("180 lbs")):
    """
    Display the findings from the ScraperInsights functions.
    """
    unique_exercises_count = count_unique_exercises(df)
    top_impact_exercises = top_exercises_by_impact(df, impact)
    top_weight_exercises = top_exercises_by_weight(df, weight)
    return templates.TemplateResponse("Scraperfindings.html", {"request": request,
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
                <img src="/static/{plot_path}" class="img-fluid" alt="{title}">
            </div>
        """

    html_content += """
        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content, status_code=200)

if __name__ == "__main__":

    uvicorn.run(app, host='127.0.0.1', port=8000)
