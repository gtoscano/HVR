import csv
import json
import numpy
import os
import pandas
import requests
import shutil
import subprocess 
import sys
import statistics
import time
from zipfile import ZipFile

from nds import nds
from dominance import compare_min
import pickle
import subprocess
import brewer2mpl
import random
import pandas as pd
import glob
import matplotlib.pyplot as plt
import seaborn as sns
from pylab import axes

from nds import nds
from dominance import compare_min
import statistics as stat

import matplotlib.pyplot as plt
sns.set_style("whitegrid", {'grid.linewidth': .3})

def compute_pf(objs):
    objs = numpy.asarray(objs)
    objs_len = len(objs)
    cnstrs = numpy.zeros((objs_len,1))
    fronts, ranks = nds(objs, cnstrs, compare_min)
    pf = objs[fronts[0]] 
    return pf.tolist()
                
def normalize_gens(path, cost, load, max_generations):

    for generation in range(1,max_generations):
        range_cost = cost[1] - cost[0]
        range_load = load[1] - load[0]
        filename = '{}/gen_{}_sol.out'.format(path, generation+1)
        print(filename)
        df = pd.read_csv(filename, sep='\t', header=None)
        df = df.rename(columns={0: 'cost', 1: 'load'})
        df['cost'] = (df['cost']-cost[0]) / range_cost
        df['load'] = (df['load']-load[0]) / range_load
        with open('{}/norm_gen_{}_sol.csv'.format(path, generation), 'w') as f:
            f.write("#\n")
            f.write(df.to_csv(index=False, header=False, sep=' '))
            f.write("#\n")

def normalize_fronts(pf_path, path, max_exec_idx, max_generations):
    with open (pf_path, 'rb') as f:
        data = pickle.load(f)
        bound_cost = data['cost']
        bound_load = data['load']
        pf = data['pf']

    range_cost = bound_cost[1]-bound_cost[0]
    range_load = bound_load[1]-bound_load[0]


    for idx in range(max_exec_idx):
        normalize_gens('{}/{}/results'.format(path, idx), bound_cost, bound_load, max_generations)

    normalized_pf = []
    for point in pf:
        normalized_pf.append([(point[0]-bound_cost[0])/range_cost, (point[1] - bound_load[0])/range_load])

    with open('{}/normalized_accumulated_pf.out'.format(path), 'w') as f:
        f.write('#\n')
        writer = csv.writer(f, delimiter=' ')
        writer.writerows(normalized_pf)
        f.write('#\n')

    
def compute_hv(pf_path, path, max_exec_idx, max_generations):
    normalize_fronts(pf_path, path, max_exec_idx, max_generations)
    hv_list = []
    b_hv_pf = subprocess.check_output(['./exec_hv', '{}/normalized_accumulated_pf.out'.format(path)])
    hv_pf = float(b_hv_pf)
    for generation in range(1, max_generations): 
        hvr = []
        for idx in range(max_exec_idx): 
            b_hv = subprocess.check_output(['./exec_hv', '{}/{}/results/norm_gen_{}_sol.csv'.format(path, idx, generation)])
            hvr.append(float(b_hv)/hv_pf)
        #median_idx = numpy.argsort(hv_tmp)[len(hv_tmp)//2]
        hv_list.append([stat.mean(hvr), stat.median(hvr), stat.stdev(hvr)])
    return hv_list

def create_plot(filename, values, labels, county):
    fig = plt.figure("hv_gen")
    ax = fig.add_subplot(111)
    ax.cla()
    ax.set_xlabel("Generations")
    ax.set_ylabel("HVR")
    plt.suptitle(county)
    #ax.boxplot(values, labels=labels) 
    idx= 0
    for data in values:
        x = list(range(len(data)))
        y = [item[0] for item in data]
        y2 = [item[1] for item in data]
        yerr = [item[2] for item in data]
        print (x,y,yerr)
        ax.errorbar(x,y,yerr, errorevery=(0,10), label=labels[idx])
        plt.xticks(rotation=45) 
        idx += 1
    
    #sns.despine(offset=1, trim=True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.savefig(filename+'.pdf', bbox_inches="tight", format='pdf')       

def get_times(doe_filename):
    time_list = []
    time_dict = {} 

    with open (doe_filename, 'rb') as f:
        data = pickle.load(f)
        for county, content in data['geographies'].items():
            if 'executions' in content.keys():
                for execution, exec_info in content['executions'].items():
                    time_list.append(exec_info['time_s'])
                    time_dict[county] = time_dict.get(county, []) + [exec_info['time_s']]
            else:
                time_dict[county] = [-1.0]

    return time_list, time_dict 

def write_csv(filename, variable_list):
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(variable_list)

if __name__ == '__main__':
    counties = [ 'BHJM']
    counter = {} 
    
    errors = []
    num_execs = 5 
    max_generations = 100 
    difference_counter = []

    #algorithms = ['NSGA-III (all vars)', 'Innovization (preferred)', 'Innovization (fixed)','Random (fixed)']
    algorithms = ['Control', 'Innovization (Static)','Random selection']
    injection = ['5', '5', '5', '5', '5', '5', '5', '5', '5', '5']
    csv_list = [['Configuration', 'Injection', 'County', 'HVR', 'Time (s)']]
    dir_base = ['cec2023-all-vars','innovization-multicounty', 'cec2023-fixed-7','cec2023-random-7']
    dir_base = ['cec2023-all-vars', 'cec2023-fixed-7','cec2023-random-7']

    times = []
    for idx, doe in enumerate(dir_base):
        time_doe, time_doe_dict = get_times(f'{doe}/doe.pck')
        times.append(time_doe_dict)
    hv_simple_statistics = [['Configuration', 'County', 'Best', 'Worst', 'AVG', 'STD']]     
    for county in counties:
        pf_path = f'pfs/pf_{county}.pck'
        hvr_list = []
        for idx, alg in enumerate(algorithms):
            print(pf_path)
            hvr_results = compute_hv(pf_path, '{}/{}/executions'.format(dir_base[idx], county), num_execs, max_generations)
            hvr_list.append(hvr_results)
        create_plot(f'plots2/{county}', hvr_list, algorithms, county)


