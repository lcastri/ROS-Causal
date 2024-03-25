import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import yaml
import os
import json

# Params definition
MAP_DIR = os.getcwd() + '/trajectory_plot/maps/'
MAP_NAME = 'inb3235'
AGENT = 'A1'
TRAJ_CSV = os.getcwd() + '/trajectory_plot/trajectories/' + AGENT + '_traj.csv'
SEL_ID = '1000_' # NOTE: set '' if not needed
GOALS_PATH = os.getcwd() + '/trajectory_plot/goals.json'
HUMAN_COLOR = 'tab:blue'
ROBOT_COLOR = 'tab:orange'

with open(GOALS_PATH, 'r') as json_file:
    GOALS = json.load(json_file)

with open(MAP_DIR + MAP_NAME + '/map.yaml', 'r') as yaml_file:
    map_info = yaml.safe_load(yaml_file)

# Step 1: Load the PNG Image
map_image = mpimg.imread(MAP_DIR + MAP_NAME + '/map.pgm')

# Step 2: Plot the Map
# Get resolution and origin from YAML
resolution = map_info['resolution']
origin_x, origin_y = map_info['origin'][:2]

# Plot the map image
plt.imshow(map_image, extent=(origin_x, origin_x + len(map_image[0]) * resolution, 
                              origin_y, origin_y + len(map_image) * resolution),
           cmap='gray')

# Step 3: Load Trajectory Data
trajectory_data = pd.read_csv(TRAJ_CSV)

# Step 4: Plot Trajectories
plt.plot(trajectory_data['r_x'].values, trajectory_data['r_y'].values, color=ROBOT_COLOR, label=f'TIAGo', zorder=3)
plt.plot(trajectory_data['h_' + SEL_ID + 'x'].values, trajectory_data['h_' + SEL_ID + 'y'].values, color=HUMAN_COLOR, label=AGENT)

# Step 5: Plot goals
for gid, g in GOALS.items():
    plt.scatter(g['x'], g['y'], s=500, color='green', alpha=0.5, zorder=2)
    plt.text(g['x'], g['y'], gid, ha='center', va='center')

# Add labels and legend
plt.xlabel('X')
plt.ylabel('Y')
plt.title('HRSI: TIAGo - ' + AGENT)
plt.legend()

# Set axis limits
plt.xlim(-1, 8.5)  # Set x-axis limits from 0 to 6
plt.ylim(-6, 4)  # Set y-axis limits from 0 to 12

# Show plot
plt.show()



