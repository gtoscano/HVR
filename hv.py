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

import matplotlib.pyplot as plt
sns.set_style("whitegrid", {'grid.linewidth': .3})

def compute_pf(objs):
    objs = numpy.asarray(objs)
    objs_len = len(objs)
    cnstrs = numpy.zeros((objs_len,1))
    fronts, ranks = nds(objs, cnstrs, compare_min)
    pf = objs[fronts[0]] 
    return pf.tolist()
                
def compute_max_min(path):
    cost = []
    load = []
    idx = []
    fx = []
    print(path)
    for i in range(0,100):
        cost_output_file = '{}/{}_output_t.csv'.format(path, i)
        load_output_file = '{}/{}_reportloads.csv'.format(path, i)
        file_exists = os.path.exists(cost_output_file)
        if file_exists:
            csvFile = pandas.read_csv(cost_output_file)
            total_cost = csvFile['Cost'].sum()
            cost.append(total_cost)
            loadFile = pandas.read_csv(load_output_file)
            total_load = loadFile['NLoadEos'].sum()
            load.append(total_load)
            idx.append(i)
            fx.append([total_cost, total_load])
    
    cost_min = min(cost)
    cost_max = max(cost)
    load_min = min(load)
    load_max = max(load)
    return {'fx':fx, 'cost':[cost_min, cost_max], 'load':[load_min, load_max]}

def normalize_fronts(pf_path, path, max_exec_idx):
    with open (pf_path, 'rb') as f:
        data = pickle.load(f)
        bound_cost = data['cost']
        bound_load = data['load']
        pf = data['pf']

    executions = {}

    for idx in range(max_exec_idx):
        executions[idx] = compute_max_min('{}/{}/results/'.format(path, idx))
    range_cost = bound_cost[1]-bound_cost[0]
    range_load = bound_load[1]-bound_load[0]

    all_fx = []
    normalized_pf = []
    for point in pf:
        normalized_pf.append([(point[0]-bound_cost[0])/range_cost, (point[1] - bound_load[0])/range_load])

    for idx, execution  in executions.items():
        new_fx = []
        for fx in execution['fx']:
            new_fx.append([(fx[0]- bound_cost[0])/range_cost, (fx[1]- bound_load[0])/range_load])
        all_fx += new_fx

        with open('{}/{}/results/normalized_front.out'.format(path, idx), 'w') as f:
            f.write('#\n')
            writer = csv.writer(f, delimiter=' ')
            writer.writerows(new_fx)
            f.write('#\n')


    with open('{}/all_fronts.out'.format(path), 'w') as f:
        f.write('#\n')
        writer = csv.writer(f, delimiter=' ')
        writer.writerows(all_fx)
        f.write('#\n')

    with open('{}/normalized_pareto_front.out'.format(path), 'w') as f:
        f.write('#\n')
        writer = csv.writer(f, delimiter=' ')
        writer.writerows(normalized_pf)
        f.write('#\n')

    return executions
    
