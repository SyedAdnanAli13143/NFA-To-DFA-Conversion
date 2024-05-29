class NFA:
   def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

def epsilon_closure(states, transitions):
    epsilon_closure_set = set(states)
    stack = list(states)
    while stack:
        current_state = stack.pop()
        if current_state in transitions and 'ε' in transitions[current_state]:
            epsilon_transitions = set(transitions[current_state]['ε']) - epsilon_closure_set
            epsilon_closure_set.update(epsilon_transitions)
            stack.extend(epsilon_transitions)
    return epsilon_closure_set

def move(states, symbol, transitions):
    result_states = set()
    for state in states:
        if state in transitions and symbol in transitions[state]:
            result_states.update(transitions[state][symbol])
    return epsilon_closure(result_states, transitions)

def nfa_to_dfa(nfa):
    dfa_states = set()
    dfa_transitions = {}
    dfa_start_state = epsilon_closure({nfa.start_state}, nfa.transitions)
    dfa_states.add(tuple(dfa_start_state))
    stack = [tuple(dfa_start_state)]

    while stack:
        current_dfa_state = stack.pop()
        for symbol in nfa.alphabet:
            next_nfa_states = set()
            for nfa_state in current_dfa_state:
                next_nfa_states.update(move({nfa_state}, symbol, nfa.transitions))
            next_dfa_state = tuple(epsilon_closure(next_nfa_states, nfa.transitions))
            if next_dfa_state not in dfa_states:
                dfa_states.add(next_dfa_state)
                stack.append(next_dfa_state)
            dfa_transitions[current_dfa_state, symbol] = next_dfa_state

    dfa_accept_states = {state for state in dfa_states if any(s in nfa.accept_states for s in state)}

    return DFA(dfa_states, nfa.alphabet, dfa_transitions, dfa_start_state, dfa_accept_states)

class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

def get_user_input():
    states = input("Enter NFA states (comma-separated): ").split(',')
    alphabet = input("Enter alphabet symbols (comma-separated): ").split(',')
    transitions = {}
    for state in states:
        transitions[state] = {}
        for symbol in alphabet + ['ε']:
            transition_input = input(f"Enter NFA transition for state {state} and symbol {symbol} (comma-separated, enter 'none' if no transition): ")
            if transition_input.lower() != 'none':
                transitions[state][symbol] = set(transition_input.split(','))

    start_state = input("Enter NFA start state: ")
    accept_states = input("Enter NFA accept states (comma-separated): ").split(',')

    return NFA(set(states), set(alphabet), transitions, start_state, set(accept_states))

def main():
    nfa = get_user_input()
    dfa = nfa_to_dfa(nfa)

    print("\nDFA States:", dfa.states)
    print("DFA Transitions:", dfa.transitions)
    print("DFA Start State:", dfa.start_state)
    print("DFA Accept States:", dfa.accept_states)

if __name__ == "__main__":
    main()
