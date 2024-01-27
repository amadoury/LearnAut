from aalpy.learning_algs import run_RPNI

def rpni_example(data):
    model = run_RPNI(data, automaton_type='dfa')
    model.visualize()


data1 = [(('a', 'a', 'a'), True),
        (('a', 'a', 'b', 'a'), True),
        (('b', 'b', 'a'), True),
        (('b', 'b', 'a', 'b', 'a'), True),
        (('a',), False),
        (('b', 'b'), False),
        (('a', 'a', 'b'), False),
        (('a', 'b', 'a'), False)]

data2 = [
    (('a', 'b', 'a'), True),
    (('b'), False)]

rpni_example(data2)