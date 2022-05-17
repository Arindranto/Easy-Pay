# -*- coding: Utf-8 -*-
import tkinter as tk
from shutil import copyfile
from PIL import ImageTk, Image
from tkinter import messagebox, simpledialog, ttk, filedialog
# Models
from models.database_basics import connect, selectFrom, insertInto, update
from models.db_info import CORRESP
from models.database import getInfoById, getFunctions, askPass, insertEmployee
# Utils
from utils.crypto import crypt
from utils.date_module import dateDiff, today, fullDate, LONG_M, firstDayOfMonth
from utils.calculator import salaryCalc
# Views
from views.form_module import centralize, Form, Input, borderColor, DateEntry, MASKS

#########################################################################################################################################################################
# Correspondance variable for database treatments
'''CORRESP= {'Nom': 'pLast',
          'Prénoms': 'pFirst',
          'Prénom(s)': 'pFirst',
          'Téléphone': 'pPhone',
          'Fonction': 'fName',
          'Matricule': 'fPrefix || N_DIGITS(num, 10)',   # fPrefix suffice to order them by matricule
          'Salaire': 'actualSal',
          'Adresse': 'pAdr',
          'Fin de contrat': 'cEnd',
          'Début de contrat': 'cStart',
          'Etat': 'isInactive'}'''
#########################################################################################################################################################################
'''def askPass(message= ''):
    "Ask password and return True or false value"
    con, cur= connect() # Connection to the database
    passes= []
    # Appending passwords to the lists
    for password in cur.execute('SELECT pass FROM Companies').fetchall():
        passes.append(password[0])
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
    return verified'''
#########################################################################################################################################################################
#def salaryCalc(sAmount, quota, wHour, bDate, eDate, fisc, maj= 0):
#    "To calculate the salary"
#    return sAmount/(quota * 4.0) * (wHour - isPositive(wHour - dateDiff(bDate, eDate) * quota/7.0) * (1 - maj/100.0)) * (1 - fisc/100.0)
#######################################################################################################################################################################

