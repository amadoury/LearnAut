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
    (('a','a'), True),
    (('a','b'), True),
    (('b'), False)]

if __name__ == '__main__' :
    plus = []
    minus = []
    flag = True
    with open("/home/amadou/Desktop/learnAut/automata/data.txt") as file :
        for line in file : 
            if (line.rstrip() == '-') : 
                flag = False
            else : 
                if (flag) : 
                    plus.append((tuple(line.rstrip()), flag))
                else : 
                    minus.append((tuple(line.rstrip()), flag))
    data = plus + minus
    print(data)
    rpni_example(data)