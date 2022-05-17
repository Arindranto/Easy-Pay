# -*- coding: Utf-8 -*-
# Basic classes and functions to make Forms
import tkinter as tk    # User interface
import re   # For regexes
from tkinter import ttk     # For additional user interfaces
from utils.converter import toNDigits
from utils.app_state import read, create  # app state checking
from utils.date_module import *   # Implemented date module


########################################################################################################################################################################
###################
#### CONSTANTS ####
###################

# For regex masks
MASKS= {'date': '[0-9]{1,2}[/.-]{1,1}[0-9]{1,2}[/.-]{1,1}[0-9]{2,4}',
        'email': '[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}',
        'alphanum': '[A-Za-z0-9\s]+',
        'phone': '\+{0,1}[0-9]{3,13}',
        'integer': '[0-9]+',
        'number': '[0-9.]+'}
####################################################################################################################################################################

####################
#### FUNCTIONS #####
####################
def centralize(container):
    "Centralize a container"
    # Get the current screen dimensions
    sw= container.winfo_screenwidth()
    sh= container.winfo_screenheight()
    tk.Tk.update(container) # We always need to update to get the actual values of the widget
    # Get the widget dimensions
    cw= container.winfo_width()
    ch=  container.winfo_height()
    
    # Change the geometry of the widget
    container.geometry("%s" %('+' + str(sw//2 - (cw//2))) + '+' + str(sh//2 - (ch//2)))
    return
    
####################################################################################################################################################################
def borderColor(widget, color= 'grey90'):
    "Setting an Entry border color to a given color"
    widget.config(highlightcolor= color, highlightbackground= color)
    return

#################################
#### FORM AND WINDOW CLASSES ####
#################################
####################################################################################################################################################################
class Input(tk.Entry):
    "Input box with labels to ease label/input creation"
    def __init__(self, boss= None, label= 'Label here', width= 20, needed= 0, **options):
        "Constructor"
        tk.Entry.__init__(self, boss, width= width, highlightthickness= 1)    # Input class is derived from tkinter Entry class
        
        # The label
        self.label= tk.Label(self.master, highlightcolor= 'black', highlightbackground= 'black', text= label, font= 'Arial 9 bold', justify= tk.LEFT, anchor= tk.W)
        
        borderColor(self)   # Set default border color
        
        self.needed= needed # When the input is needed
        self.mask= None # To determine a format for the input
        
        if (label.lower() == 'mot de passe'):   # Password are by default hidden ("mot de passe" in French)
            self.config(show= '\u25CF') # u25CF is the code for circles in place of words
    ##################################################################################################################################################################
    def place(self, row= 1, col= 2, padx= (10, 5) ,pady= 3, span= 1):
        "Placing the items with grid method because Labels and Entry need to be side by side"
        # Store the positions informations
        self.row= row
        self.col= col
        self.padx= padx
        self.pady= pady
        self.span= span
        
        self.label.grid(row= row, column= col - 1, sticky= tk.W, padx= (padx[0], padx[1]), pady= pady)  # First element of padx= side pad
                                                                                                        # Second element is middle pad
        self.label.bind('<Button-1>', self.enter)   # Enter the input when label is clicked
        # Place the Entry object
        self.grid(row= row, column= col, sticky= tk.W, padx= (0, padx[0]), pady= pady, columnspan= span)
        return
    ##################################################################################################################################################################
    def addShowHideButton(self, width= 15):
        "If we want a Button for hide/show password"
        bFrame= tk.Frame(self.master, bg= 'red')  # To pack the Button right next to the Input
        # Replacing the Entry
        self.grid_forget()  # Remove it
        self.grid(row= self.row, column= self.col, sticky= tk.W, padx= 0, pady= self.pady, columnspan= self.span)   # Replace it
        
        self.bText= tk.StringVar()  # Button text
        self.bText.set('Montrer')  # "Montrer" by default
        
        btn= tk.Button(bFrame, textvariable= self.bText, font= 'Arial 9 bold', width= width, height= 1)
        
        # Bind it with th showPass method on mouse events (click and release)
        btn.bind('<Button-1>', self.showPass)
        btn.bind('<Button1-ButtonRelease>', self.showPass)
        
        # Packing the button and it's frame
        btn.pack(side= tk.LEFT, padx= 0)
        bFrame.grid(row= self.row, column= self.col + 1, sticky= tk.W, padx= (1, self.padx[0] + 5), pady= self.pady)    # Pack the frame for the button too
        return
    #################################################################################################################################################################    
    def showPass(self, event= None):
        "To make the password appear or hide"
        if self['show'] == '': # If it is already shown then hide it
            try:    # Set the textvariable if there is a show hide button
                self.bText.set('Montrer')
                self.config(show= '\u25CF')
            except:
                self.config(show= '\u25CF')
        else:   # Else show it
            try:    # Set the textvariable if ther is a show hide button
                self.bText.set('Cacher')
                self.config(show= '')
            except:
                self.config(show= '')
    ##################################################################################################################################################################
    def enter(self, event= None):
        "Enter the label on an event like Return key or mouse click on the label"
        try:
            self.focus_set()
        except:
            ...
        return
    #####################################################################################################################################################################
    def isVoid(self):
        "Return either the entry is void or not"
        return self.get() == ''
        
######################################################################################################################################################################
class DateEntry(tk.Frame):
    "DateEntry to ease the date entry in the app using a casted module: date_module"
    def __init__(self, boss, label= "label here", default= None, state= 'readonly'):
        "Constructor"
        tk.Frame.__init__(self, boss, highlightthickness= 1)    # Frame to contain the things
        self.label= tk.Label(self.master, text= label, font= 'Arial 9 bold', justify= tk.LEFT)
        
        # Variables for storing the date
        self.dday= tk.StringVar()   # Day
        self.dmonth= tk.StringVar() # Month
        self.dyear= tk.StringVar()  # Year
        
        if default == None:   # Set to actual date if default is not set
            default= today()
            
        # Default date setting
        self.dday.set(toNDigits(default % 10000 % 100, 2))
        self.dmonth.set(MONTHS[default % 10000 // 100 - 1])
        self.dyear.set(default // 10000)
        # The Entries
        self.day= ttk.Combobox(self, width= 2, values= DAYS, textvariable= self.dday,
                              justify= tk.RIGHT, postcommand= self.setdaynumber)   # Day
        self.month= ttk.Combobox(self, width= 5, values= MONTHS, textvariable= self.dmonth,
                                 justify= tk.RIGHT)   # Month
        self.year= ttk.Combobox(self, width= 4, values= YEARS, textvariable= self.dyear,
                                justify= tk.RIGHT)    # Year
        
        # Configure the day number when we set a new month or anew year
        self.month.bind('<<ComboboxSelected>>', self.setdaynumber)
        self.year.bind('<<ComboboxSelected>>', self.setdaynumber)
        
        # Control the state of the inputs
        self.day['state']= state
        self.month['state']= state
        self.year['state']= state
        
        # Adjust the day number at the instanciation
        self.setdaynumber() # Got thissssss!!!!!
        
        # Packing the items side by side
        self.day.pack(side= tk.LEFT)
        self.month.pack(side= tk.LEFT)
        self.year.pack(side= tk.LEFT)
        return
    #####################################################################################################################################################################################
    def setdaynumber(self, event= None):
        "Adjust the day number"
        daynumber= (31, 'February', 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        mm= MONTHS.index(self.dmonth.get())  # Get month
        yy= int(self.dyear.get())  # Year parsed into int 
        if mm == 1: # February
            # Leap year
            if (not(yy%4) and yy%100 or not(yy%400)):
                self.day['values']= DAYS[:29]
            else:   # Else
                self.day['values']= DAYS[:28]
        else:
            self.day['values']= DAYS[:daynumber[mm]]    # Set the day number according to the month
        
        limit= int(self.day['values'][-1])
        # In case the actual value exceed the allowed one, set to the limit
        if int(self.dday.get()) > limit:
            self.dday.set(limit)
        return
    #####################################################################################################################################################################################
    def place(self, row= 1, col= 2, padx= None,pady= 3, span= 1):
        "Placing the items with grid method because Labels and Entry need to be side by side"
        self.label.grid(row= row, column= col - 1, sticky= tk.W, padx= (padx[0], padx[1]), pady= pady, columnspan= span)  # First element of padx= side pad
                                                                                                                          # Second element is middle pad
        self.grid(row= row, column= col, sticky= tk.W, padx= (0, padx[0]+5), pady= pady, columnspan= span)
    ######################################################################################################################################################################################
    def config(self, **args):
        "To configure the app"
        for key in args:
            if key != 'default' and key != 'highlightcolor' and key != 'highlightbackground':    # For other keys
                self.day[key]= args[key]
                self.month[key]= args[key]
                self.year[key]= args[key]
            elif key == 'default':   # Setting the default date
                default= args['default']                
                self.dday.set(toNDigits(default % 10000 % 100, 2))
                self.dmonth.set(MONTHS[default % 10000 // 100 - 1])
                self.dyear.set(default // 10000)
            else:   # By default apply the changes to the Frame itself
                self[key] = args[key]
    ##########################################################################################################################################################################################################
    def getDate(self):
        "return the date display by the widget in yyyy-mm-dd format and the int dd+mm+yy for comparison"
        return int(self.dyear.get()) * 10000 + (int(MONTHS.index(self.dmonth.get())) + 1) * 100 + int(self.dday.get())
#########################################################################################################################################################################
class Form(tk.Frame):
    "Creating a basic input list for forms"
    def __init__(self, boss,
                 lList= (['Label', 2],), # A list of [Label, width of the Entry]
                 iFPad= (None, None),    # iFrame (padx, pady) Frame padding
                 **args # Other args given as key/value pairs
                 ):
        "Constructor"
        tk.Frame.__init__(self, boss)
        self.iFrame= tk.Frame(self)    # Input Frame
        # Instance variables
        self.nInput= len(lList)    # Input numbers
        self.iList= {}  # Inputs dictionnary
        # Paddings
        self.padx= iFPad[0]
        self.pady= iFPad[1]
        
        # We need to memorize the Inputs in the dictionnary
        for i in range(self.nInput):
            self.iList[lList[i][0]]= Input(self.iFrame, # The labels are used as the key for the Input
                              label= lList[i][0],
                              width= lList[i][1],
                              needed= 1)
                              
        # Placing listening event to the inputs to ease navigation between the Inputs
        if 'scroll' not in args:    # scroll is a parameter to allow navigation between the inputs using Return button
            for i in range (self.nInput - 1):
                self.iList[lList[i][0]].bind('<Return>', self.iList[lList[i+1][0]].enter)
        return
    ##########################################################################################################################################################################################################
    def placeInputs(self, start= 1, iNames= ('Label',), padx= (10, 5), pady= (0, 0), spans= (1,)):
        "Place the inputs into the iFrame"
        r= start
        # starting row
        s= 0    #span count
        for ipt in iNames:
            # Pady setting according to the position of the Input
            PADY= None
            if r == start:
                # For the first
                PADY= (pady[0], pady[1],)
            elif  r >= self.nInput:
                #For the really last element
                PADY=(0, pady[0],)
            elif r > 1 and r < self.nInput:
                #Mid elements
                PADY= (0, pady[1],)
                
            # Placing the input object
            self.iList[ipt].place(row= r, col= 2, padx= padx, pady= PADY, span= spans[s])
            s+= 1   # Span increment
            r+= 1   # Row increment
        self.lastInsertedRow= r # Memorize the last inserted row
        
        # Placing the iFrame after placing the inputs
        self.iFrame.pack(side= tk.TOP, padx= self.padx, pady= self.pady)
        return
    ##########################################################################################################################################################################################################
    def placeButtons(self, labels= ('Labels',),
                     colors= (('lightgrey', 'black'),),  # [bg, fg]
                     side= 'left',
                     anchor= None,
                     bPad= ((0, 0), (0,0),),  # Button (padx, pady)
                     fPad= (0, 0,)   # Frame (padx, pady)
                     ):
        "To place Buttons in the Form"
        self.bList= {}    # Create a Button dictionnary
        bFrame= tk.Frame(self)  # Place them in a Frame included in the Form
        for i, label in enumerate(labels):
            # Design the placing to have right paddings at the right places
            self.bList[label]= tk.Button(bFrame, text= label, bg= colors[i][0], fg= colors[i][1], font= 'Arial 9 bold') # Has default font
            
            # Placing it
            if i == 0:  # First Button
                self.bList[label].pack(side= tk.LEFT, padx= (bPad[0][0], bPad[0][1]), pady= bPad[1])
            if i == len(labels)-1:  # Last Button
                self.bList[label].pack(side= tk.LEFT, padx= (0, bPad[0][0]), pady= bPad[1])
            if i > 0 and i < len(labels) - 1: # Mid Buttons
                self.bList[label].pack(side= tk.LEFT, padx= (0, bPad[0][1]), pady= bPad[1])
        # Packing the button frame
        bFrame.pack(side= side, padx= fPad[0], pady= fPad[1], anchor= anchor)
        return
    ##########################################################################################################################################################################################################
    def verify(self, event= None):
        "If an Input is required, we need to check it before submit"
        valid= 1    # Variable for the validity
        for ipt in self.iList.values(): # For every Inputs in the Form
            try:
                # Check needed Inputs
                if ipt.needed:
                    if ipt.get() == '':
                        borderColor(ipt, 'red')    # Set border color to red
                        valid= 0   # Make it invalid if any required Input is omitted
                    else:
                        borderColor(ipt)    # Reset the border color if it was modified in an early attempt
                
                # Check Inputs with defined format
                if ipt.mask != None and ipt.get() != '':
                    match= re.match(ipt.mask, ipt.get())    # Match the patterns with regex module match method
                    if match == None or match.span() != (0, len(ipt.get())):    # If it doesn't match (match.span() return a tuple with the starting index end the number of character in the mathched pattern)
                        borderColor(ipt, 'red')    # Set border color to red
                        valid= 0   # Invalid
                    else:
                        borderColor(ipt)
            except:
                ...
        return valid
    ##########################################################################################################################################################################################################
    def reset(self):
        "For resetting all the inputs"
        for ipt in self.iList.values():
            try:
                ipt.delete(0, len(ipt.get()))
            except:
                ...
        return
        
##########################################################################################################################################################################################################
class TreeScroll(tk.Frame):
    "Scrollable tree view"
    def __init__(self, boss= None, height= 120, width= 150, colList= ('Columns',)):
        "Initialization"
        tk.Frame.__init__(self, boss, height= height, width= width)
        # Treeview creating
        self.tree= ttk.Treeview(self, columns= colList, selectmode= 'browse', height= 10, show= 'headings')
        self.tree.column('#0', width= 0, stretch= tk.NO)    # Make the ghost column unseen
        for col in colList: # column and heading definitions
            self.tree.heading(col, text= col, anchor= tk.W)
            self.tree.column(col, minwidth= 25, anchor= tk.W, width= 120)
        # scrollbar
        scroll= tk.Scrollbar(self, orient= 'vertical', command= self.tree.yview, width= 15)
        self.tree['yscrollcommand']= scroll.set
        
        # Placing them
        self.tree.grid(row= 0, column= 0, padx= 1, sticky= tk.N+tk.S+tk.W+tk.E)
        scroll.grid(row= 0, column= 1, sticky= tk.N+tk.S)
        
        # Configure the stretching of the tree
        self.grid_columnconfigure(self.tree, weight= 1)
        self.grid_rowconfigure(self.tree, weight= 1)
        return
        
##########################################################################################################################################################################################################
class MonoTL(tk.Toplevel):
    "Toplevels with withdrawed masters"
    def __init__(self, boss, title= 'Title'):
        tk.Toplevel.__init__(self, boss, takefocus= 1)
        self.title(title)
        self.protocol('WM_DELETE_WINDOW', self.quitIt)   # On quitting the program
        return
    ##########################################################################################################################################################################################################
    def quitIt(self):
        "To quit the withdrawed master object for Toplevels"
        state= read()   # Read current state to get the informations
        create(state[0], 0) # Create a new file based on the app state and set the oppen app application to 0
        
        # Destroying the master implicitly destroy the toplevel
        try:
            self.master._destroy()  # For the particular main app object
        except:
            self.master.destroy()
        return
##########################################################################################################################################################################################################
if __name__ == '__main__':
    fen= tk.Tk()
    if askyesno(fen):
        fen.destroy()
    fen.mainloop()