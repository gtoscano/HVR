import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D


def read_all_files(file_list, columns):
    all_data = []
    
    for file_path in file_list:
        # Read only the specified columns from the CSV file
        df = pd.read_csv(file_path, usecols=columns)
        # Convert the extracted columns to a list and extend all_data
        all_data.extend(df[columns].values.tolist())
    all_data_df = pd.DataFrame(all_data, columns=columns)
    
    return all_data_df * -1.0

file_list = ['finalresults_0001-rcp8.5_gen20.csv', 'finalresults_0001-rcp8.5_gen40.csv', 'finalresults_0001-rcp8.5_gen80.csv' ]
data_names = ['20', '40', '80']

all_solutions = read_all_files(file_list, ['yield_mz','yield_sb','yield_wh'])
ideal = all_solutions.min()
nadir = all_solutions.max()
print(ideal)
print(nadir)

set1= read_all_files([file_list[0]], ['yield_mz','yield_sb','yield_wh'])
print(set1)
set2= read_all_files([file_list[1]], ['yield_mz','yield_sb','yield_wh'])
set3= read_all_files([file_list[2]], ['yield_mz','yield_sb','yield_wh'])

data_sets = [set1, set2, set3]
colors = ['red', 'blue', 'green']
markers = ['.', '^', 's']  # 'o' for circle, '^' for triangle, 's' for square

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

for i, data_set in enumerate(data_sets):
    df = pd.DataFrame(data_set, columns=['yield_mz','yield_sb','yield_wh'])
    ax.scatter(df['yield_mz'], df['yield_sb'], df['yield_wh'], c=colors[i], marker=markers[i], label='{} gens'.format(data_names[i]), s=50)  # s=50 sets the size of the markers

ax.set_xlim(ideal['yield_mz'], nadir['yield_mz'])
ax.set_ylim(ideal['yield_sb'], nadir['yield_sb'])
ax.set_zlim(ideal['yield_wh'], nadir['yield_wh'])

ax.set_xlabel('mz')
ax.set_ylabel('sb')
ax.set_zlabel('wh')
ax.legend()
plt.show()

