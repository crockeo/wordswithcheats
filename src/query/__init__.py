import string

__char_values = {
    'a': 1,
    'b': 4,
    ' ': 0,
    'c': 4,
    'd': 2,
    'e': 1,
    'f': 4,
    'g': 3,
    'h': 3,
    'i': 1,
    'j': 10,
    'k': 5,
    'l': 2,
    'm': 4,
    'n': 2,
    'o': 1,
    'p': 4,
    'q': 10,
    'r': 1,
    's': 1,
    't': 1,
    'u': 2,
    'v': 5,
    'w': 4,
    'x': 8,
    'y': 3,
    'z': 10
}

###
# __value
#
# Values a scrabble character.
def __value(c):
    val = 0
    x = 0
    while x < len(c):
        if c[x] == '(':
            val += __char_values[c[x + 1]]
            x += 2
        else:
            val += __char_values[c[x]]

        x += 1
    return val

###
# __rem
#
# Removes a value from a set, and returns the set without that value.
def __rem(s, c):
    sc = s.copy()
    sc[c] -= 1
    if sc[c] <= 0:
        del sc[c]
    return sc

###
# __search
#
# Given a trie, search through for words that use a set of letters.
def __search(node, s, bl, word='', li=0, debug=False):
    # Trie Traversal, one of:
    #  0. Base case; s={}, bl=[]
    #  1. Use a letter in the set.
    #  2. Use all of the letters from [bl] in series.
    words = []

    if debug:
        print(' ' * li, end='')
        print(s, bl, word)

    # Base Case
    if len(bl) == 0 and node.end:
        words.append(word)

    # Option 1.
    for c in s:
        if c == ' ':
            for x in string.ascii_lowercase:
                if x in node.children:
                    words.extend(
                        __search(
                            node.children[x],
                            __rem(s, ' '),
                            bl,
                            word + '({0})'.format(x),
                            li + 1,
                            debug
                        )
                    )
        elif c in node.children:
            words.extend(
                __search(
                    node.children[c],
                    __rem(s, c),
                    bl,
                    word + c,
                    li + 1,
                    debug
                )
            )

    # Option 2.
    if len(bl) > 0:
        rn = node
        eb = False
        for c in bl:
            if c in rn.children:
                rn = rn.children[c]
            else:
                eb = True
                break

        if not eb:
            words.extend(
                __search(
                    rn,
                    s,
                    '',
                    word + ''.join(bl),
                    li + 1,
                    debug
                )
            )

    return words

###
# start
#
# Starts the query mode given a trie.
def start(trie):
    print('Enter letter set. Include a \';\' followed by any letters you want to\ouse from the board.')
    print('Use a space for a blank character.')

    while True:
        i = input('> ')
        if i == 'quit':
            break

        try:
            [l,r] = i.split(';')
        except:
            continue

        s = {}
        for c in l:
            if c not in s:
                s[c] = 0
            s[c] += 1

        words = [(__value(x), x) for x in __search(trie.root, s, r)]
        words.sort()
        for (value, word) in words:
            print('{0}: {1}'.format(value, word))
