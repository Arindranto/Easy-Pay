# -*- coding: Utf-8 -*-
# The payment form
import tkinter as tk
from tkinter import messagebox

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