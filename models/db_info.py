# -*- coding: Utf-8 -*-
# Basic data dictionnary
DICT= {
    'Companies': {
        'idCom': 'INTEGER PRIMARY KEY', # id
        'uName': 'VARCHAR(20)', # username
        'cName': 'VARCHAR(20)', # Company name
        'cAdr': 'VARCHAR(40)',  # Company adress
        'pass': 'VARCHAR(20)'   # Company password
    },
    'Functions': {
        'idFun': 'INTEGER PRIMARY KEY', # Function id
        'fName': 'VARCHAR(20)', # Function name
        'fPrefix': 'VARCHAR(5)' # Funtion prefix
    },
    'Persons':
    {
        'idPers': 'INTEGER PRIMARY KEY',    # id
        'pLast': 'VARCHAR(20)', # Lastname
        'pFirst': 'VARCHAR(20)',    # Firstname
        'pSex': 'CHAR(1)',  # Sex
        'pBDate': 'INTEGER',    # Birthdate
        'pAdr': 'VARCHAR(50)',  # Adress
        'pEmail': 'VARCHAR(50) NOT NULL DEFAULT ""',    # email
        'pPhone': 'VARCHAR(15)',    # Phone number
        'cStart': 'INTEGER',    # Contract start
        'cEnd': 'INTEGER DEFAULT 77777777', # Contract end
        'quota': 'DECIMAL(3, 1)',   # Weekly hour
        'actualSal': 'DECIMAL', # Actual salary
        'fun': 'INTEGER',   # function id (fk)
        'num': 'INTEGER',   # Number in the function
        'imgPath': 'VARCHAR DEFAULT "photos/default.jpg"', # image
        'isInactive': 'SMALLINT(1) NOT NULL DEFAULT 0', # activity, 0 for active employee, 1 for incative one
        'suppl': 'FOREIGN KEY (fun) REFERENCES Functions(idFun)'
    },
    'Salaries':
    {
        'idSal': 'INTEGER PRIMARY KEY', # id
        'bDate': 'INTEGER NOT NULL',    # beginning date
        'eDate': 'INTEGER NOT NULL',    # End date
        'pDate': 'INTEGER',             # Payment date
        'wHour': 'SMALLINT(3) NOT NULL DEFAULT 0',  # Worked hour
        'sAmount': 'DECIMAL',   # Salary amount
        'fisc': 'DECIMAL(5, 2) NOT NULL DEFAULT 0', # Fiscality
        'maj': 'DECIMAL(5, 2) NOT NULL DEFAULT 0',  # Majoration
        'lib': 'VARCHAR(50) NOT NULL DEFAULT "Unknown"',    # Justificative
        'Emp': 'INTEGER NOT NULL',  # Employee id (fk)
        'suppl': 'FOREIGN KEY (Emp) REFERENCES Persons(idPers)'
    }
}

# Correspondance variable for database treatments
CORRESP= {'Nom': 'pLast',
          'Prénoms': 'pFirst',
          'Prénom(s)': 'pFirst',
          'Téléphone': 'pPhone',
          'Fonction': 'fName',
          'Matricule': 'fPrefix || N_DIGITS(num, 10)',   # fPrefix suffice to order them by matricule
          'Salaire': 'actualSal',
          'Adresse': 'pAdr',
          'Fin de contrat': 'cEnd',
          'Début de contrat': 'cStart',
          'Etat': 'isInactive'}