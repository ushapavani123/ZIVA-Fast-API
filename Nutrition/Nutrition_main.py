from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from Nutrition import reading_criteria, calculate_weight, selecting_top3_files, assign_ranks
import os

app = FastAPI()
Nutrition_folder_path = r'/Users/usha/Library/Mobile Documents/com~apple~CloudDocs/Data Science/Data wrangling/ProjectDW/Ranking_Selection'
Nutrition_criteria_file = r'/Users/usha/Library/Mobile Documents/com~apple~CloudDocs/Data Science/Data wrangling/ProjectDW/criteria.json'

Nutrition_Templates = Jinja2Templates(directory='Templates_Nutrition')


@app.get("/")
def root():
    return {"message": "ZIVA"}


@app.get("/user_profile")
def user_profile():
    return {"message": "user_profile"}


@app.get("/Yoga")
def Yoga():
    return {"message": "Yoga"}


@app.get("/Exercise")
def Exercise():
    return {"message": "Exercise"}


@app.get("/GYM_Workouts")
def GYM_Workouts():
    return {"message": "GYM Workouts"}


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

    return Nutrition_Templates.TemplateResponse("nutrition.html", {"request": request, "top_files_details": top_files_details, "all_files_details": all_files_details})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
