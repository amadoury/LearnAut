import random

def gen_words(min_len, max_len, len_plus,len_minus, len_alph):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    if (len_alph <= 0 or len_alph > 26):
        raise Exception
    alp = alphabet[:len_alph]

    len_alp = len(alp)

    plus_word = []
    minus_word = []

    for _ in range(len_plus):
        rand = random.randint(min_len, max_len)
        word = ''
        for _ in range(rand):
            word += alp[random.randint(0,len_alp - 1)]
        if not (word in plus_word):
            plus_word.append(word)

    for _ in range(len_minus):
        rand = random.randint(min_len, max_len)
        word = ''
        for _ in range(rand):
            word += alp[random.randint(0,len_alp - 1)]
        if not (word in minus_word) and not (word in plus_word):
            minus_word.append(word)

    #assert(len(minus_word) != 0)
    return plus_word, minus_word



def write_to_file(plus, minus):
    with open('data.txt', 'w') as file :
        eol = '\n'
        len_plus = len(plus)
        len_minus = len(minus)
        for i in range(len_plus):
            file.write(plus[i] + '\n')
        file.write('-\n')
        for i in range(len_minus):
            if i == len_minus - 1:
                file.write(minus[i])
            else:
                file.write(minus[i]+'\n')

if __name__ == '__main__':
    #min_len, max_len, len_plus,len_minus, len_alph
    p, m = gen_words(1, 5, 1000, 1000, 3)
    write_to_file(p, m)