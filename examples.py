from aalpy.learning_algs import run_RPNI
from aalpy.utils import ModelChecking
from aalpy.utils import FileHandler
from gen_data import gen_words
from gen_data import write_to_file
import time
import matplotlib.pyplot as plt


def rpni_example(data):
    model = run_RPNI(data, automaton_type='dfa',algorithm='classic')
    #FileHandler.save_automaton_to_file(model, path="LearnedModel-py",file_type="dot")
    #auto = FileHandler.load_automaton_from_file('dotfile',automaton_type='dfa')
    #auto.visualize()
    model.visualize()

def load_data_from_file(file):
    plus = []
    minus = []
    flag = True
    with open(file) as file :
        for line in file : 
            if (line.rstrip() == '-') : 
                flag = False
            else : 
                if (flag) : 
                    plus.append((tuple(line.rstrip()), flag))
                else : 
                    minus.append((tuple(line.rstrip()), flag))
    data = plus + minus
    return data

def multiple_test(start, end, step):
    list_time = []
    list_len = []
    for i in range(start, end, step):
        p, m = gen_words(1, 10, i, i, 4)
        write_to_file(p, m)
        data = load_data_from_file('data.txt')
        start = time.time()
        model = run_RPNI(data, automaton_type='dfa', print_info=False)
        end = time.time()
        list_time.append(round(end - start, 3))
        list_len.append(i)
    
    plt.plot(list_len, list_time)
    plt.ylabel('time')
    plt.xlabel('len word')
    plt.show()

data1 = [
    (('a','a'), True),
    (('a','b'), True),
    (('b'), False)]

if __name__ == '__main__' :
    data = load_data_from_file('data.txt')
    #rpni_example(data)

    n = 100

    automata_java = FileHandler.load_automaton_from_file('fic.txt',automaton_type='dfa')
    automata_py = run_RPNI(data, automaton_type='dfa',algorithm='classic')

    ModelChecking.compare_automata(automata_py, automata_java, n)

    
