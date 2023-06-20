# -*- coding: Utf-8 -*-
# Employee frame for the main app
import tkinter as tk
from tkinter import ttk
# Models
from models.database import getFunctions, getIdByMatricule, isActive
# Utilities
from utils.converter import toNDigits
from utils.date_module import today
from utils.thread_module import QueryThread
# Views
from views.form_module import TreeScroll
from views.forms.employee_form import EmployeeForm, CORRESP
from views.forms.payment_form import PayForm

###############################################################################################################################################################################
class EmployeeFrame(tk.Frame):
    "Will be displayed in the notebook"
    def __init__(self, boss):
        "Constructor"
        tk.Frame.__init__(self, boss)
        self.blue= None # QueryThread
        self.resultCount= None # QueryThread
        self.pg= tk.IntVar()    # To see at which page we are
        self.pg.set(1)
        self.boss= boss
        # update functions
        def new_update(event= None):
            "Help update in a new page"
            self.pg.set(1)
            # Modify the order of the thing if it is in a bad order
            self.update()
            return
        def pageUp():
            "Page up"
            if int(self.pg.get()) * 35 < int(self.count.get().split()[0]):  # Check if there is still values to show
                self.pg.set(self.pg.get() + 1)
                self.update()
            return
        def pageDown():
            "Page down"
            if self.pg.get() > 1:
                self.pg.set(self.pg.get() - 1)
                self.update()
            return
        def seeFun():
            "To see the function list"
            funChoice.config(values= ['Tout'] + getFunctions())
            return
        def menu():
            "Show the menu for a selected Item"
            print('Here we go')
        # Variables for the query
        self.order= [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]    # [Function, Sorting options, Searchbar value, Sorting order]
        # Default values
        self.order[0].set('Tout') # All functions taken in charge
        self.order[1].set('Fin de contrat') # By default sort by contract end date
        self.order[2].set('')   # Search is set at a blank string
        self.order[3].set('ASC')    # ASC by default
        
        # The employee Treeview
        self.empTree= TreeScroll(self, colList= ('Matricule', 'Nom', 'Prénom(s)', 'Fonction', 'Salaire',))
        
        # Column settings
        self.empTree.tree.column('Matricule', width= 100 ,anchor= tk.CENTER)
        self.empTree.tree.heading('Matricule', anchor= tk.CENTER)
        # Center the datas
        self.empTree.tree.column('Salaire', anchor= tk.CENTER)
        self.empTree.tree.heading('Salaire', anchor= tk.CENTER)
        
        # Event bindings
        self.empTree.tree.bind('<Double-Button-1>', self.pay) # Left click
        self.empTree.tree.bind('<Return>', self.pay)	# Enter
        #self.empTree.tree.bind('<Button-3>', menu)	# Right click

        # A frame to pack the label and the combobox to sort the datas and the research entry
        sortby= tk.Frame(self)
            
        tk.Label(sortby, text= 'Fonction: ').pack(side= tk.LEFT)   # The function label
        
        funChoice= ttk.Combobox(sortby, width= 12, textvariable= self.order[0],
                                state= 'readonly', postcommand= seeFun)  # Function combobox
        # Place it immediately
        funChoice.pack(side= tk.LEFT)
        # Event binding
        funChoice.bind('<<ComboboxSelected>>', new_update)  # Update anytime the value changes
        
        tk.Label(sortby, text= 'Trier par: ').pack(side= tk.LEFT, padx= (5, 0))   # The sort by label
        
        sortChoice= ttk.Combobox(sortby, width= 15, textvariable= self.order[1],
                         values= ['Début de contrat', 'Fin de contrat', 'Etat', 'Matricule', 'Salaire', 'Nom', 'Prénoms'],
                         state= 'readonly') # Sort by combobox
        # Placing it
        sortChoice.pack(side= tk.LEFT)
        # Event binding
        sortChoice.bind('<<ComboboxSelected>>', new_update) # Update anytime the value changes
        
        # Sort order radios
        tk.Radiobutton(sortby, text= 'Ascendante', variable= self.order[3], value= 'ASC', command= new_update).pack(side= tk.LEFT, padx= (10, 0))
        tk.Radiobutton(sortby, text= 'Descendante', variable= self.order[3], value= 'DESC', command= new_update).pack(side= tk.LEFT)

        buttons= tk.Frame(self) # Will contain all the footer widgets
        # View employee information button
        tk.Button(buttons,
                  text= 'Voir informations', font= 'Arial 9 bold',
                  command= self.edit).pack(side= tk.LEFT, anchor= tk.W, padx= 5, pady= 0)
        # Pay employee button
        tk.Button(buttons,
                  text= 'Payer', font= 'Arial 9 bold',
                  command= self.pay).pack(side= tk.LEFT, anchor= tk.W, padx= 5, pady= 0)
        
        # Pagination widgets
        bButtons= tk.Frame(buttons) # The frame
        
        # The progress bar
        self.progress= ttk.Progressbar(bButtons, length= 175, maximum= 100)
        
        # Label to show the result count
        self.count= tk.StringVar()
        self.count.set('0 résultat(s)')
        tk.Label(bButtons, textvariable= self.count, font= 'Arial 10 bold').grid(padx= 20, row= 0, column= 6, sticky= tk.W)
        
        # Pack the pagination frame
        bButtons.pack(side= tk.LEFT, expand= 1, fill= 'x', anchor= tk.CENTER, padx= 25)
        # Add employee button
        
        tk.Button(buttons, bg= 'green', fg= 'white',
                  text= 'Ajouter un salarié', font= 'Arial 9 bold',
                  command= self.addEmployee).pack(side= tk.RIGHT, anchor= tk.E, padx= 15, pady= 0)
        
        # Search entry
        sortChoice= tk.Entry(sortby, textvariable= self.order[2], width= 25)    # Search entry
        sortChoice.bind('<Return>', new_update) # Event binding
        
        # Placing the rest of the elements
        # Search Entry
        tk.Button(sortby, text= 'Rechercher', command= new_update).pack(side= tk.RIGHT, padx= (2, 5))   # Search button
        sortChoice.pack(side= tk.RIGHT) # Search entry
        self.progress.grid(row= 0, column= 5, sticky= tk.W, padx= 20)   # The progress bar
        # Pagination
        tk.Button(bButtons,
                   text= '<<', font= (None, 9, 'bold'), command= pageDown).grid(row= 0, column= 1)  # Backward page
        tk.Label(bButtons, textvariable= self.pg).grid(row= 0, column= 2)   # Page indicator
        tk.Button(bButtons,
                   text= '>>', font= 'None 9 bold', command= pageUp).grid(row= 0, column= 3)    # Forward page
        
        
        sortby.grid(padx=(5, 15), pady= 10, sticky= tk.E + tk.W) # Place th frame having the sorting options
        self.empTree.grid(sticky= tk.N+tk.S+tk.E+tk.W, padx= 5)

        buttons.grid(sticky= tk.W+tk.E, padx= 5, pady= 10) # Packing the button frame
        
        # Make the Treeview stretch
        self.grid_columnconfigure(self.empTree, weight= 1)
        self.grid_rowconfigure(self.empTree, weight= 1)
        
        new_update()    # Update for the first time
        return
    ####################################################################################################################################################################
    def addEmployee(self, event= None):
        "Add employee section"
        EmployeeForm(self)  # Add the employee
        self.mainloop() # Retake the mainloop
        return
    ####################################################################################################################################################################
    def pay(self, event= None):
        "The payment section"
        try: # If a person is selected
            # We check by matricule
            matricule= self.empTree.tree.item(self.empTree.tree.focus(), 'values')[0]   # First column of the treeview
            empId= getIdByMatricule(matricule)
            if isActive(empId):
                # Showing the employee pay form
                PayForm(self, emp= empId)
        except: # else pass
            ...
        
        self.mainloop() # Retake the mainloop
        return
    ####################################################################################################################################################################
    def edit(self, event= None):
        "View employee information and potentially editing employee information"
        # try:    # If one is selcted in the treeview
            # We check by matricule
        matricule= self.empTree.tree.item(self.empTree.tree.focus(), 'values')[0]   # First column of the treeview
        empId= getIdByMatricule(matricule)
        EmployeeForm(self, emp= empId)
        # except:
        #     ...
        
        self.mainloop() # Retake the mainloop
        return
    ####################################################################################################################################################################
    def update(self, event= None):
        "Inserts the data in the tree"
        # Element deletion
        for element in self.empTree.tree.get_children():
            self.empTree.tree.delete(element)
        # Start the progress bar
        self.progress.start(10)
        
        # Query cast
        req= '''SELECT fPrefix || "-" || num, pLast, pFirst, fName, ROUND(actualSal * 1.0, 2), isInactive, cEnd FROM Functions
                JOIN Persons ON idFun = Fun WHERE '''
        # Function filter
        if self.order[0].get() != 'Tout':
            req+= '''fName = {}'''.format('"' + self.order[0].get() + '"')
        else:
            req+= '''idFun <> 0'''
        
        # Firstname or Lastname or matricule research
        if self.order[2].get() != '':
            # Creating the name to search
            name= list(self.order[2].get().split())
            name= '%' + '%'.join(name) + '%'    # More precise search according to the lastname and the firstname
            req+= ''' AND (fPrefix || "-" || num like "{0}" OR pLast || " " || pFirst LIKE "{1}")'''.format(self.order[2].get(), name)
        
        try:    # If the frame is in an app having an option that allow the choice on showing employees or not
            if self.master.master.master.show_inactive.get() == 0:  # Don't show inactive employees
                req+= ''' AND isInactive= 0 '''
            if self.master.master.master.show_active.get() == 0:    # Don't show active employees
                req+= ''' AND isInactive= 1'''
        except:
            ...
        
        # Count the result depend on the pagination
        if self.pg.get() == 1:
            self.counter= QueryThread(query= req[:7] + 'COUNT(idPers)' + req[89:])  # The query thread count the results
            self.counter.start()    # Start it
            self.setCounter()   # Listen to the change
        
        # Sort order for the main query thread
        if self.order[1].get() == 'Matricule':  # Matricule sorting require a function creation
            self.blue= QueryThread(query= req + ''' ORDER BY %s %s LIMIT %d, 35''' %(CORRESP[self.order[1].get()], self.order[3].get(), (self.pg.get() - 1) * 35),
                                   func= (('N_DIGITS', 2, toNDigits,),)
                                   )
        else:   # else
            self.blue= QueryThread(query= req + ''' ORDER BY %s %s LIMIT %d, 35''' %(CORRESP[self.order[1].get()], self.order[3].get(), (self.pg.get() - 1) * 35))
        
        self.blue.start()   # Start the thread
        self.insert()   # Check the insertion everytime
        return
    ####################################################################################################################################################################
    def insert(self):
        "Listen if the query is done and show it"
        try:
            if self.blue.done:  # Insert if the query thread has finished running is done
                # Element insertion
                for value in self.blue.result:
                    if value[5]: # value[5]: the isInactive column
                        self.empTree.tree.insert('', tk.END, text= '', values= value, tags= ('inactive',)) 
                    elif value[6] <= today(): # value[6]: the contract end date, compare with today's date
                        self.empTree.tree.insert('', tk.END, text= '', values= value, tags= ('overdate',))   
                    else:
                        self.empTree.tree.insert('', tk.END, text= '', values= value) 
                # Reset self.blue
                self.blue= None
                # Stop the progress bar
                self.progress.stop()
                # Full effect
                self.progress['value']= 100
                self.after(50, lambda arg= {'value': 0}: self.progress.config(arg))
                return
        except:
            ...
        self.after(100, self.insert) # else check again after 100 ms
    ####################################################################################################################################################################
    def setCounter(self):
        "Set the count label to the right number"
        try:
            if self.counter.done:   # Change the value of the count label
                self.count.set(str(self.counter.result[0][0]) + ' résultat(s)')
                self.counter= None  # Reset self.counter
                return
        except:
            ...
        self.after(100, self.setCounter)    # else check again after 100 ms
    ####################################################################################################################################################################