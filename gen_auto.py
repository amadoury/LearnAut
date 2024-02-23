from aalpy import generate_random_dfa
from aalpy.learning_algs import run_RPNI


random_dfa = generate_random_dfa(alphabet=['a','b','c'], num_states=5, num_accepting_states=2)



#random_dfa.execute_sequence()
#random_dfa.visualize()

var = random_dfa.to_state_setup()

var = list(var.values())
print(var)

# model = run_RPNI(list(var.values()), automaton_type='dfa')

# model.visualize()

#print(var)