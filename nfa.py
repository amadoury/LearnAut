import random

class State:
    def __init__(self, state_id, is_accepting, initial_state=False):
        self.state_id = state_id
        self.accepting = is_accepting
        self.transition = {}
        self.initial_state = initial_state

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

    def set_accepting(self, is_accepting):
        self.accepting = is_accepting
    

class Nfa():
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


def MCA(positif_words):
    n = 0
    state_initial = State(n, False, initial_state=True)
    n += 1
    tab = []
    all_states = [state_initial]

    for word in positif_words:
        acc = False
        if(len(word) == 1):
            state_initial_word = State(n, True)
            all_states.append(state_initial_word)
            n += 1
            
            s = state_initial.get_transitions_states(word[0])
            if(s == None):
                state_initial.add_transition({word[0] : {state_initial_word}})
            else:
                s.add(state_initial_word)

            continue

        state_initial_word = State(n, False)
        all_states.append(state_initial_word)
        n += 1
        st = state_initial_word

        for c in word[1:len(word)-1]:
            st_next = State(n, False)
            all_states.append(st_next)
            n += 1
            st.set_transitions({c : {st_next}})
            st = st_next

        st_next = State(n, True)
        all_states.append(st_next)
        n += 1
        st.set_transitions({word[-1] : {st_next}})
        
        s = state_initial.get_transitions_states(word[0])
        if(s == None):
            state_initial.add_transition({word[0] : {state_initial_word}})
        else:
            s.add(state_initial_word)
    return Nfa(state_initial),all_states

def print_auto_state(state, space = "", states_searched = []):
    print(space,end="")
    if state not in states_searched:
        states_searched.append(state)
    else:
        return
    for a,b in state.transition.items():
        for s in b:
            print(a,end="\n")
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
            tab.append((m, i))
    tab = sorted(tab, key=lambda x: x[1])
    s = []
    for m, i in tab:
        s.append(m)
    return s

def mutation(partition):
    place = random.randint(0, len(partition) - 1)
    mu = random.randint(0, len(partition) - 1)
    partition = partition[:place] + [mu] + partition[place+1:]
    return partition

