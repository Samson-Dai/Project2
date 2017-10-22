#!/usr/bin/python
import sys
import time
from copy import deepcopy

def read_rules(line, rule_num):
    global alphabet, states, dfa_machine
    line_list = line.split(',')
    init_state = line_list[0]
    input_symbol = line_list[1]
    new_state = line_list[2]
    dfa_machine[init_state]



    

machine_name = ""
alphabet = []
states = []
start_state = ""
accepting_states = []
dfa_machine={}

fa_file = sys.argv[1]
test_file = sys.argv[2]
fa = open(fa_file, "r")


try:
    for i, line in enumerate(fa):
        line = line.rstrip()
        if i == 0:
            machine_name = line
            print ("Machine Name : " + machine_name);
        elif i == 1:
            alphabet = line.split(',')
            print("Alphabet: " + str(alphabet))
        elif i ==2:
            states = line.split(',')
            for state in states:
                dfa_machine[state] = {}
            print("States: " + str(states))
        elif i == 3:
            start_state = line
            print("Start state : " + start_state)
        elif i ==4:
            accepting_states = line.split(',')
            print("Accepting state : " + str(accepting_states))
        else:
            print("Rule "+ str(i-4) +" : "+ line)
            read_rules(line, i-4)
except:
    print "Cannot read the file"
finally:
    fa.close()
