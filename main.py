#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import subprocess
import numpy



def compute_hv(pf_path):
    hv_list = []
    b_hv_pf = subprocess.check_output(['./exec_hv', pf_path])
    hv = float(b_hv_pf)
    return hv


def read_all_files(file_list, columns):
    all_data = []
    
    for file_path in file_list:
        # Read only the specified columns from the CSV file
        df = pd.read_csv(file_path, usecols=columns)
        # Convert the extracted columns to a list and extend all_data
        all_data.extend(df[columns].values.tolist())
    all_data_df = pd.DataFrame(all_data, columns=columns)
    
    return all_data_df

def save_to_file(data, file_name):
    with open(file_name, 'w') as file:
        # Write the # character at the beginning of the file
        file.write("#\n")
        
        # Write the data, separated by spaces
        for row in data:
            file.write(" ".join(map(str, row)) + "\n")
        
        # Write the # character at the end of the file
        file.write("#\n")

def save_dataframe_to_file(df, file_name):
    with open(file_name, 'w') as file:
        # Write the # character at the beginning of the file
        file.write("#\n")
        
        # Write the DataFrame to the file with spaces as separators
        df.to_csv(file, sep=' ', index=False, header=False, float_format='%.6f')
        
        # Write the # character at the end of the file
        file.write("#\n")

if __name__ == '__main__':


    file_list = ['finalresults_0001-rcp8.5_gen20.csv', 'finalresults_0001-rcp8.5_gen40.csv', 'finalresults_0001-rcp8.5_gen80.csv' ]
    all_solutions= read_all_files(file_list, ['yield_mz','yield_sb','yield_wh'])
    nadir = all_solutions.min()
    ideal = all_solutions.max()


    # Normalize the data to the range [0, 1] using provided min and max
    data_normalized = (all_solutions - nadir) / (ideal - nadir)

    save_dataframe_to_file(data_normalized, 'accumulated_pf.out')
    accumulated_hv = compute_hv('accumulated_pf.out')
    print("HV of Accumulated PF: ", accumulated_hv)

    n = 0
    for pareto in file_list:
        filename = 'pareto_pf_{}.out'.format(n)
        solutions = read_all_files([pareto], ['yield_mz','yield_sb','yield_wh'])
        data_normalized = (solutions - nadir) / (ideal - nadir)
        save_dataframe_to_file(data_normalized, filename)
        pareto_hv = compute_hv(filename)
        print("HV of {}: ".format(n), pareto_hv)
        print("HVR o {}: ".format(n), pareto_hv / accumulated_hv)
        n += 1


