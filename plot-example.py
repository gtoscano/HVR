import matplotlib.pyplot as plt
import pandas as pd

# Sample data: 3 sets of values

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
set1= read_all_files([file_list[0]], ['yield_mz','yield_sb','yield_wh'])
set2= read_all_files([file_list[1]], ['yield_mz','yield_sb','yield_wh'])
set3= read_all_files([file_list[2]], ['yield_mz','yield_sb','yield_wh'])

data_sets = [set1, set2, set3]
colors = ['red', 'blue', 'green']

plt.figure(figsize=(10, 6))

for i, data_set in enumerate(data_sets):
    df = pd.DataFrame(data_set, columns=['f1', 'f2', 'f3'])
    plt.scatter(df['A'], df['B'], c=colors[i], label=f'Set {i + 1}')

plt.xlabel('A values')
plt.ylabel('B values')
plt.legend()
plt.grid(True)
plt.show()

