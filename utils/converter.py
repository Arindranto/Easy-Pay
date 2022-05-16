# -*- coding: Utf-8 -*-
# To n digits
def toNDigits(nbr, n):
    "Cast a number to a string spanning n digits"
    var= str(nbr)
    return '0' * (n - len(var)) + var