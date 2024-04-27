from aalpy import generate_random_dfa
from aalpy.learning_algs import run_RPNI
from aalpy.utils import FileHandler
from gen_data import gen_words
from examples import load_data_from_file
from aalpy.utils.ModelChecking import compare_automata
from aalpy.utils.ModelChecking import bisimilar
import matplotlib.pyplot as plt
import nfa


def to_tuple_list(l, label):
    return [(tuple(w), label) for w in l]

def to_string(t):
    s = ''
    for v in t :
        s += v
    return s

def load_automata_java(fic):
    return FileHandler.load_automaton_from_file(fic, automaton_type='dfa')

def compare_aalpy_learnlib(data_file, file_java):
    p,m = load_data_from_file('data.txt')
    model_rpni =  run_RPNI(p+m, automaton_type='dfa', print_info=False)
    auto_java = load_automata_java('dot-java.txt')

    p, m = gen_words(1, 5, 1000, 1000, 3)
    n1 = 0
    n2 = 0
    t = 0
    for w in p : 
        try : 
            res1 = model_rpni.compute_output_seq(model_rpni.initial_state, w)
            n1 += 1 if res1[-1] else 0 
            res2 = auto_java.compute_output_seq(auto_java.initial_state, w)
            n2 += 1 if res2[-1] else 0
            if res1[-1] != res2[-1]:
                t += 1
        except Exception:
            continue

    print("l'automate aalpy : ", n1 / len(p))
    print("l'automate learnlib : ", n2 / len(p))
    print("taux d'erreur ",t/len(p))

def compare_aalpy_with_random(taille, np, nm, nstate):
    #generating a random automata
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    alpha = alphabet[:taille]
    random_dfa = generate_random_dfa(alphabet=alpha, num_states=nstate, num_accepting_states=nstate//2+1)
    

    # generating a word from the alphabet used to generate the random_dfa and doing rpni on that data
    p, m = gen_words(1,10,np,0,len(alpha))
    
    # vérifier que si w appartient à p => w appartient à L(alph)
    # vérifier que si w appartient à n => w n'appartient pas à L(alph)

    p1 = []
    m1 = []
    for w in p :
        try:
            res = random_dfa.compute_output_seq(random_dfa.initial_state, w)
            if res[-1] : 
                p1.append(w)
            else:
                m1.append(w)
        except:
            continue

    p1 = to_tuple_list(p1, True)
    m1 = to_tuple_list(m1, False)

    # apprentissage d'un automate avec l'échentillon p1, m1
    model_rpni = run_RPNI(p1 + m1, automaton_type='dfa', print_info=False)
    
    # on teste la qualité de l'automate model_rpni
    # pour cela on génére un seconde échantillon 
    p, m = gen_words(1,5, np, nm, len(alpha))
    p1 = []
    m1 = []
    for w in p :
        try:
            res = random_dfa.compute_output_seq(random_dfa.initial_state, w)
            if res[-1] : 
                p1.append(w)
            else:
                m1.append(w)
        except:
            continue
         
    n = 0
    l = p1 + m1
    for w in l : 
        try : 
            res1 = random_dfa.compute_output_seq(random_dfa.initial_state, w) 
            res2 = model_rpni.compute_output_seq(model_rpni.initial_state, w)

            if ((not res1[-1]) and res2[-1]) or (res1[-1] and (not res2[-1])):
                n += 1
        except Exception:
            continue

#    print("Taux d'error du rpni ", n / len(l))
    return n / len(l)

def compare_RPNI_NFA(taille, np, nm):

    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    alpha = alphabet[:taille]
    p, m = gen_words(1,5, np, nm, len(alpha))

    p1 = to_tuple_list(p, True)
    m1 = to_tuple_list(m, False)

    model_rpni = run_RPNI(p1 + m1, automaton_type='dfa', print_info=False)

    _, all_states = nfa.MCA(p)
    auto_genetic = nfa.bundle(nfa.algo_genetic(p, m, 50, 10), all_states)
    

    p, m = gen_words(1,5, np, nm, len(alpha))
         
    n = 0
    l = p + m

    for w in l : 
        try : 
            res1 = auto_genetic.is_accept(w)
            res2 = model_rpni.compute_output_seq(model_rpni.initial_state, w)

            if ((not res1) and res2[-1]) or (res1 and (not res2[-1])):
                n += 1
        except Exception:
            continue

    return n / len(l)


if __name__ == '__main__':
    print(compare_RPNI_NFA(3,20, 20))
    # somme = 0
    # var = 15
    # x = range(2,var)
    # y = []
    # for j in x:
    #    somme = 0
    #    for i in range(5):
    #         somme += compare_RPNI_NFA(3,20, 10,j)
    #    print(j," ",somme/100)
    #    y.append(somme/100)

    # ymax = []
    # ymin = []
    # for i in range(var-2):
    #     ymax.append(max(y[i:]))
    #     ymin.append(min(y[i:]))

    # fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1)
    # ax.set_ylabel("Taux erreur")
    # ax.set_xlabel("nombre d'états")
    # ax.set_title("Evolution moyenne des comparaisons")
       

    # ax.plot(x,y, label='curve')
    # ax.plot(x, ymin, color='tab:red', label='inf curve')
    # ax.plot(x, ymax, color='tab:green', label='sup curve')
    # ax.legend()
    # plt.show()


    # np = ['aa', 'aba', 'bbbb', 'ca', 'cccb']
    # nm = ['b', 'bba', 'cc', 'a']
