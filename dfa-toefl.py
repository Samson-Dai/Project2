#!/usr/bin/python
import sys
import time
from copy import deepcopy

def read_fa(line):
    global promb_counter, problem_list, problem_info
    if (line[0] == 'c'):
        line_list = line.split()
        problem_info = {}
        problem_info["clauses"] = []  # init clauses
        problem_info["total_num_li"] = 0
        problem_list.append(problem_info)  # append a new problem in the list
        problem_info["promb_num"] = line_list[1]
        problem_info["max_num_literal"] = line_list[2]
        problem_info["test_char"] = line_list[3]
        promb_counter += 1
    elif (line[0] == "p"):
        line_list = line.split()
        problem_info["var_num"] = line_list[2]
        problem_info["clause_num"] = line_list[3]
    else:
        line_list = line.split(',')
        problem_info["total_num_li"] += len(line_list) - 1
        a_clause = []
        for item in line_list[0: len(line_list) - 1]:
            a_clause.append(item)
        problem_info["clauses"].append(a_clause)

machine_name = ""
alphabet = []
states = []
start_state = ""
accepting_states = []



fa_file = sys.argv[1]
test_file = sys.argv[2]
fa = open(fa_file, "r")


try:
    for i, line in enumerate(fa):
        line = line.rstrip()
        if i == 0:
            if ":" in line:
                colon = line.index(':')
                machine_name = line[:colon]
                print ("Machine name: " + machine_name)
            else:
                machine_name = line
                print ("Machine name: " + machine_name)

        elif i == 1:
            alphabet = line.split(',')
            print("Alphabet: " + str(alphabet))
        elif i ==2:
            states = line.split(',')
            print("States: " + str(states))
        elif i == 3:
            start_state = line
            print("Start state : " + start_state)
        elif i ==4:
            accepting_states = line.split(',')
            print("Accepting state : " + str(accepting_states))
        else:
            print("Rule "+ str(i-4) +" : "+ line)
except:
    print "Cannot read the file"
finally:
    fa.close()
