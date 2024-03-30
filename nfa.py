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

    def __str__(self):
        return str(self.state_id)

    def set_transitions(self, t):
        self.transition = t
    
    def add_transition(self, t):
        self.transition.update(t)

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
     


def MCA(positif_words):
    n = 0
    state_initial = state(n, False)
    n += 1
    tab = []

    for word in positif_words:
        acc = False
        if(len(word) == 1):
            state_initial_word = state(n, True)
            n += 1
            
            s = state_initial.get_transitions_states(word[0])
            if(s == None):
                state_initial.add_transition({word[0] : {state_initial_word}})
            else:
                s.add(state_initial_word)

            continue

        state_initial_word = state(n, False)
        n += 1
        st = state_initial_word

        for c in word[1:len(word)-1]:
            st_next = state(n, False)
            n += 1
            st.set_transitions({c : {st_next}})
            st = st_next

        st_next = state(n, True)
        n += 1
        st.set_transitions({word[-1] : {st_next}})
        
        s = state_initial.get_transitions_states(word[0])
        if(s == None):
            state_initial.add_transition({word[0] : {state_initial_word}})
        else:
            s.add(state_initial_word)
    return nfa(state_initial, None)

def print_auto_state(state, space = ""):
    print(space,end="")
    for a,b in state.transition.items():
        for s in b:
            print(a,s,end="\n")
            print_auto_state(s, space + "   ")
    print("")

def print_auto(automata):
    print(automata.initial_state)
    print_auto_state(automata.initial_state)



def partition(lst, min_size=1, max_size=None):
    if max_size is None:
        max_size = len(lst)
    
    partitions = []
    
    while lst:
        size = random.randint(min_size, min(max_size, len(lst)))
        partition = random.sample(lst, size)
        partitions.append(partition)
        lst = [x for x in lst if x not in partition]
    
    return partitions

def string_from_partition(partition):
    tab =  []
    for m, part in enumerate(partition):
        for i in part:
            tab.append((m + 1, i))
    tab = sorted(tab, key=lambda x: x[1])
    s = ""
    for m, i in tab:
        s += str(m)
    return s

def mutation():
    pass

def crossover():
    pass


s1 = state(1, False)
s2 = state(2, False)
s3 = state(3, False)
s4 = state(4, False)
s5 = state(5, True)
s1.set_transitions({'a':{s1, s2}, 'b':{s1}})
s2.set_transitions({'a':{s3}, 'b':{s3}})
s3.set_transitions({'a':{s4}, 'b':{s4}})
s4.set_transitions({'a':{s5}, 'b':{s5}})

 
auto = MCA(["aab", "ba", "aaa", "b"])

# print_auto(auto)

# states = auto.is_accept('aab')
# print(states)
# states = auto.is_accept('aaa')
# print(states)
# states = auto.is_accept('ba')
# print(states)
# states = auto.is_accept('b')
# print(states)
# states = auto.is_accept('a')
# print(states)

# states = a.is_accept('abbbb')
# print(states)


print(string_from_partition([[1, 2, 6], [3, 7, 9, 10], [4, 8, 12], [5], [11]]))