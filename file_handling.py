import pandas as pd
import os
file_paths = ["workout_data1.csv", "workout_data2.csv", "workout_data3.csv"]


for file_path in file_paths:
    if os.path.exists(file_path):#checks if file exists
        data = pd.read_csv(file_path)
        all_data = pd.concat([all_data, data], ignore_index=True) if 'all_data' in locals() else data#if all_data doesnt exist create it with the first file data
    else:
        print(f"File not found: {file_path}")#if file doesnt exist print error


#filter appropraite columns for linear regression model
columns_to_keep = ["start_time", "exercise_title", "set_index", "weight_kg", "reps"]
filtered_data = all_data[columns_to_keep]

#convert string date to datetime object
filtered_data["date"] = pd.to_datetime(filtered_data["start_time"], format="%d %b %Y, %H:%M").dt.date
filtered_data = filtered_data.drop(columns=["start_time"])#drop irellevant date string column

print(filtered_data)

