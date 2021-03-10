#
# Complete the 'checkDivisibility' function below.
#
# The function is expected to return a STRING_ARRAY.
# The function accepts STRING_ARRAY arr as parameter.
#

from itertools import permutations
import pdb

def checkDivisibility(arr):
    # Write your code here
    ints = [int(k) for k in arr]
    perms = permutations(ints)
    # perm_string = []
    perm_ints = []
    # pdb.set_trace()
    for kk in perms:
        num = int(''.join(map(str,kk)))
        if num % 8 == 0:
            return "YES"
    return "NO"



if __name__ == '__main__':
    blah = checkDivisibility('1234')
    print(blah)
    pdb.set_trace()
