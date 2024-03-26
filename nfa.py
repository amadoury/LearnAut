class state:
    def __init__(self, state_id, is_accepting):
        self.state_id = state_id
        self.accepting = is_accepting
        self.transition = {}

    def set_transitions(self, t):
        self.transition = t

    def get_transitions_states(self, c):
        for a,b in self.transition.items():
            if a == c :
                return b
        return None

class nfa():
    def __init__(self, initial_state):
        self.initial_state = initial_state
        
    def is_accept(self, s):
        prev = {self.initial_state}
        states = set()
        for i in range(len(s)) :
            for st in prev:
                if(st.get_transitions_states(s[i]) != None):
                    for state in st.get_transitions_states(s[i]):
                        states.add(state)
            prev = states
            if i != len(s) - 1 : 
                states = set()

        for st in states:
            if st.accepting == True:
                return True
        return False

s1 = state(1, False)
s2 = state(2, False)
s3 = state(3, False)
s4 = state(4, False)
s5 = state(5, True)

s1.set_transitions({'a':{s1, s2}, 'b':{s1}})
s2.set_transitions({'a':{s3}, 'b':{s3}})
s3.set_transitions({'a':{s4}, 'b':{s4}})
s4.set_transitions({'a':{s5}, 'b':{s5}})

a = nfa(s1)

states = a.is_accept('abbbb')
print(states)