def crossover(partition_1, partition_2):
    len_1 = len(partition_1)
    len_2 = len(partition_2)

    return (partition_1[:len_1 // 3] + partition_2[len_2 // 3:]
            , partition_2[:len_2 // 3] + partition_1[len_1 // 3:])

def partition_from_string(s):
    part = []
    for j, m in enumerate(s) :
        part.append((j,m))
    
    part = sorted(part, key=lambda x: x[1])
    partition = []
    i = 0
    while i < len(part) : 
        l = [a for (a, b) in part if b == part[i][1]]
        partition.append(l)
        i += len(l)
    return partition

def part_initial_state(partition):
    for i, part in enumerate(partition):
        for state in part : 
            if state.initial_state :
                return i
    return None

def part_contains_accepting(part):
    for state in part :
        if state.accepting :
            return True
    return False


def which_part(state, all):
    for i,st in enumerate(all) :
        if state in st.state_id : 
            return i
    return None

def nfa_from_partition(partition, all_states):
    j = part_initial_state(partition)
    assert(j != None)
    accept = part_contains_accepting(partition[j])
    initial_state = State(partition[j],accept,initial_state=True)

    all = [initial_state]

    for i, part in enumerate(partition):
        if i != j :
            accept = part_contains_accepting(part)
            all.append(State(part, accept))
    
    for state in all_states:
        for k, v in state.transition.items() : 
            for st in v :
                p = which_part(st, all)
                if p != None : 
                    q = which_part(state, all)
                    if q != None:
                        s = all[q].get_transitions_states(k)
                        if s != None :
                            s.add(all[p])
                        else : 
                            all[q].add_transition({k:{all[p]}})
    return Nfa(initial_state)

def number_to_states(partitions, all_states):
    l = []
    for p in partitions:
        m = []
        for s in p:
            #[v] = [a for a in all_states if a.state_id == s]

            it = filter(lambda x: (x.state_id == s) ,all_states)
            # if len(list(it)) == 1:
            [v] = list(it)
            m.append(v)
        l.append(m)
    return l

def fitness_function(p, all_states, m, plus):

    p = partition_from_string(p)
    ps = number_to_states(p, all_states)
    nfa = nfa_from_partition(ps, all_states)


    err = 0

    for s in plus : 
        if not nfa.is_accept(s):
            err += 1

    for s in m : 
        if nfa.is_accept(s):
            err += 1
    return 100*err + len(p)


def initial_gen(len_gen, list_states, m, plus):
    l = []
    for _ in range(len_gen):
        p = partition(list(range(len(list_states))))
        st = string_from_partition(p)
        print(st)
        l.append((st, fitness_function(st, list_states, m, plus)))
    l = sorted(l, key=lambda x: x[1])
    return l

def next_gen(prev_gen, list_states, states_minus , states_plus, cent_mut=5, cent_copy=5):
    len_mut = (cent_mut * len(prev_gen)) // 100
    len_copy = (cent_copy * len(prev_gen)) // 100
    len_cross = ((100 - cent_copy - cent_mut) * len(prev_gen)) // 100
    if(len_cross % 2 != 0):
        len_cross -= 1
        len_copy += 1
    
    len_cross //= 2
    
    #
    # t = sum(n for _, n in prev_gen)
    # a = []
    # for _, j in prev_gen:
    #     a.append(1 - j / t)

    a = [(10 ** i) for i in range(len(prev_gen))]
    a.reverse()
    #print("weights : ", a)
    #copy
    l = prev_gen[:len_copy] 
    
    #mutation
    for _ in range(len_mut):
        [(c, _)] = random.choices(prev_gen, weights=a)
        p = mutation(c)
        l.append((p, fitness_function(p, list_states, states_minus, states_plus)))

    #crossover 
    for _ in range(len_cross):

        [(c1, _)] = random.choices(prev_gen, weights=a)
        [(c2, _)] = random.choices(prev_gen, weights=a)

        b,c = crossover(c1, c2)

        fb = fitness_function(b, list_states, states_minus, states_plus)
        fc = fitness_function(c, list_states, states_minus, states_plus)

        l.append((b, fb)) 
        l.append((c, fc))
        l = sorted(l, key=lambda x: x[1])
    return l

def best_avg_fitness(g):
    _, bf = g[0]
    avgf = sum(n for _, n in g) / len(g)
    return g, bf, avgf

def algo_genetic(p, m, taille_gen, nb_gen):
    nfa, all_states = MCA(p)

    init_gen = initial_gen(taille_gen, all_states, m, p)
    all = [best_avg_fitness(init_gen)]
    print("first gen best fitness :", all[0][1])
    prev_gen = init_gen
    for _ in range(nb_gen):
        n_gen = next_gen(prev_gen, all_states, m, p)
        all.append(best_avg_fitness(n_gen))
        prev_gen = n_gen

    #all = sorted(all, key=lambda x: x[1])
    return all

def bundle(res_algo_genetic, all_states):

    p = partition_from_string(res_algo_genetic[len(res_algo_genetic)-1][0][0][0])

    ps = number_to_states(p,all_states)

    return nfa_from_partition(ps,all_states)


if __name__ == '__main__':

    a = algo_genetic(['aa', 'aba', 'bbbb', 'ca', 'cccb'], ['b', 'bba', 'cc', 'a', 'abb', 'c', 'acc', 'bbb', 'b'], 20, 100)

    n, all_states = MCA(['aa', 'aba', 'bbbb', 'ca', 'cccb'])
    # print(mca.is_accept('b'))
    # print(mca.is_accept('aba'))

    # print(a[len(a)-1][1])

    # print(n.is_accept('b'))
    # print(n.is_accept('bba'))
    # print(n.is_accept('cc'))
    # print(n.is_accept('a'))

    # print(n.is_accept('aa'))
    # print(n.is_accept('aba'))
    # print(n.is_accept('bbbb'))
    # print(n.is_accept('ca'))
    # print(n.is_accept('cccb'))


    print("-----------------------------------")

    p = partition_from_string(a[len(a)-1][0][0][0])

    ps = number_to_states(p,all_states)

    n = nfa_from_partition(ps,all_states)
 
    #print_auto(n)

    for i in range(len(a)):
        print(a[i][1], "---", a[i][2])

    # print()
    # print_auto(n)

    # print(n.is_accept('b'))
    # print(n.is_accept('bba'))
    # print(n.is_accept('cc'))
    # print(n.is_accept('a'))

    # print(n.is_accept('aa'))
    # print(n.is_accept('aba'))
    # print(n.is_accept('bbbb'))
    # print(n.is_accept('ca'))
    # print(n.is_accept('cccb'))


    # s1 = State(1, False, initial_state=True)
    # s2 = State(2, False)
    # s3 = State(3, False)
    # s4 = State(4, False)
    # s5 = State(5, True)

    # s1.set_transitions({'a':{s1, s2}, 'b':{s1}})
    # s2.set_transitions({'a':{s3}, 'b':{s3}})
    # s3.set_transitions({'a':{s4}, 'b':{s4}})
    # s4.set_transitions({'a':{s5}, 'b':{s5}})

    # a = Nfa(s1)

    # #print_auto(a)

    # auto, auto_states = MCA(["aab", "ba", "aaa", "b"])
    # # print(m)


    # st1 = State(1, False, initial_state=True)
    # st2 = State(2, False)
    # st3 = State(3, False)
    # st4 = State(4, True)

    # st1.set_transitions({'a':{st2}, 'b' : {st4}})
    # st2.set_transitions({'a':{st3}})

    # au = Nfa(st1)

    # print(au.is_accept("a"))

    # aut = nfa_from_partition([[st1, st2], [st3], [st4]], [st1, st2, st3, st4])
    # print_auto(aut)

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


    # p1 = string_from_partition([[1, 2, 6, 7], [3, 9, 10], [4, 5, 8, 11, 12]])
    # p2 = string_from_partition([[1, 3], [2, 7, 9, 10], [4, 8, 12], [5, 6], [11]])
    # print(p1)
    # s = partition_from_string(p1)
    # print(s)

    # # print(p1,p2)
    # # p1,p2 = crossover(p1,p2)
    # # print(p1,p2)

    # p1 = mutation(p1)
    # print(p1)

    # p = string_from_partition([[0, 1, 2, 6, 7], [3, 9], [4, 5, 8]])

    # automata_merged = partition_to_automata(p, auto_states)
    # print_auto(automata_merged)