def compute_hv(pf_path, path, max_exec_idx):
    executions = normalize_fronts(pf_path, path, max_exec_idx)
    hv = {}
    hvr = {}
    hv_list = []
    hv_tmp = []
    b_hv_pf = subprocess.check_output(['./exec_hv', '{}/normalized_pareto_front.out'.format(path)])
    hv_pf = float(b_hv_pf)
    for idx, execution  in executions.items():
        b_hv = subprocess.check_output(['./exec_hv', '{}/{}/results/normalized_front.out'.format(path, idx)])
        hv[idx] = float(b_hv)
        hvr[idx] = float(b_hv)/hv_pf
        hv_list.append(float(b_hv)/hv_pf)
        hv_tmp.append(float(b_hv)/hv_pf)
    median_idx = numpy.argsort(hv_tmp)[len(hv_tmp)//2]
    return hv_list

def call_hv(pf_path, path, num_execs):

    hv_list, median = compute_hv(pf_path, path, num_execs) 
    hva = numpy.asarray(hv_list)
    best = numpy.max(hva[:,1])
    worst = numpy.min(hva[:,1])
    avg = numpy.mean(hva[:,1])
    std = numpy.std(hva[:,1])
    return numpy.asarray(hv_list)


    '''
    print(f'{best}')
    print(f'{worst}')
    print(f'{avg}')
    print(f'{std}')
    print(f'best/worst/avg/std')

    print('Median: {}\n'.format(median))

    print(hv_list)
    
    with open('{}/hv.out'.format(path), 'w') as f:
        f.write('Median: {}\n'.format(median))
        f.write('Best: {}\n'.format(best))
        f.write('Worst: {}\n'.format(worst))
        f.write('Avg: {}\n'.format(avg))
        f.write('STD: {}\n'.format(std))
        writer = csv.writer(f)
        writer.writerows(hv_list)
    '''
def create_plot(filename, values, labels, county):
    fig = plt.figure("hv_gen")
    ax = fig.add_subplot(111)
    ax.cla()
    ax.set_xlabel(county)
    ax.set_ylabel("HVR")
    plt.suptitle('Ratio of the Hypervolume')
    ax.boxplot(values, labels=labels) 
    plt.xticks(rotation=45) 
    #sns.despine(offset=1, trim=True)
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
    counties = [ 'Berkeley', 'Grant', 'Hampshire', 'Hardy', 'Jefferson', 'Mineral', 'Monroe', 'Morgan', 'Pendleton', 'Preston', 'Tucker']
    counties = [ 'Berkeley', 'Mineral',  'Hardy', 'Jefferson']
    counties = [ 'Grant',  'Morgan', 'Pendleton', 'Preston']
    counties = [ 'GMPP',  'BMHJ']
    counties = [ 'BHJM']
    counties = [ 'Berkeley', 'Mineral',  'Hardy', 'Jefferson']
    counter = {} 
    
    errors = []
    num_execs = 11 
    num_execs = 5 
    difference_counter = []
    idx = ['1', '99/1', '95/5', '50/50']
    idx = ['All vars','Static Innovization', 'Dynamic Innovization']
    idx = ['innovization-strategy-1-5','innovization-strategy-1-10','innovization-strategy-2-5','innovization-strategy-2-10','innovization-strategy-3-5','innovization-strategy-3-10','innovization-strategy-4-5','innovization-strategy-4-10']
    algorithms = ['Eps-cnstr', 'NSGA-III+99m+1c', 'NSGA-III+95m+5c', 'NSGA-III+50m+50c']
    algorithms = ['50/50', '95/5', '1']
    algorithms = ['Original', 'Static Innovization', 'Dynamic Innovization']
    algorithms = ['Original', 'Static', 'Dynamic', 'Preferred']
    algorithms = ['Control', 'Preferred']
    algorithms = ['NSGA-III (all vars)', 'S1-5BMPs','S1-10BMPs','S2-5BMPs','S2-10BMPs','S3-5BMPs','S3-10BMPs','S4-5BMPs','S4-10BMPs']
    algorithms = ['NSGA-III (all vars)', 'Strategy 1','Strategy 2','Strategy 3','Strategy 4']
    injection = ['20', '20', '20', '20']
    injection = ['5', '5', '5', '5', '5', '5', '5', '5', '5', '5']
    csv_list = [['Algorithm', 'Injection', 'County', 'HVR', 'Time (s)']]
    dir_base = [f'1_cc_20_eps', f'99_math_1_cc_20_eps', f'95_math_5_cc_20_eps-finished', '50_math_50_cc_20_eps-tmp']
    dir_base = ['50_math_50_cc_5_eps-finished','95_math_5_cc_5_eps', '1_cc_5_eps']
    dir_base = ['95_math_5_cc_5_eps', 'innovization-all-11', 'innovization-dynamic-99.9', 'innovization-preferred-bmps']
    dir_base = ['95_math_5_cc_20_eps-finished', 'innovization-testing']
    dir_base = ['control-all-vars', 'innovization-testing']
    dir_base = ['control-all-vars', 'innovization-multicounty']
    dir_base = ['95_math_5_cc_5_eps', 'innovization-strategy-1-5','innovization-strategy-1-10','innovization-strategy-2-5','innovization-strategy-2-10','innovization-strategy-3-5','innovization-strategy-3-10','innovization-strategy-4-5','innovization-strategy-4-10']
    dir_base = ['95_math_5_cc_5_eps', 'innovization-strategy-1-10','innovization-strategy-2-10', 'innovization-strategy-3-10','innovization-strategy-4-10']

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
            hvr_results = compute_hv(pf_path, '{}/{}/executions'.format(dir_base[idx], county), num_execs)

            hva = numpy.asarray(hvr_results)
            best = numpy.max(hva)
            worst = numpy.min(hva)
            avg = numpy.mean(hva)
            std = numpy.std(hva)
            hv_simple_statistics.append([alg,county,best,worst, avg, std])

            
            hvr_list.append(hvr_results)
            for run_idx, hvr in enumerate(hvr_results):
                run_time = times[idx][county][run_idx]
                print(alg, idx, county)
                csv_list.append([alg, injection[idx], county, hvr, run_time])

        create_plot(f'plots2/{county}', hvr_list, algorithms, county)
    write_csv('make_plots.csv', csv_list)
    for  row_idx in range(len(hv_simple_statistics[0])):
        row = ''
        for  col_idx in range(len(hv_simple_statistics)):
            row += '{},'.format(hv_simple_statistics[col_idx][row_idx])
        row = row[:-1] + '\n'
        print (row)



    print(hv_simple_statistics)


