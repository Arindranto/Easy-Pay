# -*- coding: Utf-8 -*-
# Basic calculations
from utils.date_module import dateDiff

###############################################################################################################################################################
def isPositive(nbr: float):
    "Return 0 if a number is not positive or the number if it is"
    if nbr <= 0:
        return 0
    return nbr
###############################################################################################################################################
def salaryCalc(sAmount, quota, wHour, bDate, eDate, fisc, maj= 0):
    "To calculate the salary"
    return sAmount/(quota * 4.0) * (wHour - isPositive(wHour - dateDiff(bDate, eDate) * quota/7.0) * (1 - maj/100.0)) * (1 - fisc/100.0)