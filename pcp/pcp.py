#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

def count_crossings_per_column(df):
    crossings_list = []
    crossings_dict = {}
    # Iterate over each pair of columns
    for i in range(len(df.columns) - 1):
        crossings = 0
        col1 = df.iloc[:, i]
        col2 = df.iloc[:, i + 1]
        # For each pair of rows in these columns
        for j in range(len(df) - 1):
            for k in range(j + 1, len(df)):
                # Check if the lines cross
                if (col1.iloc[j] - col1.iloc[k]) * (col2.iloc[j] - col2.iloc[k]) < 0:
                    crossings += 1
        crossings_list.append(crossings)
        crossings_dict[df.columns[i]] = crossings
    return crossings_list, crossings_dict

def count_crossings(df):
    crossings = 0
    # Iterate over each pair of columns
    for i in range(len(df.columns) - 1):
        col1 = df.iloc[:, i]
        col2 = df.iloc[:, i + 1]
        # For each pair of rows in these columns
        for j in range(len(df) - 1):
            for k in range(j + 1, len(df)):
                # Check if the lines cross
                if (col1.iloc[j] - col1.iloc[k]) * (col2.iloc[j] - col2.iloc[k]) < 0:
                    crossings += 1
    return crossings

def best_corr(df):
    results = {}
    orders = {}
    for column in df.columns.tolist():
        columns_ordered = df.corr()[column].sort_values().index #best f_10: 8
        data_normalized = df[columns_ordered]
        crossings = count_crossings(data_normalized)
        results[column] = crossings
        orders[column] = columns_ordered

    sorted_list = sorted(results.items(), key=lambda x: x[1])
    return sorted_list, orders



def pcp(filename):
    # Load the CSV file into a pandas DataFrame
    data = pd.read_csv(filename)
    # Select only the last 13 columns
    data = data.iloc[:, -13:]
    
    # Normalize the data to the range [0, 1]
    scaler = MinMaxScaler()
    data_normalized = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
    
    # Reorder columns by their mean value
    columns_ordered = data_normalized.mean().sort_values().index
    columns_ordered = data_normalized.median().sort_values().index
    columns_ordered = data_normalized.sum().sort_values().index
    columns_ordered = (data_normalized.max() - data_normalized.min()).sort_values().index
    ## By variance
    columns_ordered = data_normalized.var().sort_values().index

    ## By standard deviation
    columns_ordered = data_normalized.std().sort_values().index

    ## Assuming 'target' is your column of interest
    corr_sorted, orders = best_corr(data_normalized)
    column_selected = corr_sorted[0][0]
    crossings = corr_sorted[0][1]
    columns_ordered = orders[column_selected]
    print("Number of Crossings:", crossings)
    #columns_ordered = ['column1', 'column2', 'column3', ..., 'column13']

    data_normalized = data_normalized[columns_ordered]

    crossing_dict = count_crossings_per_column(data_normalized)

    print(crossing_dict)


    # Add a color column using the first column of the data
    # convert it to str to avoid interpretation as a numeric class
    data_normalized['color_class_column'] = data_normalized.iloc[:,0].astype(str)
    
    # Add dummy class column for coloring
    #data_normalized['color_class_column'] = 1 
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    parallel_coordinates(data_normalized, 'color_class_column', colormap=plt.get_cmap("cool"))
    
    # Save the figure
    plt.savefig('pcp.png')
    
    # Show the plot
    plt.show()

if __name__ == '__main__':
    filename = 'dssat_var_and_functions.csv'
    pass
    pcp(filename)

