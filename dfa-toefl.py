#!/usr/bin/python
import sys
import time
from copy import deepcopy

def read_rules(line, rule_num):
    global dfa_machine
    line_list = line.split(',')
    init_state = line_list[0]
    input_symbol = line_list[1]
    new_state = line_list[2]
    dfa_machine[init_state][input_symbol]= [new_state,rule_num]


machine_name = ""
alphabet = []
states = []
start_state = ""
accepting_states = []
dfa_machine = {}


fa_file = sys.argv[1]
test_file = sys.argv[2]
fa = open(fa_file, "r")
test = open(test_file, "r")

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

            read_rules(line, i-4)

    print(dfa_machine)

    for line in test:
        print line

except:
    print "Cannot read the file"
finally:
    fa.close()
