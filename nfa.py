class state:
    def __init__(self, state_id, is_accepting):
        self.state_id = state_id
        self.accepting = is_accepting

    def set_transitions(self, t):
        self.transition = t

    def get_transitions_states(self, t):
        for a,b in self.transition.items():
            if a == t :
                return b
        return None

class nfa():
    def __init__(self, initial_state):
        self.initial_state = initial_state

    def is_accept(self, s, states = None, tab = set()):
        if s == None:
            return states
        if states == None:
            tab = self.initial_state.get_transitions_states(s[0])
        else:
            for st in states:
                for state in st.get_transitions_states(s[0]):
                    tab.add(state)
        if tab == None:
            return None
        if len(s) == 1:
            return self.is_accept(None, tab)
        return self.is_accept(s[1:], tab)
    

s1 = state(1, False)
s2 = state(2, True)
s3 = state(3, True)

s1.set_transitions({'a':{s2, s3}})
#print(s1.get_transitions_states('a'))
a = nfa(s1)

print(a.is_accept('a'))
