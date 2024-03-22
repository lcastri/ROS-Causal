import json
import os
import pandas as pd
   
GOALS_JSON = os.getcwd() + '/trajectory_plot/goals.json'
CSV_PATH = os.getcwd() + '/bag_processing_ws/src/bag_processing_bringup/traj/'


        
def convert_time(df):
    # Convert the 'time' column from epoch format to datetime
    tmp_time = pd.to_datetime(df['time'], unit='s')
    
    # Calculate the time difference in seconds
    df['time_seconds'] = (tmp_time - tmp_time.iloc[0]).dt.total_seconds()


# Define a function to determine the goal ID based on coordinates
def get_goal_id(x, y):
    for goal_id, goal_info in GOALS.items():
        if x == goal_info['x'] and y == goal_info['y']: return goal_id
    return None


def add_goalID(df):
    # Apply the function to create the 'goalID' column
    df['goalID'] = df.apply(lambda row: get_goal_id(row['h_1000_{gx}'], row['h_1000_{gy}']), axis=1)

    # Save the modified DataFrame back to the CSV file
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]


if __name__ == '__main__':
    
    with open(GOALS_JSON, 'r') as json_file:
        GOALS = json.load(json_file)
    
    for i in range(1, 16):
        input_csv_path = "A" + str(i) + "_traj.csv"  # Replace with your input CSV file path
        output_csv_path = "A" + str(i) + "_traj.csv"  # Replace with your desired output CSV file path
        df = pd.read_csv(CSV_PATH + input_csv_path)
        
        add_goalID(df)
        convert_time(df)
        
        # Save the modified DataFrame back to the CSV file
        df.to_csv(CSV_PATH + output_csv_path, index=False)