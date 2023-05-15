#!/usr/bin/env python3

'''
Log parser script for HTTP logs in HoneyEVSE project
authors: Bianchi Tommaso, Turrin Federico
'''

import pandas as pd
import argparse
import os 
import json
import matplotlib.pyplot as plt
import seaborn as sns

argParser = argparse.ArgumentParser()
argParser.add_argument("-f", "--file", help="path of log file to parse")

# file name argument 
args = argParser.parse_args()
filename = args.file

# check if the file exists, otherwise exit the program
try:
    if not os.path.isfile(filename):
        print(f'[!] FILE \"{filename}\" NOT FOUND!')
        exit()
except:
    print("File not provided! Call -h for help")
    exit()

# PARSER METHODS
# find the type of log
def find_log_type(log_string):
    if "Time" in log_string:
        return "Time"
    elif "Button" in log_string:
        return "Action"
    elif ("GET" in log_string) or ("POST" in log_string) or ("HEAD" in log_string):
        return "Request"
    return "No specific type"

# parse time type log
def time_parser(log):
    date = log[0]
    hour = log[1]
    page = log[10]
    ip = log[12]
    time = log[13]
    return [date, hour, page, ip, time]

# parse request type log
def request_parser(log):
    ip = log[5]
    date = log[8][1:]
    hour = log[9][:-1]
    request_type = log[10][1:]
    page = log[11]
    request_action = log[12]
    request_code = log[13]
    return [ip, date, hour, request_type, page, request_action, request_code]

# parse action button type log
def action_parser(log):
    date = log[0]
    hour = log[1]
    button = log[5]
    ip = log[10]
    return [date, hour, button, ip]

def nested_dict_to_list(dict):
    final_list = []
    for key, value in dict.items():
        l = [key]
        for v in value:
            l.append(v)
        final_list.append(l)
    return final_list

# "MAIN"
# counters for the different actions
time_counters = {      
        }

request_counters = {
}

action_counters = {
}
    
# list of all ips in logs --> check them in Grey Noise
ip_list = []

# open the file and start parse it
with open(filename, 'r') as f:
    for line in f.readlines():
        # parse line with different fields and use it a json
        log = find_log_type(line) 
        log_line = line.strip().split(" ") # remove line terminator and split the fields

        if log == "Time":
            time_parse = time_parser(log_line)
            # result = [date, hour, page, ip, time_on_page]
            # handle results
            page = time_parse[2]
            time_on_page = float(time_parse[4])

            # add to the dict if not present
            if page not in time_counters.keys():
                time_counters[page] = [time_on_page, 1]
            else:
                time_counters[page][0] = time_counters[page][0] + time_on_page
                time_counters[page][1] += 1 # counter for the specific page action 
            
            # update ip list
            #if time_parse[3] not in ip_list:
            ip_list.append(time_parse[3].replace(":", ""))
            
        elif log == "Request":
            request_parse = request_parser(log_line)
            # result = [ip, date, hour, request_type, page, request_action, request_code]
            # handle results
            request_type = request_parse[3]

            # add to the dict if not present
            if request_type not in request_counters.keys():
                request_counters[request_type] = 1
            else:
                request_counters[request_type] += 1

            #if request_parse[0] not in ip_list:
            ip_list.append(request_parse[0].replace(":", ""))
            
        elif log == "Action":
            action_parse = action_parser(log_line)
            # result = [date, hour, button, ip]
            # handle results
            button = action_parse[2]

            # add to the dict if not present
            if button not in action_counters.keys():
                action_counters[button] = 1
            else:
                action_counters[button] += 1

            #if action_parse[3] not in ip_list:
            ip_list.append(action_parse[3].replace(":", ""))

    
    time_df = pd.DataFrame(nested_dict_to_list(time_counters), columns=["page", "time", "counter"])
    request_df = pd.DataFrame(list(request_counters.items()), columns=["request", "counter"])
    action_df = pd.DataFrame(list(action_counters.items()), columns=["action", "counter"])

    #### statistics for time on page
    print("######## TIME STATISTICS ########")
    print("Total time spent on pages:", time_df['time'].sum())
    print("Time spent on each page:")
    for page in time_df['page']:
        print("\tPage", page, ":", float(time_df.loc[time_df['page'] == page]['time']), ", in percentage:", 100*float(time_df.loc[time_df['page'] == page]['time'])/time_df['time'].sum())

    #### statistics for requests
    print("\n######## REQUEST STATISTICS ########")
    print("Total requests:", request_df['counter'].sum())
    print("Requests for each type:")
    for request in request_df['request']:
        print("\tRequest type", request, ":", int(request_df.loc[request_df['request'] == request]['counter']), ", in percentage:", 100*int(request_df.loc[request_df['request'] == request]['counter'])/request_df['counter'].sum())
    

    #### statistics for action
    print("\n######## REQUEST STATISTICS ########")
    print("Total button press:", action_df['counter'].sum())
    print("For for each button:")
    for button in action_df['action']:
        print("\tButton pressed", button, ":", int(action_df.loc[action_df['action'] == button]['counter']), ", in percentage:", 100*int(action_df.loc[action_df['action'] == button]['counter'])/action_df['counter'].sum())


# save unique ip address in file
with open('repeated-ips-greynoise.txt', mode='wt', encoding='utf-8') as myfile:
    for ip in ip_list:
        myfile.write(f'\n{ip}')

# compute IP statistic from here
unique_ip_list = list(set(ip_list))

with open('unique-ips.txt', mode='wt', encoding='utf-8') as myfile:
    for ip in unique_ip_list:
        myfile.write(f'\n{ip}')

time_tot = time_df['time'].sum()
request_tot = request_df['counter'].sum()
action_tot = action_df['counter'].sum()

# PLOTS
# Apply the default theme

sns.set_theme()
# sns.set(rc = {'figure.figsize':(18,18)})
# plt.figure(figsize=(12,12))

# plt.rcParams['font.family'] = 'serif'
# plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']

time_plot = sns.barplot(data=time_df, x="page", y="time")
time_plot.set(xlabel='Page', ylabel='Time Spent (s)')
# time_plot.set_ylabel("Time Spent (s)", fontsize=20)
# time_plot.tick_params(labelsize=18, rotation=0)
plt.savefig('time_results_http.pdf', bbox_inches='tight')
# plt.show()

request_plot = sns.barplot(data=request_df,x="request", y="counter")
time_plot.set(xlabel='Request Type', ylabel='Number of Requests')
# request_plot.set_xlabel("Request Type", fontsize=20)
# request_plot.set_ylabel("Number of Requests", fontsize=20)
# request_plot.tick_params(labelsize=18, rotation=0)
plt.savefig('request_results_http.pdf', bbox_inches='tight')
# # plt.show()



