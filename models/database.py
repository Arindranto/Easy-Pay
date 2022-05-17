# -*- coding: Utf-8 -*-
# Database class to easily manipulate the models
#import sqlite3 as sql
from tkinter import messagebox
from models.database_basics import connect, selectFrom, insertInto

def getInfoById(empId):
	infos= ('idPers', 'pLast', 'pFirst', 'pSex', 'pBDate', 'pAdr', 'pEmail', 'pPhone', 'fName', 'fPrefix', 'num', 'cStart', 'actualSal', 'cEnd', 'quota', 'isInactive', 'imgPath')
	con, cur= connect()
	selectFrom(cur, 'Functions JOIN Persons ON idFun = fun', infos, (['idPers = ', empId, ''],))
	result= cur.fetchone()
	cur.close()
	con.close()
	return result
############################################################################################
def getFunctions():
    "Select all the functions"
    con, cur = connect()
    selectFrom(cur, 'Functions', ('fName',), (['idFun <> ', 0, ''],))
    result= [function[0] for function in cur.fetchall()]
    cur.close()
    con.close()
    return result
    #functions= []
    #for function in cur.execute('''SELECT fName FROM Functions WHERE idFun <> 0''').fetchall():
    #    functions.append(function[0])
    #return functions
###########################################################################################
def askPass(message= ''):
    "Ask password and return True or false value"
    con, cur= connect() # Connection to the database
    # Appending passwords to the lists
    selectFrom(cur, 'Companies', ('pass',))
    passes= [password[0] for password in cur.fetchall()]
    #for password in cur.fetchall():
    #    passes.append(password[0])
    verified= False
    while not verified:  # Ask password to confirm the commitment
        try:
            if crypt(simpledialog.askstring('Easy Pay', message, show= '\u25cf')) not in passes:
                messagebox.showerror('', 'Mot de passe incorrect')
                verified= False
            else:
                verified= True
        except:
            break # Because NoneType is not iterable for crypt method
    cur.close()
    con.close()
    return verified
###########################################################################################################
def insertEmployee(pLast, pFirst, pSex, pBDate, pAdr, pEmail, pPhone, cStart, Fun, num, quota, actualSal, imgPath, cdd= False):
	"Insert a new employee"
	con, cur= connect()	# Connection
	fields= ['pLast', 'pFirst', 'pSex', 'pBDate', 'pAdr', 'pEmail', 'pPhone', 'cStart', 'Fun', 'num', 'quota', 'actualSal', 'imgPath']
	datas= [pLast, pFirst, pSex, pBDate, pAdr, pEmail, pPhone, cStart, Fun, num, quota, actualSal, imgPath]
	if cdd:
		fields.append('cEnd')
		datas.append(cdd)
	insertInto(cur, 'Persons', fields, datas)
	return con 	# Return for confirmation or other
###########################################################################################################################
def updateEmployee(idPers, pLast, pFirst, pAdr, pEmail, pPhone, actualSal, cEnd, quota, imgPath):
	"Updating an Employee"
	message= ''	# To return, the comparison between the 2 states