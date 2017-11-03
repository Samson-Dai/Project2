#!/usr/bin/python
import sys
import time
from copy import deepcopy

def read_rules(line):
    global nfa_machine
    rules = nfa_machine["transfer_function"]
    line_list = line.split(',')
    init_state = line_list[0]
    input_symbol = line_list[1]
    new_state = line_list[2]
    if (input_symbol not in rules[init_state]):
        rules[init_state][input_symbol]= []
    rules[init_state][input_symbol].append(new_state)


def explore_individual (a_state, a_symbol):
    global nfa_machine
    if(a_symbol in nfa_machine["transfer_function"][a_state]):
        return nfa_machine["transfer_function"][a_state][a_symbol]
    else:
        return ''


def explore(states_to_explore):
    global new_states,to_explore,state_map,nfa_machine, new_dfa_machine
    print("Currently explore " + str(states_to_explore))

    state_str = ''.join(states_to_explore)
    if (state_str not in new_states):
        new_states.append(state_str)
        to_explore.append(state_str)
        state_map[state_str] = states_to_explore

    result = {}
    for a_symbol in nfa_machine["alphabet"]:
        result[a_symbol] = ""
        temp_states = []
        for a_state in states_to_explore:
            a_result = explore_individual (a_state, a_symbol)
            print ("For "+ str(a_state) + " and input " + str(a_symbol) +" we get " + str(a_result))
            if (a_result != '' and (a_result not in temp_states)):
                temp_states.append(a_result)  #a_result can be a list

        temp_list = []
        if (len(temp_states) == 0):
            result[a_symbol] = 'phi'
        else:
            for result_states in temp_states:
                temp_list.extend(result_states)
            result[a_symbol] = ''.join(temp_list)
        print(temp_list)

        if (state_str not in  new_dfa_machine["transfer_function"]): # add it to the rule
            new_dfa_machine["transfer_function"][state_str] = {}
        new_dfa_machine["transfer_function"][state_str][a_symbol] = result[a_symbol]

        if (result[a_symbol] not in new_states):
            new_states.append(result[a_symbol])
            to_explore.append(result[a_symbol])
            state_map[result[a_symbol]] = temp_list
            print("We have a new state when explore: " + str(temp_list))



    
nfa_machine = {
    "machine_name" : "",
    "alphabet" : [],
    "states" : [],
    "start_state" : "",
    "accepting_states" : [],
    "rejected_states" : [],
    "current_state" : "",
    "transfer_function" : {}
}

new_dfa_machine = {
    "machine_name" : "",
    "alphabet" : [],
    "states" : [],  # by definition is the power set
    "start_state" : "",
    "accepting_states" : [],
    "rejected_states" : [],
    "current_state" : "",
    "transfer_function" : {}
}

state_map = {}

fa_file = sys.argv[1]
fa = open(fa_file, "r")

try:  #read from the nfa definition and construct the machine, print the information at the same time
    for i, line in enumerate(fa):
        line = line.rstrip()
        if i == 0:
            if ":" in line:
                colon = line.index(':')
                machine_name = line[:colon]
                nfa_machine["machine_name"] = machine_name
                print ("Machine name: " + machine_name)
            else:
                machine_name = line
                nfa_machine["machine_name"] = machine_name
                print ("Machine name: " + machine_name)

        elif i == 1:
            alphabet = line.split(',')
            nfa_machine["alphabet"] = alphabet
            print("Alphabet: " + str(alphabet))
        elif i ==2:
            states = line.split(',')
            nfa_machine["states"] = states
            for state in states:
                nfa_machine["transfer_function"][state] = {}
                state_map[state] = [state]
            print("States: " + str(states))
        elif i == 3:
            start_state = line
            nfa_machine["start_state"] = start_state
            print("Start state : " + start_state)
        elif i ==4:
            accepting_states = line.split(',')
            rejected_states = list(set(states).difference(set(accepting_states)))
            nfa_machine["accepting_states"] = accepting_states
            nfa_machine["rejected_states"] = rejected_states
            print("Accepting states : " + str(accepting_states))
        else:
            print("Rule "+ str(i-4) +" : "+ line)
            read_rules(line)
except:
    print "Cannot read the file"
finally:
    fa.close()

to_explore = deepcopy(nfa_machine["states"])
new_states = deepcopy(to_explore)
new_states.append('phi')


new_dfa_machine["machine_name"] = nfa_machine["machine_name"] + " to DFA"
new_dfa_machine["alphabet"] = nfa_machine["alphabet"]
"""new_dfa_machine = {
    "machine_name" : "",
    "alphabet" : [],
    "states" : [],
    "start_state" : "",
    "accepting_states" : [],
    "rejected_states" : [],
    "current_state" : "",
    "transfer_function" : {}
}"""


while (len(to_explore)>0):
    element_to_explore = to_explore[0]
    print("The remain to explore is " + str(to_explore))
    to_explore.pop(0)
    explore(state_map[element_to_explore])

print(new_dfa_machine)
    

def get_new_start_state():
    pass

