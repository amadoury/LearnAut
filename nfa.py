import random
from itertools import islice

def batched_docs(iterable, n):
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch

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
    def __str__(self):
        return str(self.state_id)

class nfa():
    def __init__(self, initial_state, list_states):
        self.initial_state = initial_state
        self.list_states = list_states
 
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
    
    def partition(self):
        nb_part = random.randint(2, len(self.list_states))
        # l = []
        # for i in range(0, len(self.list_states) // nb_part):
        #     l.append(self.list_states[i :: nb_part])

        # return l
        return batched_docs(self.list_states, nb_part)



s1 = state(1, False)
s2 = state(2, False)
s3 = state(3, False)
s4 = state(4, False)
s5 = state(5, True)
s1.set_transitions({'a':{s1, s2}, 'b':{s1}})
s2.set_transitions({'a':{s3}, 'b':{s3}})
s3.set_transitions({'a':{s4}, 'b':{s4}})
s4.set_transitions({'a':{s5}, 'b':{s5}})


a = nfa(s1, [s1, s2, s3, s4, s5])
print(list(a.partition()))

# states = a.is_accept('abbbb')
# print(states)

