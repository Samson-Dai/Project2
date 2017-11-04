#!/usr/bin/python
import sys
from copy import deepcopy

#this function reads rules and rule number to state what each rule does.
def read_rules(line, rule_num):
    global dfa_machine#we have to save each rule in dfa machine therefore take in global dfa_machine variable
    line_list = line.split(',')
    init_state = line_list[0]#first is the initial state
    input_symbol = line_list[1]#input symbol to determine which state to go to
    new_state = line_list[2]#new state after take in the symbol
    dfa_machine[init_state][input_symbol]= [new_state,rule_num]#finally, save this rule to a dfa_machine with a new_state and rule_num

def do_test(line):
    global dfa_machine, current_state, accepting_states,start_state, alphabet, rejected_states

    current_state = start_state  # set current state to the start state which means start from the initial state.
    for i in range(0, len(line)):
        letter = line[i]
        init_state = current_state

        if (letter not in alphabet):#if input symbols are not in alphabet then prints invalid error
            print("Invalid Input")
            current_state = rejected_states[0]#this is done because this state should not be an accepting state and therefore we mark it as a rejected state so that it does not print out accepted despite if the state is the accepted state.
            break;


        if (letter not in dfa_machine[current_state]):#if there is not input symbol, letter, then it prints out current state does not have the input symbol to proceed.
            print("No rule for state " + str(current_state) + " with input "+ str(letter))
            current_state = rejected_states[0]##this is done because this state should not be an accepting state and therefore we mark it as a rejected state so that it does not print out accepted despite if the state is the accepted state.
            break;
        
        #after checking each of different symbols with states, we finally proceed with our logic
        new_state = dfa_machine[current_state][letter][0]#save the new state with current input argument: current_state and input symbol
        rule_num = dfa_machine[current_state][letter][1]#save the rule number with current input argument: current state and input symbol
        print(str(i+1)+","+str(rule_num)+","+str(init_state)+","+str(letter)+","+str(new_state))
        current_state = new_state #update current state

    if current_state in accepting_states:#check if the current state is the accepting state
        print("Accepted\n")
    else:#if not, print rejected
        print("Rejected\n")
    

#different varibles(easily recognizable by their names, and nothing tricky)
machine_name = ""
alphabet = []
states = []
start_state = ""
accepting_states = []
rejected_states = []
current_state =""
dfa_machine = {}

#taking the file argument which is the rules for the machine.
fa_file = sys.argv[1]
#testing bunch of inputs for the machine
test_file = sys.argv[2]
fa = open(fa_file, "r")#opening the rule file
test = open(test_file, "r")#opening the test file

try:  #read from the DFA definition and construct the machine, print the information at the same time
    for i, line in enumerate(fa):
        line = line.rstrip()
        if i == 0:
            if ":" in line:#distinguishes the first line and parse the machine name
                colon = line.index(':')
                machine_name = line[:colon]
                print ("Machine name: " + machine_name)
            else:
                machine_name = line
                print ("Machine name: " + machine_name)

        elif i == 1:#take the input symbols and save it into alphabet
            alphabet = line.split(',')
            print("Alphabet: " + str(alphabet))
        elif i ==2:#defines the states
            states = line.split(',')
            for state in states:#here, we save different states into dfa_machine[state]
                dfa_machine[state] = {}
            print("States: " + str(states))
        elif i == 3:#define the start state
            start_state = line
            print("Start state : " + start_state)
        elif i ==4:#define the accepting state and call other states as rejected states
            accepting_states = line.split(',')
            rejected_states = list(set(states).difference(set(accepting_states)))
            print("Accepting states : " + str(accepting_states))
            print("Rejected states: " + str(rejected_states))
        else:#these are different cases of rules and we read the rule in function called, "read_rules"
            print("Rule "+ str(i-4) +" : "+ line)
            read_rules(line, i-4)

    for line in test: #read from the test file and do the test
        line = line.rstrip()
        print("String : " + line)
        do_test(line)

except:
    print "Cannot read the file"
finally:
    fa.close()#finally close the fa which is opened the rule file
    test.close()#close the test file
