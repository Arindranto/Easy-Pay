# -*- coding: Utf-8 -*-
'''Indication:
    *** Foreign keys starts with uppercase to ease the database reading
    *** Three main table: Functions, Employes, Salaries, Presences
'''

# Module to manipulate the Sqlite database
import sqlite3 as sql
import os
from models.db_info import DICT
import utils.app_state as app_state
from utils.crypto import crypt, normalize    # To crypt the data

######################################################################################################

# Get the working database
db= app_state.read()[0]

######################################################################################################
def createTable(cursor, tableName, fields):
    #"Use a cursor to create a table in the database"
    #con, cursor= connect()
    #try:
        # Casting the query
        query= 'CREATE TABLE ' + tableName + '('
        for field in fields:
            if field != 'suppl': # For supplementary infos keys
                query= query + field + ' '
            query= query + fields[field] + ', '
        # Finalize the query
        query= query[:-2] + ');'

        cursor.execute(query)
        return True
    #except:
        #cursor.close()
        #con.close()
    #    return False
######################################################################################################
def insertInto(cursor, tableName, fields= None, datas= None):
    "Use a cursor to insert data in the database"
    try:
        query= 'INSERT INTO ' + tableName
        if fields: # If specified field
            query= query + '(' + ', '.join([field for field in fields]) + ')'
        query= query + ' VALUES '
        # Datas are replaced by ? to avoid SQL injection
        query= query + '(' + ', '.join(['?' for data in datas]) + ');'
        #print(query)
        cursor.execute(query, datas)
        return True # return the connection to close or confirm accoding to the needs
    except:
        return False

######################################################################################################
def selectFrom(cursor, tableNames, fields= None, conditions= ()):
    #"A select query"
        #print('Cursor is ', cursor)
    #try:
        # Start
        if fields:
            query= 'SELECT ' + ', '.join([field for field in fields])
        else:
            query= 'SELECT * '

        # Please notice that for joins, you must enter the join manually here in tableNames parameter
        query+= ' FROM ' + tableNames
        # Conditions
        if conditions:
            query+= ' WHERE '
        for condition in conditions:
            # conditions example includes (['something = ', value1, 'OR'], ['other thing <=', value2, 'AND'])
            #filler= filler + [condition[1] for condition in conditions]
            if len(condition) == 3: # Normal operator
                query+= condition[0] + ' ? ' + condition[2] + ' '
            elif len(condition) == 4: # Between ie: (['begin', 'value', 'end', 'logic operator'])
                # Careful to always place the condition in position 1
                query+= ' ? BETWEEN ' + condition[0] + ' AND ' + condition[2] + ' ' + condition[3] + ' '
        query= query + ';'
        #print(query)

        # execution condition
        if conditions:
            cursor.execute(query, tuple(condition[1] for condition in conditions))
        else:
            cursor.execute(query)
        return True
    #except:
        #return False

###########################################################################################################
def update(cursor, tableName, values, conditions):
    "Update operation"
    try:
        query= 'UPDATE ' + tableName + ' SET ' + ','.join(value[0] + ' = ? ' for value in values) + ' WHERE ' + ' '.join([condition[0] + ' ? ' + condition[2] for condition in conditions]) 
        cursor.execute(query, tuple(value[1] for value in values) + tuple(condition[1] for condition in conditions))
        return True # return the connection to close or confirm accoding to the needs
    except:
        return False