class EmployeeForm(tk.Toplevel):
    "The form to add an employee"
    def __init__(self, boss, emp= None):
        "Constructor method"
        tk.Toplevel.__init__(self, boss)
        # About the window
        self.title("Informations sur le salarié")
        self.withdraw()
        try:    # Icon placing
            self.iconbitmap('icons/emp_icon.ico')
        except:
            pass
        self.resizable(0, 0)    # Unresizable
        # THE BIOGRAPHY FORM
        self.bio= Form(self,
                   lList= (['Nom', 22],
                   ['Prénom(s)', 22],
                   ['Adresse', 22],
                   ['Email', 22],
                   ['Téléphone', 15],),
                   iFPad= ((5, 5), (5, 10))
                   )
        self.bio.iList['Birthdate']= DateEntry(self.bio.iFrame, label= 'Date de\nnaissance', default= 20000101) # A date entry for the birthdate
        
        # Placements of the first 3 Inputs
        self.bio.placeInputs(iNames= ('Nom', 'Prénom(s)', 'Birthdate'),
                        padx= (5, 5), pady= (0, 5),
                        spans= (1, 1, 1,))
        # Radio button for gender
        tk.Label(self.bio.iFrame, text= 'Sexe ', font= 'Arial 9 bold').grid(row= 4, column= 1, sticky= tk.W, padx= (5, 0))
        self.gender= tk.StringVar()  # The variable that will store the gender
        self.gender.set('M')
        # Radios
        m= tk.Radiobutton(self.bio.iFrame, anchor= 'w', variable= self.gender, value= 'M', text= 'Homme', command= None)
        m.grid(row= 5, column= 1, sticky= tk.W, padx= (20, 0), columnspan= 2)
        f= tk.Radiobutton(self.bio.iFrame, anchor='w', variable= self.gender, value= 'F', text= 'Femme', command= None)
        f.grid(row= 6, column= 1, sticky= tk.W, padx= (20, 0), columnspan= 2)
        
        # Adress, email and phone number inputs placing
        self.bio.placeInputs(start= 8, iNames= ('Adresse', 'Email', 'Téléphone',), padx= (5, 5), pady= (5, 5), spans=(1, 1, 1,))

        # THE CONTRACT FORM
        self.contract= Form(self,
                   lList= (),
                   iFPad= ((5, 5), (5, 10))
                   )
                   
        
        self.matr = tk.StringVar() # Label to show the matricule if there is one
        self.matr.set('(Matricule)')    # By default it will be 'Matricule'
        tk.Label(self.contract.iFrame, textvariable= self.matr, font= 'Arial 10 bold').grid(row= 1, column= 1, columnspan= 3)   # The concerned label
        
        # Contract type choice
        tk.Label(self.contract.iFrame, text= 'Type', font= 'Arial 9 bold').grid(row= 2, column= 1, sticky= tk.W, padx= (5, 0))   # The title
        self.conType= tk.StringVar()
        self.conType.set('cdd') # cdd by default
        
        # Gridding methods
        def grid_forget():
            "Take out the contract end date entry"
            if self.conType.get() == 'cdi':    # If cdd is selected, remove the contract end information
                self.contract.iList['Contract end'].label.grid_forget()
                self.contract.iList['Contract end'].grid_forget()
        def grid():
            "Place the contract end date"
            if self.conType.get() == 'cdd':  # If cdi is selected
                self.contract.placeInputs(start= 8, iNames= ('Contract end',), padx= (5, 5), pady= (0, 0), spans= (2,))
        
        # Contract type radios
        cdd= tk.Radiobutton(self.contract.iFrame, anchor= 'w', variable= self.conType, value= 'cdd', text= 'CDD', command= grid)
        cdd.grid(row= 2, column= 2, sticky= tk.W)
        cdi= tk.Radiobutton(self.contract.iFrame, anchor='w', variable= self.conType, value= 'cdi', text= 'CDI', command= grid_forget)
        cdi.grid(row= 2, column= 3, sticky= tk.W)
        
        tk.Label(self.contract.iFrame, text= 'Fonction', font= 'Arial 9 bold').grid(row= 3, column= 1, sticky= tk.W, padx= (5, 0))
        # The function combobox
        self.comboFrame= tk.Frame(self.contract.iFrame, highlightthickness= 1)  # The border for the combobox
        self.funCombo= ttk.Combobox(self.comboFrame,
                               values= getFunctions(),
                               state= 'normal',
                               width= 16,
                               )    # The function combobox
        
        # Other input declaration
        self.contract.iList['Horaire hebdomadaire']= Input(self.contract.iFrame, label= 'Horaire hebdomadaire', needed= 1, width= 6)   # Hour number per week
        self.contract.iList['Salaire mensuel']= Input(self.contract.iFrame,
                                                      label= 'Salaire mensuel brut',
                                                      width= 15,
                                                      needed= 1) # Salary input
        self.contract.iList['Contract start']= DateEntry(self.contract.iFrame, default= today(), label= 'Début de contrat') # A date entry for Contract start
        self.contract.iList['Contract end']= DateEntry(self.contract.iFrame, default= today() + 50000, label= 'Fin de contrat') # A date entry for Contract end by 5 years by default
        
        # FORM TITLES
        # Employee photo
        self.imgframe= tk.Frame(self.bio.iFrame, highlightthickness= 2)
        self.empImg= tk.Button(self.imgframe, command= self.choosePhoto, relief= tk.FLAT)   # The Button for the image
        borderColor(self.imgframe)  # Setting the image border
        
        self.setEmpPhoto()  # Set the image
        
        self.empImg.pack(padx= 1, pady= 1)  # Place the button      
        self.imgframe.grid(row= 0, column= 1, columnspan= 2, pady= (0, 10)) # PLacing the frame
        
        tk.Label(self.contract.iFrame, text= 'CONTRAT', font= 'Arial 11 bold').grid(row= 0, column= 1, columnspan= 3)
        # Forms reliefs
        self.bio.config(bd= 2, relief= tk.GROOVE)
        self.contract.config(bd= 2, relief= tk.GROOVE)
        
        # Input placing
        self.contract.placeInputs(start= 4, iNames= ('Horaire hebdomadaire', 'Salaire mensuel',),
                                  padx= (2, 5), pady= (2, 2), spans= (2, 2, ))
        self.contract.placeInputs(start= 7, iNames= ('Contract start', 'Contract end',),
                                  padx= (5, 5), pady= (5, 2), spans= (2, 2, ))
        # Button placement
        self.contract.placeButtons(side= 'bottom',
                          anchor= tk.CENTER,
                          labels= ('Vider', 'Enregistrer'),
                          colors= (['light grey', 'black'], ['green', 'white'],),
                          bPad= ((5, 5), (0, 10)),
                          fPad= (0, (0, 0)))
        
        # FINAL ITEM PLACING
        self.funCombo.pack()    # Funciton combobox
        self.comboFrame.grid(row= 3, column= 2, sticky= tk.W, padx= (0, 5), pady = 3, columnspan= 3) # Functions combobox Frame
        self.bio.grid(row= 0, column= 0, sticky= tk.N, padx= (10, 5), pady= 10)     # Biography form
        self.contract.grid(row= 0, column= 1, sticky= tk.N+tk.S, padx= (5, 10), pady= 10)   # Contract form
        
        # Button configuration
        self.contract.bList['Enregistrer'].config(command= self.add)
        self.contract.bList['Vider'].config(command= self.reset)
        
        # Input mask for regex checking
        self.bio.iList['Adresse'].mask= MASKS['alphanum']
        self.bio.iList['Téléphone'].mask= MASKS['phone']
        self.bio.iList['Email'].mask= MASKS['email']
        self.contract.iList['Salaire mensuel'].mask= MASKS['number']
        self.contract.iList['Horaire hebdomadaire'].mask= MASKS['number']
        
        # Unnecessary input
        self.bio.iList['Email'].needed = 0

        # Inputs linking and other bindings
        def enter(event= None):
            "To enter the function combobox"
            self.funCombo.focus_set()
            return
        self.bio.iList['Téléphone'].bind('<Return>', enter) # Link the last input in the first form to the first input of the second form
        self.funCombo.bind('<<ComboboxSelected>>', self.generateMatricule) # Generate a matricule for the current person
        self.funCombo.bind('<KeyRelease>', self.generateMatricule) # Generate a matricule for the current person
        self.funCombo.bind('<Return>', self.contract.iList['Horaire hebdomadaire'].enter) # Enter next input
        self.contract.iList['Horaire hebdomadaire'].bind('<Return>', self.contract.iList['Salaire mensuel'].enter) # Enter next input
        
        # If emp is provided, it's for information showing and potential editing
        if emp != None:
            #con, cur= connect() # db connection
            # Fetch the data from the database
            # self.current= (0: idPers,
            #                1: pLast,
            #                2: pFirst,
            #                3: pSex,
            #                4: pBDate,
            #                5: pAdr,
            #                6: pEmail,
            #                7: pPhone,
            #                8: fName,
            #                9: fPrefix,
            #                10: num,
            #                11: eStart,
            #                12: actualSal,
            #                13: cEnd,
            #                14: quota,
            #                15: isInactive
            #                16: imgPath)
            #self.current= cur.execute('''SELECT idPers, pLast, pFirst, pSex, pBDate, pAdr, pEmail, pPhone, fName, fPrefix, num, cStart, actualSal, cEnd, quota, isInactive, imgPath
            #                          FROM Functions JOIN Persons ON idFun = Fun WHERE idPers = %d''' %(emp)).fetchone()
            # Close the db properly
            #cur.close()
            #con.close()
            self.current= getInfoById(emp)
            # The employee photo is in index 16
            self.setEmpPhoto(self.current[16])
            
            def doNothing():
                return
            
            if self.img != 'photos/default.jpg' or self.current[15]:    # Disable the button if the image is logged successfully or if the employee is already inactive
                self.empImg.config(command= doNothing)
                
            self.matr.set(self.current[9] + '-' + str(self.current[10]))    # Matricule set
            
            # Data insertion in the form
            self.bio.iList['Nom'].insert(tk.END, self.current[1])
            self.bio.iList['Prénom(s)'].insert(tk.END, self.current[2])

            self.bio.iList['Adresse'].insert(tk.END, self.current[5])
            try:
                self.bio.iList['Email'].insert(tk.END, self.current[6]) # There might be no email at all
            except:
                ...
            self.bio.iList['Téléphone'].insert(tk.END, self.current[7])
            self.funCombo.set(self.current[8])
            self.contract.iList['Horaire hebdomadaire'].insert(tk.END, self.current[14])
            self.contract.iList['Salaire mensuel'].insert(tk.END, self.current[12])
            # Make some entry unmodifiable
            self.funCombo.config(state= 'disabled')
            self.contract.iList['Contract start'].config(default= self.current[11], state= 'disabled')
            self.bio.iList['Birthdate'].config(default= self.current[4], state= 'disabled')
            f.config(state= 'disabled')
            m.config(state= 'disabled')
            # About contract type
            if self.current[13] != 77777777: # If ther is a value, it is a cdd
                self.contract.iList['Contract end'].config(default= self.current[13])
            else:   # else cdi
                self.conType.set('cdi')
                grid_forget()   #Takeout the contract end entry
            # INACTIVE EMPLOYEE
            if self.current[15]:    # If the employee is already inactive, make all the inputs disabled
                # Personal information
                self.bio.iList['Nom'].config(state= 'disabled')
                self.bio.iList['Prénom(s)'].config(state= 'disabled')
                self.bio.iList['Adresse'].config(state= 'disabled')
                self.bio.iList['Email'].config(state= 'disabled')
                self.bio.iList['Téléphone'].config(state= 'disabled')
                # Contract informations
                self.contract.iList['Contract end'].config(default= self.current[13], state= 'disabled')
                self.contract.iList['Horaire hebdomadaire'].config(state= 'disabled')
                self.contract.iList['Salaire mensuel'].config(state= 'disabled')
                
                # Contract type
                cdd.config(state= 'disabled')
                cdi.config(state= 'disabled')
                # Remove the buttons
                self.contract.bList['Vider'].config(text= 'Salarié licencié', bg= 'red', fg= 'white', relief= tk.FLAT, command= None)    # Message
                self.contract.bList['Enregistrer'].pack_forget()
            else:   # Change the button works
                self.contract.bList['Vider'].config(text= 'Licencier', bg= 'red', fg= 'white', command= self.fire)
                self.contract.bList['Enregistrer'].config(text= 'Modifier', command= self.update)
            # Cut the current variable to the necessary ones [0: idPers, 1: pLast, 2: pFirst, 3: pAdr, 4: pEmail, 5: pPhone, 6: actualSal, 7: cEnd, 8: quota, 9: imgPath]
            self.current= self.current[0:3]+self.current[5:8]+self.current[12:15] + (self.current[16],)
        # On window closing action
        self.protocol('WM_DELETE_WINDOW', self.quit)
        self.bio.iList['Nom'].enter()   # Enter the first input by deafault
        
        # Show it when ready
        self.deiconify()
        centralize(self)    # Centralization of the Toplevel
        self.grab_set()
        self.mainloop()
        # Destroy after main loop ends
        self.destroy()
        return
    ########################################################################################################################################################################
    def setEmpPhoto(self, path= 'photos/default.jpg'):
        "Setting the photo of the employee"
        try:
            img= ImageTk.PhotoImage(Image.open(path).resize((70, 80), Image.ANTIALIAS))  # Try to open an image
            self.img= path # set path
        except:
            self.img= 'photos/default.jpg'
            img= ImageTk.PhotoImage(Image.open(self.img).resize((70, 80), Image.ANTIALIAS))   # Enter the default one
        # Place the image
        self.empImg['image']= img
        self.empImg.image= img
    #########################################################################################################################################################################
    def choosePhoto(self):
        "Choose the photo of the employee using filedialog"
        img= filedialog.askopenfilename(initialdir= 'd:/') # With initial directory always set at d:/
        # Copy the image in the photos file
        if img != '':   # Copy if an image was selected and change the image of the empImg
            self.img= 'photos/' + img.split('/')[-1]    # Setting the self.img
            try: # If they are not the same file
                copyfile(img, self.img) # Copying the file to the photos directory
            except:   # If it's the same file
                ...
            self.setEmpPhoto(self.img)  # Setting the image
    #########################################################################################################################################################################
    def reset(self):
        "For resetting all the inputs"
        self.bio.reset()
        self.contract.reset()
        self.funCombo.delete(0, tk.END) # The function combobox
        return
    #######################################################################################################################################################################
    def generateMatricule(self, event= None):
        "Generate a matricule for the current employee"
        try:    # Generate a matricule if the function is existant
            con, cur= connect()
            selectFrom(cur, 'Functions', ('fPrefix', 'idFun',), (['fName = ', self.funCombo.get().title(), ''],))   # Get the prefix
            p= cur.fetchone()
            selectFrom(cur, 'Persons', ('COUNT(idPers)',), (['fun = ', p[1], ''],))
            self.matr.set(p[0] + '-' + str(cur.fetchone()[0] + 1))
        except: # else by default it' s '(Matricule)'
            self.matr.set('(Matricule)')
        # Close connection
        if con or cur:
            cur.close()
            con.close()
        return
    #######################################################################################################################################################################
    def add(self):
        "Add the values to the database"
        isSet= self.bio.verify() * self.contract.verify()   # Verify the 2 forms first
        # Test of the funCombo if it's blank
        if self.funCombo.get() == '':
            borderColor(self.comboFrame, 'red')
            isSet= 0
        else:
            borderColor(self.comboFrame)
        # Test the date conformity
        if (self.conType.get() == 'cdd'
            and (self.contract.iList['Contract end'].getDate() - self.contract.iList['Contract start'].getDate() < 0)):
            borderColor(self.contract.iList['Contract start'], 'red')
            borderColor(self.contract.iList['Contract end'], 'red')
            # isSet will be used to mark the validity of all the inputs
            isSet= 0
        else:
            borderColor(self.contract.iList['Contract start'])
            borderColor(self.contract.iList['Contract end'])
        # Test the function name
        function= self.funCombo.get().title()    # Get the function entered
        
        # __Admin__ is a reserved function
        if function == "__Admin__":
            # Show error message
            messagebox.showerror('Easy Pay', 'La fonction "__Admin__" est invalide')
            isSet= 0
        
        # Check if the image is the default one
        if self.img == 'photos/default.jpg':
            borderColor(self.imgframe, 'red')
            isSet= 0
        else:
            borderColor(self.imgframe)
        
        # Enter only if the inputs were valid
        if isSet:
            # Pass the values to the database
            con, cur= connect() # connect to the database
            
            # First check the function if it is a new one
            selectFrom(cur, 'Functions', ('idFun', 'fPrefix', ), (['fName = ', function, ' AND '], ['fName <> ', 'Administrator', ''],))
            idFun= cur.fetchone() # Get one
            
            add= 1  # add is a check variable either to add the person or not
            
            if idFun == None: # if the function return None, add it before everything
                #ask= 0
                pre= '' # To get the prefix values
                while pre == '':   # While the user entered void string and it was not cancelled
                    pre= simpledialog.askstring("Ajout d'une nouvelle fonction", 'Préfixe des matricules pour la fonction: ' + function, parent= self)
                    pre= pre.upper()
                    # Condition to validate the values
                    if pre is not None:
                        selectFrom(cur, 'Functions', ('fName',), (['fPrefix = ', pre, ''],))
                        add= cur.fetchone() # Check if the prefix is already used
                        insertInto(cur, 'Functions', ('fName', 'fPrefix',), (function, pre))    # Insertion
                        #cur.execute('''INSERT INTO Functions(fName, fPrefix) VALUES('%s', '%s')''' %(function, pre))    # Insertion
                        if add is None: # Valid prefix
                            add= 1  # Change the adding variable, cause we can add
                            con.commit()    # Commit change
                            selectFrom(cur, 'Functions', ('idFun', 'fPrefix',), (['fName = ', function, ''],))
                            idFun= cur.fetchone()    # Get the idFun and the prefix
                        else:   # Already used prefix
                            messagebox.showerror('Easy Pay', 'Le préfixe est déjà utilisé pour la fonction: ' + add[0].title())
                            #ask= 0
                            pre = ''    # Reloop
                # Close the database on leaving the loop
                cur.close()
                con.close()

            # Insertion
            if add:
                # Reconnect to the database
                #con, cur= connect()
                
                self.generateMatricule() # Matricule generation
                # Query cast
                #req= '''INSERT INTO 
                #            Persons(pLast, pFirst, pSex, pBDate, pAdr, pEmail, pPhone, cStart, Fun, num, quota, actualSal, imgPath'''
                #if self.conType.get() == 'cdd':
                #    req+= ', cEnd'
                #req+= ''') VALUES('%s', '%s', '%s', %d, '%s', '%s', '%s', %d, %d, %d, %d, %f, "%s"''' %(
                #              self.bio.iList['Nom'].get().title(),
                #              self.bio.iList['Prénom(s)'].get().title(),
                #              self.gender.get(),
                #              self.bio.iList['Birthdate'].getDate(),
                #              self.bio.iList['Adresse'].get().title(),
                #              self.bio.iList['Email'].get(),
                #              self.bio.iList['Téléphone'].get(),
                #              self.contract.iList['Contract start'].getDate(),
                #              idFun[0],
                #              int(self.matr.get().split('-')[1]),
                #              float(self.contract.iList['Horaire hebdomadaire'].get()),
                #              float(self.contract.iList['Salaire mensuel'].get()),
                #              self.img)
                              # , ask)
                # cdd case
                if self.conType.get() == 'cdd':
                    cdd= self.contract.iList['Contract end'].getDate()
                else:
                    cdd= False  # CDI
                con= insertEmployee(
                        self.bio.iList['Nom'].get().title(),
                        self.bio.iList['Prénom(s)'].get().title(),
                        self.gender.get(),
                        self.bio.iList['Birthdate'].getDate(),
                        self.bio.iList['Adresse'].get().title(),
                        self.bio.iList['Email'].get(),
                        self.bio.iList['Téléphone'].get(),
                        self.contract.iList['Contract start'].getDate(),
                        idFun[0],
                        int(self.matr.get().split('-')[1]),
                        float(self.contract.iList['Horaire hebdomadaire'].get()),
                        float(self.contract.iList['Salaire mensuel'].get()),
                        self.img,
                        cdd
                    )
                #cur.execute(req)    # Execute
                con.commit() # Commit
                # Close the connection
                #cur.close()
                con.close()
                
                self.master.update()    # Update the master treeview
                
                self.withdraw() # Withdraw the window
                messagebox.showinfo('Easy Pay', 'Nouveau salarié enregistré')   # Success message
                
                self.quit()  # Quit the main loop
        else:   # Don't add yet
            ...
        return
    #########################################################################################################################################################################
    def fire(self):
        "To fire an employee is to modify his active state to 0"
        con, cur= connect() # db connection
        
        # Set inactive to one
        update(cur, 'Persons', (['isInactive', 1], ['cEnd', today()],), (['idPers = ', self.current[0], ''],))
        #cur.execute('''UPDATE Persons SET isInactive= 1, cEnd= %d WHERE idPers = %d''' %(today(), self.current[0]))
        
        # if messagebox.askyesno('Easy Pay', 'Voulez-vous vraiment licencier cet employé?'):  # Confirm
        if messagebox.askyesno('Easy Pay', 'Licencier le salarié?'): # always ask passwords for irrevocable changes
            con.commit()    # Commit the changes
            try:
                self.master.master.master.master.refresh()  # Refresh the full app if it is in a main application
            except:
                # Else update the master only
                self.master.update()
            self.quit()
        else:
            self.grab_set() # Grab the focus if false
        # Close the connection
        cur.close()
        con.close()
    #########################################################################################################################################################################
    def update(self):   
        "To update an already existing person"
        # First check if the input are valid
        isSet= self.bio.verify() * self.contract.verify()
        # Date conformity
        if (self.conType.get() == 'cdd'
            and (self.contract.iList['Contract end'].getDate() - self.contract.iList['Contract start'].getDate() < 0)):
            borderColor(self.contract.iList['Contract start'], 'red')
            borderColor(self.contract.iList['Contract end'], 'red')
            # isSet is a checking variable
            isSet = 0
        else:
            borderColor(self.contract.iList['Contract start'])
            borderColor(self.contract.iList['Contract end'])
            
        if self.img == 'photos/default.jpg':  # If it is the default photo
            borderColor(self.imgframe, 'red')
            isSet= 0
        else:
            borderColor(self.imgframe)

        datas= []
        # Enter if valid
        if isSet:
            # Query cast
            # get the current input values
            # self.current == [0: idPers, 1: pLast, 2: pFirst, 3: pAdr, 4: pEmail, 5: pPhone, 6: actualSal, 7: cEnd, 8: quota, 9: imgPath]
            message= ''
            # Image modification
            if self.current[9] != self.img:
                message+= 'Modification de la photo\n'
                datas.append(['imgPath', self.img])
            
            change= ('Nom', 'Prénom(s)', 'Adresse')
            # Compare Firstname, Lastname, Adress to generate a comparison message
            for i in range(1, 4):
                if self.current[i] != self.bio.iList[change[i-1]].get().title():
                    message += change[i-1] + ': ' + self.current[i] + ' ---> ' + self.bio.iList[change[i-1]].get().title() + '\n' # Message
                    #req+= ''' ''' + CORRESP[change[i-1]] + ''' = "%s"''' %(self.bio.iList[change[i-1]].get().title()) + ''','''  # Query
                    datas.append([CORRESP[change[i-1]], self.bio.iList[change[i-1]].get().title()])
                    # val+= ', "%s"' %(self.bio.iList[change[i]].get().lower())
            # Email
            if self.current[4] != self.bio.iList['Email'].get():
                message += 'Email: ' + self.current[4] + ' ---> ' + self.bio.iList['Email'].get() + '\n'    # Message
                #req+= ''' pEmail = "%s"''' %(self.bio.iList['Email'].get()) + ''','''   # Query
                datas.append(['pEmail', self.bio.iList['Email'].get()])
            # Phone number
            if self.current[5] != self.bio.iList['Téléphone'].get():
                message += 'Téléphone: ' + self.current[5] + ' ---> ' + self.bio.iList['Téléphone'].get() + '\n'    # Message
                #req+= ''' pPhone = "%s"''' %(self.bio.iList['Téléphone'].get()) + ''','''   # Query
                datas.append(['pPhone', self.bio.iList['Téléphone'].get()])
            # Monthly salary
            if self.current[6] != float(self.contract.iList['Salaire mensuel'].get()):
                message += 'Salaire mensuel: ' + str(self.current[6]) + ' ---> ' + self.contract.iList['Salaire mensuel'].get() + '\n'  # Message
                #req+= ''' actualSal= %f''' %(float(self.contract.iList['Salaire mensuel'].get())) + ''',''' # Query
                datas.append(['actualSal', float(self.contract.iList['Salaire mensuel'].get())])
            # Weekly quota
            if self.current[8] != int(self.contract.iList['Horaire hebdomadaire'].get()):
                message += 'Horaire hebdomadaire: ' + str(self.current[8]) + ' ---> ' + self.contract.iList['Horaire hebdomadaire'].get() + '\n'    # Message
                #req+= ''' quota= %f''' %(float(self.contract.iList['Horaire hebdomadaire'].get())) + ''','''    # Query
                datas.append(['quota', float(self.contract.iList['Horaire hebdomadaire'].get())])
            # Contract date details
            if  self.conType.get() == 'cdd' and self.current[7] != self.contract.iList['Contract end'].getDate():    # For CDD
                    message += ('Date de fin de contrat: '
                    + str(self.contract.iList['Contract end'].getDate())[6:8] + ' '
                    + LONG_M[int(str(self.contract.iList['Contract end'].getDate())[4:6]) - 1] + ' '
                    + str(self.contract.iList['Contract end'].getDate())[0:4] + '\n'
                    )   # Message
                    #req+= ''' cEnd = %d''' %(self.contract.iList['Contract end'].getDate()) + ''','''   # Query
                    datas.append(['cEnd', self.contract.iList['Contract end'].getDate()])
            elif self.conType.get() == 'cdi' and self.current[7] != 77777777: # Contract type modification
                    message += 'Modification du type de contrat à: CDI\n' # Message
                    #req+= ''' cEnd = 77777777,'''   # Query
                    datas.append(['cEnd', 77777777])
            # Finalisation of the person update query
            #req= req[0:-1] + ''' WHERE idPers = %d''' %(self.current[0])    # -1 because of the last comma when concatenationg the query
            # Ask to validate the changes
            if message != '':   # If we have a message, we should ask
                con, cur= connect() # Connection to the db
                update(cur, 'Persons', datas, (['idPers = ', self.current[0], ''],))
                #cur.execute(req) # Execute the query
                if messagebox.askyesno('Easy Pay', message + '\nEnregistrer le(s) modification(s)?'):
                    con.commit()    # Commit if the user accepts it
                    messagebox.showinfo('Easy Pay', 'Modification(s) enregistré(s) avec succès')    # Success message
                    # Update current employee information for the form [0: idPers, 1: pLast, 2: pFirst, 3: pAdr, 4: pEmail, 5: pPhone, 6: actualSal, 7: cEnd, 8: quota]
                    selectFrom(cur, 'Persons',
                                ('idPers', 'pLast', 'pFirst', 'pAdr', 'pEmail', 'pPhone',
                                'actualSal', 'cEnd', 'quota', 'imgPath',), (['idPers = ', self.current[0], ''],))
                    self.current= cur.fetchone()
                    self.master.update()    # Update the master after that
                else:
                    self.grab_set() # Grab the focus if false
                # Close the database
                cur.close()
                con.close()
            self.bio.iList['Nom'].enter()   # Enter the first input again
