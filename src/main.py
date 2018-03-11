import random
import string
import time
import sys

import wordtrie

###
# random_word
#
# Generates a random word of random length (1-8).
def random_word():
    l = random.randrange(1, 8)
    c = []
    for x in range(l):
        c.append(random.choice(string.ascii_lowercase))
    return ''.join(c)

def main(args):
    trie = wordtrie.WordTrie()

    s = time.clock()
    n = 0
    for x in range(1000000):
        w = random_word()
        if trie.has_word(w):
            n += 1
    print('Stop: {}, words: {}'.format(time.clock() - s, n))

if __name__ == '__main__':
    main(sys.argv)
