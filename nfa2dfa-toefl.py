#!/usr/bin/python
import sys
import time
from copy import deepcopy
from itertools import combinations

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


def get_reachable_states(state):
    global reachable_states,detected_states,nfa_machine
    detected_states.append(state)
    if('~' in nfa_machine["transfer_function"][state]):
        raw_states = nfa_machine["transfer_function"][state]['~']
        to_add = list(set(raw_states).difference(set(reachable_states)))
        reachable_states.extend(to_add)
        to_detect = list(set(raw_states).difference(set(detected_states)))
        print("To detect: " + str(to_detect))
        if(len(to_detect) > 0):
            update_reachable_states(to_detect)

def update_reachable_states(state_list):
    global reachable_states,detected_states
    for state in state_list:
        get_reachable_states(state)


def explore_individual (a_state, a_symbol):
    global nfa_machine
    if(a_symbol in nfa_machine["transfer_function"][a_state]):
        return nfa_machine["transfer_function"][a_state][a_symbol]
    else:
        return ''


def explore(states_to_explore):
    global new_states,to_explore,state_map,nfa_machine, new_dfa_machine, reachable_states, detected_states

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

        raw_list = []
        if (len(temp_states) == 0):
            result[a_symbol] = 'phi'
        else:
            for result_states in temp_states:
                raw_list.extend(result_states)
            raw_list = list(set(raw_list))
            reachable_states = deepcopy(raw_list)
            detected_states = []
            update_reachable_states(reachable_states)
            temp_list =  deepcopy(reachable_states)  #need to count in all the reach states for the result
            temp_list.sort()
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

def gen_new_states():
    global nfa_machine, new_dfa_machine
    new_dfa_machine["states"].append("phi")
    original_states = nfa_machine["states"]
    for i in range(1,len(original_states)+1):
        tuple_list = list(combinations(original_states,i))
        for t in tuple_list:
            t = list(t)
            t.sort()
            new_state = ''.join(t)
            new_dfa_machine["states"].append(new_state)
    
def check_accepting_states(states):
    global nfa_machine, new_dfa_machine
    ac = ''.join(states)
    for s in states:
        if (s in nfa_machine["accepting_states"] and (ac not in new_dfa_machine["accepting_states"])):
            new_dfa_machine["accepting_states"].append(ac)
            break

def add_trap_rule():
    global nfa_machine, new_dfa_machine
    new_dfa_machine["transfer_function"]['phi'] = {}
    for symbol in nfa_machine["alphabet"] :
        new_dfa_machine["transfer_function"]['phi'][symbol] = 'phi'
    
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
    "transfer_function" : {}
}

state_map = {}
reachable_states = []
detected_states = []
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
gen_new_states()
add_trap_rule()

while (len(to_explore)>0):
    element_to_explore = to_explore[0]
    print("The remain to explore is " + str(to_explore))
    to_explore.pop(0)
    reachable_states = deepcopy(state_map[element_to_explore])
    detected_states = []
    update_reachable_states(state_map[element_to_explore])
    reachable_states.sort()
    print("Reachable is " + str(reachable_states))
    if(len(new_dfa_machine["start_state"])==0):
        new_dfa_machine["start_state"] = ''.join(reachable_states)
    check_accepting_states(reachable_states)
    explore(reachable_states)

print(new_dfa_machine)

output_file_name = sys.argv[1].replace('.txt', '')+ "-DFA" +".csv"
output_file = open(output_file_name, "w")

try:  #read from the nfa definition and construct the machine, print the information at the same time
   output_file.write(new_dfa_machine["machine_name"] + "\n")
   output_file.write(",".join(new_dfa_machine["alphabet"])+ "\n")
   output_file.write(",".join(new_dfa_machine["states"])+ "\n")
   output_file.write(new_dfa_machine["start_state"]+ "\n")
   output_file.write(",".join(new_dfa_machine["accepting_states"])+ "\n")
   for key1 in new_dfa_machine["transfer_function"]:
    for key2 in new_dfa_machine["transfer_function"][key1]:
        output_file.write(key1 + "," + key2+ "," + new_dfa_machine["transfer_function"][key1][key2]+ "\n")

except:
    print "Cannot write to file"
finally:
    output_file.close()