######################################################################################################
def create():
    "Creating the database in db directory using a data dictionnary"
    if os.path.isdir('db'): # If the db is in path
        conn= sql.connect('''db/management.db''')
        cur= conn.cursor()
        # CREATING THE TABLES
        # Company table(uName (username),
        #              cName (Company name),
        #              cAdr (Company adress),
        #              pass (Password))
        # replace with execute many
        #cur.execute_many()
        for table in DICT:
            createTable(cur, table, DICT[table])
        conn.commit()
        # Functions table(idFun (id),
        #                 fName (function name),
        #                 fPrefix (Prefix for the matricule))

        ###############################################################

        '''cur.execute("""CREATE TABLE Functions
        (
            idFun INTEGER PRIMARY KEY,
            fName VARCHAR(20),
            fPrefix VARCHAR(5)
        )""")
        
        # Person table(idEmp (id),
        #              pLast (Lastname, family name)
        #              pFirst (Firstname),
        #              pSex (gender)
        #              pBDate (Birthdate),
        #              pAdr (physocal adress),
        #              pEmail (email),
        #              pPhone (phone number),
        #              cStart (contract start),
        #              cEnd (contract end), 77777777 is the default value
        #              quota (Number of hours to be done for full salary),
        #              actualSal (actual salary),
        #              #idFun (function),
        #              num (rank for matricule generation),
        #              imgPath (path to the emlpoyee photo),
        #              isInactive (1 if the person is already inactive, else 0)
        cur.execute("""CREATE TABLE Persons
        (
            idPers INTEGER PRIMARY KEY,
            pLast VARCHAR(20),
            pFirst VARCHAR(20),
            pSex CHAR(1),
            pBDate INTEGER,
            pAdr VARCHAR(50),
            pEmail VARCHAR(50) NOT NULL DEFAULT "",
            pPhone VARCHAR(15),
            cStart INTEGER ,
            cEnd INTEGER DEFAULT 77777777,
            quota DECIMAL(3, 1),
            actualSal DECIMAL,
            Fun INTEGER,
            num INTEGER,
            imgPath VARCHAR DEFAULT 'photos/default.jpg',
            isInactive SMALLINT(1) NOT NULL DEFAULT 0,
            FOREIGN KEY(fun) REFERENCES Functions(idFun)
        )""")
        
        # Salaries table(
        #                idSal (salary id)
        #                bDate (beginning date),
        #                eDate (end date),
        #                pDate (payment date)
        #                wHour (total working hour in a month)
        #                sAmount (salary amount (brute)),
        #                fisc (Fiscal deduction),
        #                maj (Majoration for supplementary hours)
        #                Emp (Employee id))
        #                Composed primary key : bDate, eDate, Emp (Modified recently to eas selection)
        cur.execute("""CREATE TABLE Salaries
        (
            idSal INTEGER PRIMARY KEY,
            bDate INTEGER NOT NULL,
            eDate INTEGER NOT NULL,
            pDate INTEGER,
            wHour SMALLINT(3) NOT NULL DEFAULT 0,
            sAmount DECIMAL,
            fisc DECIMAL(5, 2) NOT NULL DEFAULT 0,
            maj DECIMAL(5, 2) NOT NULL DEFAULT 0,
            lib VARCHAR(50) NOT NULL DEFAULT 'Unknown',
            Emp INTEGER NOT NULL,
            FOREIGN KEY (Emp) REFERENCES Persons(idPers)
        )""")'''

        #########################################################################
        
        # Inserting the main admin in the app by default
        name= crypt('__MainAdmIN__')
        password= crypt('_*_EasyPayAdmin2022_*_')
        #cur.execute('INSERT INTO Companies(idCom, uName, pass) VALUES (%d, "%s", "%s")' %(0, name, password))
        insertInto(cur, 'Companies', ('idCom', 'uName', 'pass',), (0, name, password))
        # Creating Administrator function in Functions table
        insertInto(cur, 'Functions', ('idFun', 'fName',), (0, '__Admin__'))
        #cur.execute('INSERT INTO Functions(idFun, fName) VALUES (%d, "%s")' %(0 ,'__Admin__'))
        conn.commit()
        cur.close()
        conn.close()
    else: # create the db path
        os.mkdir('db')
        create()
    return
#####################################################################################################
def connect():
    "Ease the connection to the database with path db"
    con, cur = None, None
    try:
        con= sql.connect(db)    # By default db == 'db\management.db'
        cur= con.cursor()
        # Verify if the database is already actually filled
        cur.execute('''SELECT * FROM Functions''')
    except:
        try:
            #print('Must recreate the database')
            create()    # Recreate the database
            #print('Database created')
            # Reconnection after table creation
            con= sql.connect('''db/management.db''')
            cur= con.cursor()
            
            app_state.create(db= '''db/management.db''', appstate= 1)   # Reset the database path in the app_state module
        except:
            ...
    return con, cur # Return the connection and the cursor
    
########################################################################################################