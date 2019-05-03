"""
Obfuscate text Module
"""

from __future__ import print_function

N =8
sign_plus = '+'
sign_minus = '-'
sign_line = '|'
sign_point = '.'
sign_space = ' '


class Queens:

    def __init__(self, n=N, str=''):
        self.n = n
        self.str = str
        self.length = len(str)
        self.results = ''
        self.reset()

    def reset(self):
        n = self.n
        self.y = [None] * n             # Where is the queen in column x
        self.row = [0] * n              # Is row[y] safe?
        self.up = [0] * (2*n-1)         # Is upward diagonal[x-y] safe?
        self.down = [0] * (2*n-1)       # Is downward diagonal[x+y] safe?
        self.nfound = 0                 # Instrumentation

    def solve(self, x=0):               # Recursive solver
        results = ''
        for y in range(self.n):
            if self.safe(x, y):
                self.place(x, y)
                if x+1 == self.n:
                    results = results + self.add_block()
                else:
                    results = results + self.solve(x+1)
                self.remove(x, y)
        if x == 0:
            self.results = results
        return results

    def safe(self, x, y):
        return not self.row[y] and not self.up[x-y] and not self.down[x+y]

    def place(self, x, y):
        self.y[x] = y
        self.row[y] = 1
        self.up[x-y] = 1
        self.down[x+y] = 1

    def remove(self, x, y):
        self.y[x] = None
        self.row[y] = 0
        self.up[x-y] = 0
        self.down[x+y] = 0
    
    def get_char(self, pos):
        if pos < self.length:
            return self.str[pos]
        else:
            return sign_space

    silent = 0                          # If true, count solutions only
    position = 0                        # the index of the string

    def add_block(self):
        position = self.position
        results = ''
        self.nfound = self.nfound + 1
        if self.silent:
            return
        results = results + (sign_plus + sign_minus + sign_minus * 2 * self.n + sign_plus) + '\n'
        for y in range(self.n-1, -1, -1):
            results = results + sign_line + sign_space
            # results = results + (sign_line, end=sign_space)
            for x in range(self.n):
                if self.y[x] == y:
                    results = results + self.get_char(position) + sign_space
                    # results = results + (self.get_char(position), end=sign_space)
                    position = position + 1
                    self.position = position
                else:
                    results = results + sign_point + sign_space
                    # results = results + (sign_point, end=sign_space)
            results = results + sign_line + '\n'
        results = results + (sign_plus + sign_minus + sign_minus * 2 * self.n + sign_plus) + '\n'
        return results
    
    def display(self):
        print(self.results)

def obfuscate(n, str):
    import sys
    silent = 0
    if sys.argv[1:2] == ['-n']:
        silent = 1
        del sys.argv[1]
    if sys.argv[1:]:
        n = int(sys.argv[1])
    q = Queens(n, str)
    q.silent = silent
    q.solve()
    q.display()
    print(q.nfound)

