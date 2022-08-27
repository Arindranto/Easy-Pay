# -*- coding: Utf-8 -*-
# Salary frame class definition
import tkinter as tk
from tkinter import ttk
# Model
from models.database import getSalaryId
# Utilities
from utils.calculator import isPositive
from utils.date_module import dateDiff, fullDate, today, dateToInt, firstDayOfMonth
from utils.thread_module import QueryThread
# Views
from views.form_module import TreeScroll, DateEntry
from views.forms.payment_form import PayForm


####################################################################################################################################################
class SalaryFrame(tk.Frame):
    "Will be displayed in the notebook"
    def __init__(self, boss):
        "Constructor"
        tk.Frame.__init__(self, boss)
        self.blue= None # QueryThread
        self.boss= boss
        self.pg= tk.IntVar()    # To see at which page we are
        self.pg.set(1)
        def generate_update(event= None):
            "Generate the update everytime a date is selected"
            self.pg.set(1)
            self.bDate.setdaynumber()
            self.eDate.setdaynumber()
            self.update()
        def pageUp():
            "Page up"
            # Verify the pagination if there is still records left to display
            if int(self.pg.get()) * 35 < int(self.count.get().split()[0]):
                self.pg.set(self.pg.get() + 1)
                self.update()
        def pageDown():
            "Page down"
            if self.pg.get() > 1:
                self.pg.set(self.pg.get() - 1)
                self.update()
        # Variable for the query
        self.order= tk.StringVar() # The order asc or desc
        self.count= tk.StringVar() # To count the results
        self.order.set('ASC')    # ASC by default for the order thing
        self.salTree= TreeScroll(self, colList= ('Matricule', 'Période', 'Somme', 'Date de paiement'))
        
        # Configuration for the columns
        self.salTree.tree.column('Période', width= 100,anchor= tk.CENTER)
        self.salTree.tree.heading('Période', anchor= tk.CENTER)
        self.salTree.tree.column('Date de paiement', width= 100,anchor= tk.CENTER)
        self.salTree.tree.heading('Date de paiement', anchor= tk.CENTER)
        self.salTree.tree.column('Matricule', width= 100 ,anchor= tk.CENTER)
        self.salTree.tree.heading('Matricule', anchor= tk.CENTER)
        self.salTree.tree.column('Somme', width= 100 ,anchor= tk.E)
        self.salTree.tree.heading('Somme', anchor= tk.E)
        
        sortby= tk.Frame(self)  # Will contain the sorting options
        
        tk.Label(sortby, text= 'Paiments du:').pack(side= tk.LEFT) # Beginning date
        self.bDate= DateEntry(sortby, default= firstDayOfMonth()) # Date Entry set at the first day of the month
        self.bDate.pack(side= tk.LEFT)
        tk.Label(sortby, text= 'au:').pack(side= tk.LEFT, padx= (10, 0))    # Ending date
        self.eDate= DateEntry(sortby, default= today() + 31)  # Date Entry set at the last day of the current month
        self.eDate.pack(side= tk.LEFT)
        self.search= tk.Entry(sortby, width= 13)    # Search entry
        tk.Button(sortby, text= 'Rechercher', command= generate_update).pack(side= tk.RIGHT, padx= (2, 5))  #  Search button
        self.search.pack(side= tk.RIGHT)
        # Sort order radios
        tk.Radiobutton(sortby, text= 'Ascendante', variable= self.order, value= 'ASC', command= generate_update).pack(side= tk.LEFT, padx= (10, 0))
        tk.Radiobutton(sortby, text= 'Descendante', variable= self.order, value= 'DESC', command= generate_update).pack(side= tk.LEFT)
        
        # Binding the date entries to the update method
        self.bDate.day.bind('<<ComboboxSelected>>', generate_update)
        self.eDate.day.bind('<<ComboboxSelected>>', generate_update)
        self.bDate.month.bind('<<ComboboxSelected>>', generate_update)
        self.eDate.month.bind('<<ComboboxSelected>>', generate_update)
        self.bDate.year.bind('<<ComboboxSelected>>', generate_update)
        self.eDate.year.bind('<<ComboboxSelected>>', generate_update)
        # Binding the tree to the double click
        self.salTree.tree.bind('<Double-Button-1>', self.payDetail)
        self.salTree.tree.bind('<Return>', self.payDetail)
        # Search binding
        self.search.bind('<Return>', generate_update)
        
        sortby.grid(padx=(5, 15), pady= 10, sticky= tk.E + tk.W) # Pack them
        sortby= tk.Frame(self) # Redefine it as a new fram variable to economize variables
    
        # View payment details Button
        tk.Button(sortby,
                  text= 'Détails', font= 'Arial 9 bold',
                  command= self.payDetail
                 ).pack(side= tk.LEFT, anchor= tk.W, padx= 5, pady= 0)
        bButtons= tk.Frame(sortby) # Pagination frame
        
        # Pagination buttons and label
        tk.Button(bButtons,
                  text= '<<', font= (None, 9, 'bold'), command= pageDown).grid(row= 0, column= 1)
        tk.Label(bButtons, textvariable= self.pg).grid(row= 0, column= 2)
        tk.Button(bButtons,
                  text= '>>', font= 'None 9 bold', command= pageUp
                 ).grid(row= 0, column= 3)
                  
        self.progress= ttk.Progressbar(bButtons, length= 175, maximum= 100) # The progress bar
        self.progress.grid(row= 0, column= 5, sticky= tk.W, padx= 20)
        
        tk.Label(bButtons, textvariable= self.count, font= 'Arial 10 bold').grid(row= 0, column= 6, padx= 20, sticky= tk.W) # The result count label
        
        bButtons.pack(side= tk.LEFT, expand= 1, fill= 'x', anchor= tk.CENTER, padx= 138)    # Align the buttons properly
        
        # Search entry
        generate_update()    # Start by updating
        
        self.salTree.grid(sticky= tk.N+tk.S+tk.E+tk.W, padx= 5)    # Packing the tree
        sortby.grid(sticky= tk.W+tk.E, padx= 5, pady= 10) # Packing the button frame
        
        # Make the Treeview stretch
        self.grid_columnconfigure(self.salTree, weight= 1)
        self.grid_rowconfigure(self.salTree, weight= 1)
        return
    ###############################################################################################################################################
    def payDetail(self, event= None):
        "The payment detail"
        try:    # Try to get the information about the payment if one is selected
            period= self.salTree.tree.item(self.salTree.tree.focus(), 'values')[1]   # Save the period that is in the second column
            period= period.split(' au ')    # Split it to get the 2 dates
            matricule= self.salTree.tree.item(self.salTree.tree.focus(), 'values')[0]
            salId= getSalaryId(dateToInt(period[0]), dateToInt(period[1]), matricule)    # Get empId and salId at once
            # Showing the employee card
            PayForm(self, emp= salId[0], sal= salId[1])
        except:
            ...
        self.mainloop() # Retake the main loop
        return
    ###################################################################################################################################################
    def update(self, event= None):
        "Inserts the data in the tree"
        # Delete all
        for element in self.salTree.tree.get_children():
            self.salTree.tree.delete(element)
        self.progress.start(10) # Start the progress bar
        # Query cast
        req= '''SELECT
                fPrefix || "-" || num,
                FULL_DATE(bDate, 2) || " au " || FULL_DATE(eDate, 2),
                ROUND(sAmount/(quota * 4.0) * (wHour - TO_UNSIGNED(wHour - DATE_DIFF(bDate, eDate) * quota/7.0) * (1 - maj/100.0)) * (1 - fisc/100.0), 2),
                FULL_DATE(pDate), isInactive, cEnd FROM Salaries JOIN Persons ON Emp = idPers JOIN Functions ON Fun = idFun WHERE pDate BETWEEN %d AND %d ''' %(self.bDate.getDate(), self.eDate.getDate())
        # Filter
        if self.search.get() != '':
            # If the search field is not blank
            req+= ''' AND fPrefix || "-" || num LIKE "%s" ''' %(self.search.get())
        try:    # If the frame is in an app having an option that allow shoing inactive employees
            if self.master.master.master.show_inactive.get() == 0:  # Don't show inactive employees
                req+= ''' AND isInactive= 0 '''
            if self.master.master.master.show_active.get() == 0:    # Don't show active employees
                req+= ''' AND isInactive= 1 '''
        except:
            ...
        
        # If the counter need to be changed
        if self.pg.get() == 1:
            self.counter= QueryThread(query= req[:7] + 'COUNT(idSal)' + req[322:])  # Counter thread
            self.counter.start()
            self.setCounter()   # Query checker

        self.blue= QueryThread(query= req + '''ORDER BY pDate %s LIMIT %d, 35''' %(self.order.get(), (self.pg.get()-1) * 35),   # Order using the pagination
                                func= (('DATE_DIFF', 2, dateDiff,), ('TO_UNSIGNED', 1, isPositive,), ('FULL_DATE', -1, fullDate),) # New functions
                              ) # Main query
        self.blue.start()
        self.insert()   # Check if the query is done
        return
    ##############################################################################################################################################################
    def insert(self):
        "Listen if the query is done and insert the results in the Treeview"
        try:
            if self.blue.done:  # Insert if the query thread has finished running is done
                # Insert the new elements
                for value in self.blue.result:
                    if value[4]: # value[4]: the isInactive column
                        self.salTree.tree.insert('', tk.END, text= '', values= value, tags= ('inactive',)) 
                    elif value[5] <= today(): # value[5]: the contract end date, compare with today's date
                        self.salTree.tree.insert('', tk.END, text= '', values= value, tags= ('overdate',))   
                    else:
                        self.salTree.tree.insert('', tk.END, text= '', values= value) 
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
    ###############################################################################################################################################################
    def setCounter(self):
        "Set the count label to the right number"
        try:
            if self.counter.done:   # Change the value of the count label
                self.count.set(str(self.counter.result[0][0]) + ' résultat(s)')
                self.counter= None  # Reset self.counter to None
                return
        except:
            ...
        self.after(100, self.setCounter) # else check again after 100 ms
    ################################################################################################################################################################