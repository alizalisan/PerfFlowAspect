import os
import numpy as np
import csv
import json
from statistics import mean

# move to the directory with data
# os.chdir("/ams_with_pfa_data")

func_name = '"IdealGas::Eval"'
usage = '{"cpu_usage": 0.0, "memory_usage": 0}'
usage_full = '{"cpu_usage":'

with open('ams_data_physics_NULL.csv', mode='w') as csv_file:
    fieldnames = ['Run no.', 'numElements', 'threshold', 'physicsComplexity', 'Dur1', 'Max_Dur1', 'Min_Dur1', 'Mem_usage1',
    'CPU_usage1', 'Dur2', 'Max_Dur2', 'Min_Dur2', 'Mem_usage2', 'CPU_usage2', 'Dur3', 'Max_Dur3', 'Min_Dur3', 'Mem_usage3', 
    'CPU_usage3', 'Dur4', 'Max_Dur4', 'Min_Dur4', 'Mem_usage4', 'CPU_usage4']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    run_no = 1

    for i in range(1, 10):
        numElements = 10000 * i
        for th in np.arange(0.0, 1.01, 0.1):
            th = round(th, 2)
            for ph in range(1, 10):
                physics_complexity = ph * 10

                os.chdir("nE"+str(numElements)+"_th"+str(th)+"_phyC"+str(physics_complexity))
                my_list = []
                for filename in os.listdir(os.getcwd()):
                    mem_list = []
                    cpu_list = []
                    dur_list = []
                    with open(os.path.join(os.getcwd(), filename), 'r') as f:
                        for line in f:
                            if func_name in line and usage not in line:
                                if usage_full in line:
                                    line = line[:-4]
                                    mem_list.append(float(((line.split(", "))[-1]).split(": ")[-1])) #memory usage
                                    cpu_list.append(float((((line.split(", "))[-2]).split("{")[-1]).split(": ")[-1])) #cpu usage
                                else:
                                    line = line[:-3]
                                    dur_list.append(float(((line.split(", "))[-1]).split(": ")[-1])) #duration
                    if (len(dur_list)):
                        my_list.append(mean(dur_list))
                        my_list.append(max(dur_list))
                        my_list.append(min(dur_list))
                        my_list.append(mean(mem_list))
                        my_list.append(mean(cpu_list))
                    else:
                        my_list.append("NULL")
                        my_list.append("NULL")
                        my_list.append("NULL")
                        my_list.append("NULL")
                        my_list.append("NULL")
               
                writer.writerow({'Run no.': run_no, 'numElements': numElements, 'threshold': th, 
                'physicsComplexity': physics_complexity, 'Dur1': my_list[0], 'Max_Dur1': my_list[1], 'Min_Dur1': my_list[2], 
                'Mem_usage1': my_list[3], 'CPU_usage1':my_list[4], 'Dur2': my_list[5], 'Max_Dur2': my_list[6], 
                'Min_Dur2': my_list[7], 'Mem_usage2': my_list[8], 'CPU_usage2': my_list[9], 'Dur3': my_list[10], 
                'Max_Dur3': my_list[11], 'Min_Dur3': my_list[12], 'Mem_usage3': my_list[13], 'CPU_usage3': my_list[14], 
                'Dur4': my_list[15], 'Max_Dur4': my_list[16], 'Min_Dur4': my_list[17], 'Mem_usage4': my_list[18], 
                'CPU_usage4': my_list[19]})
                f.close()
                os.chdir('..')
                run_no = run_no + 1