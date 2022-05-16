# -*- coding: Utf-8 -*-

####################################
##### DATE TREATMENT FUNCTIONS #####
####################################


from datetime import datetime
from utils.converter import toNDigits

# CONSTANTS
# Day definition
DAYS= ['01','02','03','04','05','06','07','08','09',10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
# Month definition
MONTHS= ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sept', 'Oct', 'Nov', 'Déc']
LONG_M= ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
# Year Definition
YEARS= []
for i in range(1900, 2100):
    YEARS.append(i)

#################
### FUNCTIONS ###
#################
    
###############################################################################################################################################################
def dateDiff(bDate, eDate, limit= 28):
    "Return the number of days between two date in int format, first and last day count"
    day_numbers= [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] # Keep the day numbers
    # Keep the differences in a tuple (year_diff, month_diff, day_diff)
    date_1= [bDate // 10000, bDate % 10000 // 100, bDate % 100] # To store bDate 
    date_2= [eDate // 10000, eDate % 10000 // 100, eDate % 100]# To store eDate
    if date_1 == date_2:
        # If it's the same date
        return 1
    date_diff= 0
    while (date_1[0] < date_2[0] or date_1[1] < date_2[1]): # Begin with year and month comparison
        date_diff+= day_numbers[date_1[1]-1] - date_1[2]    # We complete the days first
        date_1[2]= 0    # No need of date_1[2] (day of the beginning date) from now on
        
        date_1[1]+= 1# Month is finished
        # If the month is up to 12
        if date_1[1] > 12:
            # Back to 1 and increment year
            date_1[1]= 1 # Month
            date_1[0]+= 1 # Year increment
            
            print(date_1[0])
            # Leap year check
            if not(date_1[0] % 4 and date_1[0] % 100) or not(date_1[0] % 400):
                day_numbers[1]= 29
    # Add the last days
    if bDate // 10000 == date_1[0] and bDate % 10000 // 100 == date_1[1]: # If we didn't change the year and month
        date_diff= date_2[2] - date_1[2] + 1
    else: # If we changed anything
        date_diff+= date_2[2] + 1
    if date_diff > limit: # Return the limit if it's up to the actual limit
        return limit
    return date_diff

###############################################################################################################################################################    
def today():
    "Return today's date in int format"
    return int(str(datetime.now()).split('-')[0] + str(datetime.now()).split('-')[1] + str(datetime.now()).split('-')[2].split()[0])

###############################################################################################################################################################    
def fullDate(date, style= 1):
    "Return full date from an integer given date in dd-mm-yyyy format"
    # If style is 1, it's full date (dd MonthName yyyy)
    if style == 1:
        return str(date % 100) + " " + LONG_M[date % 10000 // 100 - 1] + " " + str(date // 10000)
    # else return short style date (dd-mm-yyyy)
    return str(toNDigits(date % 100, 2)) + "-" + str(toNDigits(date % 10000 // 100, 2)) + "-" + str(date // 10000)

###############################################################################################################################################################
def dateToInt(date):
    "Return the integer format of a given dd-mm-yyyy date"
    return int(date.split('-')[2] + toNDigits(int(date.split('-')[1]), 2) + toNDigits(int(date.split('-')[0]), 2))

###############################################################################################################################################################
def firstDayOfMonth():
    "Return the first day of the current month in yyyymmdd int format"
    return today() // 100 * 100 + 1
###############################################################################################################################################################