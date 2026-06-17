from file_handling import get_cleaned_data
import seaborn as sns
import pandas as pd

data = get_cleaned_data()

#implementing week column
data["date"] = pd.to_datetime(data["date"])
data["week"] = data["date"].dt.to_period("W").apply(lambda r: r.start_time)

#creating a average summary table of excercise per week
weekly_data = data.groupby(["exercise_title", "week"]).agg(
    avg_weight_kg=("weight_kg", "mean"),
    max_weight_kg=("weight_kg", "max"),
    avg_reps=("reps", "mean"),
    total_reps=("reps", "sum"),
    num_sets=("set_number", "count")
).reset_index()

weekly_data = weekly_data.sort_values(["exercise_title", "week"])#sort excercise title and week to make sure the next week weight is correct
weekly_data["next_week_weight"] = (weekly_data.groupby("exercise_title")["max_weight_kg"].shift(-1))
##create a new column with the max weight of the next week for each exercise,
# shift(-1) moves the values up by one row so that the next week weight is in the same row as the current week
weekly_data = weekly_data.dropna(subset=["next_week_weight"])#drop rows where next week weight is missing, which will be the last week of each exercise since there is no next week data for it

correlation = weekly_data.select_dtypes(include=["number"]).corr()["next_week_weight"]

print(correlation)

from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression

features = ["avg_weight_kg", "max_weight_kg", "avg_reps", "total_reps", "num_sets"]#use the average weight, max weight, average reps, total reps and number of sets as features for the linear regression model
x = weekly_data[features]
y = weekly_data["next_week_weight"]#target variable for linear regression model

model = LinearRegression()

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)#split the data into training and testing sets, using 80% of the data for training and 20% for testing, with a random state of 42 for reproducibility

model.fit(X_train, y_train)#use training data to fit the linear regression model

predictions = model.predict(X_test)#use the fitted linear regression model to make predictions on the testing data
model_mae = mean_absolute_error(y_test, predictions)#mae calculation

baseline_predictions = X_test["max_weight_kg"]#use current week max weight as baseline prediction for next week weight
baseline_mae = mean_absolute_error(y_test, baseline_predictions)#calculate the mean absolute error between the baseline predictions and the actual test values to evaluate the performance of the baseline model

print("Model MAE:", model_mae, "Baseline MAE:", baseline_mae)
