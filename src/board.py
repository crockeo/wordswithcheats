
###
# Board
#
# A class representing a WWF board.
class Board(object):
    size = 11

    def __init__(self, state={}):
        self.state = state

    def __str__(self):
        rs = []
        for row in range(self.size):
            r = []
            for col in range(self.size):
                r.append(
                    self.state[(row, col)] if (row, col) in self.state else '-'
                )
            rs.append(' '.join(r))
        return '\n'.join(rs)

    ###
    # __peers
    #
    # Returns the peers of a tile location.
    def __peers(self, tile):
        (x, y) = tile

        ps = []
        if x > 0:
            ps.append((x - 1, y))
        if x < (self.size - 1):
            ps.append((x + 1, y))
        if y > 0:
            ps.append((x, y - 1))
        if y < (self.size - 1):
            ps.append((x, y + 1))
        return ps

    ###
    # __word_edges_helper
    #
    # A helper function for word_edges that recurs on each tile.
    def __word_edges_helper(self, tile, seen, edges):
        seen.add(tile)
        peers = self.__peers(tile)
        for peer in peers:
            if peer in self.state:
                if peer not in seen:
                    self.__word_edges_helper(peer, seen, edges)
            else:
                edges.add(peer)
        return edges

    ###
    # word_edges
    #
    # Finds the set of locations that are on the edge of an existing word.
    def word_edges(self):
        for k in self.state:
            src = k
        return self.__word_edges_helper(src, set(), set())

    ###
    # edge_direction
    #
    # Finds the direction(s) that this location will have to concern itself.
    #
    # Note, the '!= E' sections are from testing wherein I would set edges to
    # words on the puzzle to 'E' for easier testing.
    def edge_direction(self, edge):
        (x, y) = edge

        dirs = set()
        if (x - 1, y) in self.state and self.state[(x - 1, y)] != 'E':
            dirs.add('U')
        if (x + 1, y) in self.state and self.state[(x + 1, y)] != 'E':
            dirs.add('D')
        if (x, y - 1) in self.state and self.state[(x, y - 1)] != 'E':
            dirs.add('L')
        if (x, y + 1) in self.state and self.state[(x, y + 1)] != 'E':
            dirs.add('R')

        return dirs

    ###
    # __dir_fn
    #
    # Converts a direction letter into a direction function.
    def __dir_fn(self, d):
        if d == 'U':
            return lambda x: (x[0] - 1, x[1])
        if d == 'D':
            return lambda x: (x[0] + 1, x[1])
        if d == 'L':
            return lambda x: (x[0], x[1] - 1)
        if d == 'R':
            return lambda x: (x[0], x[1] + 1)
        pass

    ###
    # __edge_words_helper
    def __edge_words_helper(self, edge, d):
        dfn = self.__dir_fn(d)
        pos = dfn(edge)
        s = ''
        while pos in self.state:
            if d == 'U' or d == 'L':
                s = self.state[pos] + s
            else:
                s = s + self.state[pos]
            pos = dfn(pos)
        return s

    ###
    # edge_words
    #
    # Gets the text(s) associated with an edge location.
    def edge_words(self, edge):
        ds = self.edge_direction(edge)
        ts = {}
        for d in ds:
            ts[d] = self.__edge_words_helper(edge, d)

        if 'L' in ts and 'R' in ts:
            ts['X'] = ts['L'] + '-' + ts['R']
            del ts['L']
            del ts['R']
        elif 'L' in ts:
            ts['X'] = ts['L'] + '-'
            del ts['L']
        elif 'R' in ts:
            ts['X'] = '-' + ts['R']
            del ts['R']

        if 'U' in ts and 'D' in ts:
            ts['Y'] = ts['U'] + '-' + ts['D']
            del ts['U']
            del ts['D']
        elif 'U' in ts:
            ts['Y'] = ts['U'] + '-'
            del ts['U']
        elif 'D' in ts:
            ts['Y'] = '-' + ts['D']
            del ts['D']

        return ts

###
# test_str
#
# Tests the __str__ functionality of the Board.
def test_str():
    bs = [
        Board(),
        Board({ (0, 0): 'a' })
    ]

    ss = [
        ('- - - - - - - - - - -\n' +
         '- - - - - - - - - - -\n' +
         '- - - - - - - - - - -\n' +
         '- - - - - - - - - - -\n' +
         '- - - - - - - - - - -\n' +
         '- - - - - - - - - - -\n' +
         '- - - - - - - - - - -\n' +
         '- - - - - - - - - - -\n' +
         '- - - - - - - - - - -\n' +
         '- - - - - - - - - - -\n' +
         '- - - - - - - - - - -'),

        ('a - - - - - - - - - -\n' +
         '- - - - - - - - - - -\n' +
         '- - - - - - - - - - -\n' +
         '- - - - - - - - - - -\n' +
         '- - - - - - - - - - -\n' +
         '- - - - - - - - - - -\n' +
         '- - - - - - - - - - -\n' +
         '- - - - - - - - - - -\n' +
         '- - - - - - - - - - -\n' +
         '- - - - - - - - - - -\n' +
         '- - - - - - - - - - -'),
    ]

    for x in range(len(bs)):
        if str(bs[x]) != ss[x]:
            return False
    return True

###
# test_word_edges
#
# Tests that the word edges function finds the correct edges for a word.
def test_word_edges():
    b = Board({
        (5, 4): 's',
        (5, 5): 'e',
        (5, 6): 'x'
    })

    return b.word_edges() == set([
        (4, 4),
        (4, 5),
        (4, 6),
        (5, 3),
        (5, 7),
        (6, 4),
        (6, 5),
        (6, 6)
    ])

###
# test_edge_direction
#
# Tests that edge_direction returns a lambda (or a set of lambdas) that
# transform edges in the right direction.
def test_edge_direction():
    b = Board({
        (3, 6): 'l',
        (4, 6): 'a',
        (5, 4): 's',
        (5, 5): 'e',
        (5, 6): 'x'
    })

    return b.edge_direction((4, 5)) == set(['D', 'R'])

###
# test_edge_words
#
# Tests that edge_words returns the correct strings.
def test_edge_words():
    b = Board({
        (3, 6): 'l',
        (4, 6): 'a',
        (4, 7): 'r',
        (4, 8): 't',
        (5, 4): 's',
        (5, 5): 'e',
        (5, 6): 'x'
    })

    return b.edge_words((4, 5)) == {
        'X': '-art',
        'Y': '-e'
    }

###
# main
#
# Entry-point for this module. Runs unit tests on the functionality of Board.
def main():
    tests = [
        ('test_str', test_str),
        ('test_word_edges', test_word_edges),
        ('test_edge_direction', test_edge_direction),
        ('test_edge_words', test_edge_words)
    ]

    for (name, test) in tests:
        if not test():
            print('{} failed!'.format(name))

    b = Board({
        (3, 6): 'l',
        (4, 6): 'a',
        (4, 7): 'r',
        (4, 8): 't',
        (5, 4): 's',
        (5, 5): 'e',
        (5, 6): 'x'
    })

    for edge in b.word_edges():
        print('{} => {}'.format(edge, b.edge_words(edge)))
    for edge in b.word_edges():
        b.state[edge] = 'E'
    print(b)

if __name__ == '__main__':
    main()
