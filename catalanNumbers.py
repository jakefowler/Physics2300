# Cn = (2n)! / (n+1)!n! 
# The first Catalan numbers for n = 0, 1, 2, 3, ... 
# are 1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786, 
# 208012, 742900, 2674440, 9694845, 35357670, 129644790, 477638700, 
# 1767263190, 6564120420, 24466267020, 91482563640, 343059613650, 
# 1289904147324, 4861946401452, ... 

from math import factorial as fac
n = 0
CatalanNum = 0
while CatalanNum < 1e9:
    CatalanNum = (fac((2*n)) // (fac((n + 1)) * fac(n)))
    if CatalanNum < 1e9:
        print(CatalanNum)   
    n += 1
