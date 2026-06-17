import pandas as pd
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_paths = [
os.path.join(BASE_DIR, "data", "workout_data1.csv"),
os.path.join(BASE_DIR, "data", "workout_data2.csv"),
os.path.join(BASE_DIR, "data", "workout_data3.csv")
]

all_data = pd.DataFrame()
for file_path in file_paths:
    if os.path.exists(file_path):#checks if file exists
        data = pd.read_csv(file_path)
        if "weight_kg" not in data.columns and "weight_lbs" in data.columns:#if user is using lbs
            data["weight_kg"] = pd.to_numeric(data["weight_lbs"], errors="coerce") * 0.453592#lbs conversion
        elif "weight_kg" in data.columns:#if using kg ignore
            data["weight_kg"] = pd.to_numeric(data["weight_kg"], errors="coerce")#empties column if there are no values in weight column
        else:
            continue
        all_data = pd.concat([all_data, data], ignore_index=True)
    else:
        print(f"File not found: {file_path}")#if file doesnt exist print error
if all_data.empty:
    raise FileNotFoundError("No workout CSV files were found.")


#filter appropraite columns for linear regression model
columns_to_keep = ["start_time", "exercise_title", "set_index", "weight_kg", "reps"]
filtered_data = all_data[columns_to_keep].copy()


#convert set_index to set_number since the index starts with 0
filtered_data["set_index"] = pd.to_numeric(filtered_data["set_index"], errors="coerce")#convert set_index to numeric, if it fails convert to None
filtered_data["set_number"] = filtered_data["set_index"] +1
filtered_data = filtered_data.drop(columns=["set_index"])#drop set_index column created

#convert string date to datetime object
filtered_data["date"] = pd.to_datetime(filtered_data["start_time"], format="%d %b %Y, %H:%M").dt.date
filtered_data = filtered_data.drop(columns=["start_time"])#drop irellevant date string column

#drop rows with missing values
filtered_data = filtered_data.dropna(subset=["weight_kg", "reps", "set_number", "date"])
cleaned_data = filtered_data


def get_cleaned_data():#usage of function to reduce running time of code and to make it more modular
    return cleaned_data