#########################################################################################################################################################
class PayForm(tk.Toplevel):
    def __init__(self, boss, emp, sal= None):
        "Constructor method"
        tk.Toplevel.__init__(self, boss)    # Instanciation of the parent class
        self.title('Fiche de paie') # Title
        self.protocol('WM_DELETE_WINDOW', self.quit)    # Quit on delete window protocol
        self.resizable(0, 0)  # Unresizable
        
        # Try adding icon
        try:
            self.iconbitmap('icons/info_icon.ico')
        except:
            ...
        # Pay Form
        self.form= tk.Frame(self, relief= tk.GROOVE, bd= 2) # first start with the persons information
        # Database connection to get the person information
        con, cur= connect()
        # self.pers[Lastname and Firstname, function name, matricule, actual salary, quota, image]
        self.pers= cur.execute('''SELECT pLast || '\n' || pFirst, fName, fPrefix || "-" || num, actualSal, quota, imgPath 
                                  FROM Functions JOIN Persons ON idFun = Fun
                                  WHERE idPers = %d''' %(emp)).fetchone()
        # Close the connection after querying it
        cur.close()
        con.close()
        
        # Form text filling
        self.labels= ('Nom et prénom(s)', self.pers[0], 'Fonction', self.pers[1], 'Matricule', self.pers[2],
                      'Salaire mensuel brut', self.pers[3], 'Horaire hebdomadaire\ncontractuel', self.pers[4],) # Labels for the text
        # Place the image
        img= ImageTk.PhotoImage(Image.open(self.pers[5]).resize((70, 80), Image.ANTIALIAS))
        lab= tk.Label(self.form, image= img)
        lab.image= img
        lab.grid(row= 0, columnspan= 2, pady= (10, 0))
        # Filling the information frame
        for label in self.labels:
            if self.labels.index(label) % 2:    # If it is a content
                if self.labels.index(label) == 9: # Last label
                    tk.Label(self.form, text= label, justify= tk.LEFT).grid(row= self.labels.index(label) + 1, column= 1, padx= (10, 5), pady= (0, 10), sticky= tk.W)
                else:   # Not last label
                    tk.Label(self.form, text= label, justify= tk.LEFT).grid(row= self.labels.index(label) + 1, column= 1, padx= (10, 5), sticky= tk.W)
            else:   # If it is a title
                if self.labels.index(label) == 0:   # First label
                    tk.Label(self.form, text= label, font= 'Arial 9 bold', justify= tk.LEFT).grid(row= self.labels.index(label) + 1, column= 1, padx= 5, pady= (10, 0), sticky= tk.W)
                else:   # Middle labels
                    tk.Label(self.form, text= label, font= 'Arial 9 bold', justify= tk.LEFT).grid(row= self.labels.index(label) + 1, column= 1, padx= 5, sticky= tk.W)
        
        # Slice self.pers to the only necessary thing: [SALARY AMOUNT, QUOTA] + [id of the person]
        self.pers= self.pers[3:5] + (emp,)
        
        self.form.pack(padx= (10, 5), pady= 10, side= tk.LEFT, expand= 1, fill= 'y')    # Packing the whole information frame on the left
        
        # Form input
        self.form= Form(self,
                        lList= ([]),   # lList is not yet specified
                        iFPad= ((0, 0,),(0, 0),))
                        
        # Creating the input lists
        self.form.iList['du:']= DateEntry(self.form.iFrame, label= 'du:', default= firstDayOfMonth())   # Starting date
        self.form.iList['au:']= DateEntry(self.form.iFrame, label= 'au:', default= today())   # Ending date
        self.form.iList['wHour']= Input(self.form.iFrame, label= 'Heures de travail:', width= 7, needed= 1) # Worked hours
        self.form.iList['deduction']= Input(self.form.iFrame, label= 'Retenues (%):', width= 5, needed= 1) # Deduction
        self.form.iList['lib']= Input(self.form.iFrame, label= 'Libellé du paiement:', width= 20, needed= 1)    # Label of the paiment
        
        # Placing the elements
        tk.Label(self.form.iFrame, text= 'Période', font='Arial 9 bold').grid(row= 0, column= 1, sticky= tk.W, padx= 5, pady= (10, 0))  # Title for the period
        self.form.placeInputs(start= 2, iNames= ('du:', 'au:',), padx= (10, 3), pady= (5, 5,), spans= (1, 1,)) # The date inputs have a greater margin from the left
        self.form.placeInputs(start= 4, iNames= ('wHour', 'deduction', 'lib',), padx= (5, 3), pady= (5, 5,), spans= (1, 1, 1,)) # The rests are aligned with the period label
        
        # Button placing
        self.form.placeButtons(labels= ('Payer',), colors= (['green','#ffffff'],),
                               anchor= tk.CENTER, side= tk.BOTTOM, fPad= (10, 10))
        # Buttons configuration
        self.form.bList['Payer'].config(command= self.pay)  # Payments
        
        # Relief configuration for the form frame
        self.form.config(relief= tk.GROOVE, bd= 2)
        
        # Mask configuration
        self.form.iList['wHour'].mask= MASKS['number']
        self.form.iList['deduction'].mask= MASKS['number']
        
        self.form.pack(side= tk.LEFT, pady= 10, padx= (5, 10), anchor= tk.N, expand= 1, fill= 'both')   # Oacking it next to the information frame
        
        # Events bindings about the link order of the inputs using Return key
        self.form.iList['wHour'].bind('<Return>', self.form.iList['deduction'].enter)
        self.form.iList['deduction'].bind('<Return>', self.form.iList['lib'].enter)
        self.form.iList['lib'].bind('<Return>', self.pay)
        
        # If sal is not None then it's for viewing informations
        if sal != None:
            con, cur= connect()
            # Getting the salary details    [beginning date, ending date, payment date, worked hours, deduction, majoration, payment label]
            salaryDetail= cur.execute('''SELECT bDate, eDate, pDate, sAmount, wHour, fisc, maj, lib FROM Salaries WHERE idSal= %d''' %(sal)).fetchone()
            # Close the db after querying the informations
            cur.close()
            con.close()
            
            # Setting default values in the Form and disable them
            self.form.iList['du:'].config(default= salaryDetail[0], state= "disabled")
            self.form.iList['au:'].config(default= salaryDetail[1], state= "disabled")
            self.form.iList['wHour'].insert(tk.END, salaryDetail[4])
            self.form.iList['deduction'].insert(tk.END, salaryDetail[5])
            self.form.iList['lib'].insert(tk.END, salaryDetail[7])
            
            # Disable all the inputs
            self.form.iList['wHour'].config(state= "disabled")
            self.form.iList['deduction'].config(state= "disabled")
            self.form.iList['lib'].config(state= "disabled")
            
            # Take out the pay button
            self.form.bList['Payer'].pack_forget()
            
            # Inserting new elements
            if salaryDetail[6] > 0: # Majoration informations
                tk.Label(self.form.iFrame, text= 'Heures\nsupplémentaires:', font= 'Arial 9 bold',
                         justify= tk.LEFT).grid(row= 8, column= 1, sticky= tk.W, padx= 5, pady= (5, 0),)   # Overtime label
                tk.Label(self.form.iFrame, text= '%.2f h à %.2f %s' %(float(salaryDetail[4] - dateDiff(salaryDetail[0], salaryDetail[1]) * self.pers[1] / 7),
                                                                      float(salaryDetail[6]), "%"
                                                                     )
                        ).grid(row= 8, column= 2, sticky= tk.W)   # Overtime informations (hours and majoration percentage)
            
            tk.Label(self.form.iFrame, text= 'Salaire net: %.2f' %(salaryCalc(salaryDetail[3], float(self.pers[1]), salaryDetail[4],
                                                                   salaryDetail[0], salaryDetail[1], salaryDetail[5], salaryDetail[6])),
                     font= 'Calibri 13 bold', relief= tk.RIDGE, bd= 3
                    ).grid(row= 9, column= 1, columnspan= 2, pady= (10, 0)) # Net paid salary
            tk.Label(self.form.iFrame, text= 'Payé le %s' %(fullDate(salaryDetail[2])), font= 'Arial 9 bold').grid(row= 10, column= 1, columnspan= 2, pady= (10, 0))  # Payment date
            
        # Last configuration
        self.grab_set() # Grabbing sets (focus)
        centralize(self)    # Centralization
        self.form.iList['wHour'].enter()    # Enter the first input by default
        self.mainloop() # Mainloop
        self.destroy()  # Destroy when quitting the mainloop
        return
    #######################################################################################################################################################################################################
    def verify(self):
        "Verification method"
        # First verify the 2 inputs
        isSet= 1
        # Date coherence check
        if (self.form.iList['au:'].getDate() - self.form.iList['du:'].getDate() < 0):
            borderColor(self.form.iList['du:'], 'red')
            borderColor(self.form.iList['au:'], 'red')
            isSet= 0
        else:
            borderColor(self.form.iList['du:'])
            borderColor(self.form.iList['au:'])
        
        isSet*= self.form.verify() 
        if isSet:
            # Database verification if the salary is already paid
            con, cur= connect()
            date_interval= cur.execute('''SELECT bDate, eDate FROM Salaries WHERE
                                          Emp = {2} AND ({0} BETWEEN bDate AND eDate OR {1} BETWEEN bDate AND eDate)'''.format(
                                                                                                                              self.form.iList['du:'].getDate(),
                                                                                                                              self.form.iList['au:'].getDate(),
                                                                                                                              self.pers[2])
                                      ).fetchone()
            # Close the connection
            cur.close()
            con.close()
            if date_interval != None:   # If the date already exists
                # Error message
                messagebox.showerror('Easy Pay', 'Le salaire du {0} au {1} a déjà été payé'.format(fullDate(date_interval[0]), fullDate(date_interval[1])))
                isSet= 0
        return isSet
    #######################################################################################################################################################################################################
    def pay(self, event= None):
        "Payment method"
        # First check the inputs
        maj= '' # Majorations
        
        if self.verify():   # Verification
            # Calculate the date differences between beginning date and ending date
            date_diff= dateDiff(self.form.iList['du:'].getDate(), self.form.iList['au:'].getDate())
            salary= None    # Reset salary
            
            # If date_diff < 20, ask before continuing, else continue
            if date_diff >= 20 or date_diff < 20 and messagebox.askyesno('Easy Pay', 'Voulez-vous payer {} jour(s) de travail'.format(date_diff)):  # If the employee want to take a salary before 20 days
                self.grab_set() # grab focus
                # If there is any accordable majoration
                if float(self.form.iList['wHour'].get()) > date_diff * float(self.pers[1]) / 7:    # Date_diff * quota / 7 would give the average normal working hour
                    maj= simpledialog.askfloat('Easy Pay', '%s heures supplémentaires (%.2f h)' %('%', float(self.form.iList['wHour'].get()) - date_diff * self.pers[1] / 7))
                    if maj != None: # Calculate the salary if it when if the person did not quit the majoration toplevel and entered a valid floating point value
                        salary= salaryCalc(self.pers[0], self.pers[1], float(self.form.iList['wHour'].get()),
                                           self.form.iList['du:'].getDate(), self.form.iList['au:'].getDate(), float(self.form.iList['deduction'].get()),
                                           maj= maj)
                    self.grab_set() # grab focus
                else:   # else with no majoration at all
                    salary= salaryCalc(self.pers[0], self.pers[1], float(self.form.iList['wHour'].get()),
                                       self.form.iList['du:'].getDate(), self.form.iList['au:'].getDate(), float(self.form.iList['deduction'].get())
                                      )
                    maj= 0  # Maj receive 0 in the case of no majoration
            
            # Data insertion
            if salary != None:
                con, cur= connect() # Connection creating
                # Get current date in int format
                date_diff= today()
                # Query cast
                req= '''INSERT INTO Salaries(bDate, eDate, pDate, sAmount, Emp, wHour, fisc, lib, maj)
                        VALUES (%d, %d, %d, %f, %d, %f, %f, "%s", %f)'''%(
                                                                           self.form.iList['du:'].getDate(),
                                                                           self.form.iList['au:'].getDate(),
                                                                           date_diff,
                                                                           self.pers[0],
                                                                           self.pers[2],
                                                                           float(self.form.iList['wHour'].get()),
                                                                           float(self.form.iList['deduction'].get()),
                                                                           self.form.iList['lib'].get(),
                                                                           float(maj)
                                                                           )
                cur.execute(req) # Query execution
                self.withdraw() # Withdraw the window before confirmation
                if messagebox.askyesno('Easy Pay', 'Payer la somme de %.2f?' %(salary)): # Confirm before committing it to the database
                    con.commit()
                    try:
                        self.master.master.master.master.frames[1].update()  # Update the salary frame if the app is included in a MainApp object
                    except:
                        ...
                    self.quit() # Quit the main loop
                    messagebox.showinfo('Easy Pay', 'Paiement enregistré avec succès') # Success message
                else:
                    self.deiconify()    # Deiconify the window
                    self.grab_set() # Grab the focus if the user did not confirm
                    self.form.iList['wHour'].enter()    # Try to enter the first input by default
                # Close the db properly
                cur.close()
                con.close()
            return
    #######################################################################################################################################################################################################
if __name__ == '__main__':
    fen= tk.Tk()
    EmployeeForm(fen)
    fen.mainloop()