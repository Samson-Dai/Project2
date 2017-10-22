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

def do_test(line):
    global dfa_machine, current_state, accepting_states
    for i in range(0, len(line)):
        letter = line[i]
        init_state = current_state
        new_state = dfa_machine[current_state][letter][0]
        rule_num = dfa_machine[current_state][letter][1]
        print(str(i+1)+","+str(rule_num)+","+str(init_state)+","+str(letter)+","+str(new_state))
        current_state = new_state
    if current_state in accepting_states:
        print("Accepted")
    else:
        print("Rejected")

machine_name = ""
alphabet = []
states = []
start_state = ""
accepting_states = []
current_state =""
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
            for state in states:
                dfa_machine[state] = {}
            print("States: " + str(states))
        elif i == 3:
            start_state = line
            current_state = start_state
            print("Start state : " + start_state)
        elif i ==4:
            accepting_states = line.split(',')
            print("Accepting state : " + str(accepting_states))
        else:
            print("Rule "+ str(i-4) +" : "+ line)
            read_rules(line, i-4)

    for line in test:
        line = line.rstrip()
        print("String : " + line)
        do_test(line)

except:
    print "Cannot read the file"
finally:
    fa.close()
    test.close()
