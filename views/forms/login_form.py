# -*- coding: Utf-8 -*-
# Authentication window
import tkinter as tk
from tkinter import messagebox
# Models
from models.database_basics import connect, selectFrom
# Utilities
from utils.crypto import crypt  # To decrypt the datas in the database
# Views
from views.form_module import centralize, Form, MonoTL

#########################################################################################################################################################
class Login(MonoTL):
    "Login form: grid method is the basic placement method"
    def __init__(self, boss= None):
        "Constructor"
        # Parent class instanciation
        MonoTL.__init__(self, boss, title= 'Easy Pay') 
        self.withdraw() # Withdraw first
        
        try:
            self.iconbitmap('icons/lock_icon.ico')   # icon
        except:
            pass
        self.resizable(False, False)    # Make it unresizable
        
        # Title part
        tk.Label(self, text= 'Authentification', font= 'Arial 18 bold', fg= 'blue', justify= 'left').pack(side= tk.TOP,padx= 10, pady= (10, 0))
        
        # Instance variables for the input error message
        self.errMess= tk.StringVar()
        
        # Creating an InputList Frame
        self.inputs= Form(self,
                          lList= (['Pseudo', 28],['Mot de passe', 20],),
                           iFPad= (10, (0, 3)), scroll= 0
                          )
        
        # Item placing
        tk.Label(self, textvariable= self.errMess, fg= 'red', font= 'Arial 9 bold').pack(side= tk.BOTTOM)    # Error message at the bottom of the window
        self.inputs.pack(side= tk.TOP, padx= 5, pady= 5)    # The form frame
        
        # Inputs placement
        self.inputs.placeInputs(iNames= ('Pseudo', 'Mot de passe',), padx= (10, 5), pady= (10, 5), spans= (2, 1,))
        # Buttons
        self.inputs.placeButtons(labels= ('Se connecter', 'Vider'),
                                 colors= (['royal blue', 'white'],['light grey', 'black'],),
                                 bPad= ((5, 5), 5),
                                 fPad= (5, 0))
        # Input frame configuration
        self.inputs.iFrame.config(bd= 2, relief= tk.GROOVE) # Input Frame border
        
        # Add a show/hide Button to the password
        self.inputs.iList['Mot de passe'].addShowHideButton(6)
        
        # Button configurations
        self.inputs.bList['Se connecter'].config(command= self.check)   # Connection
        self.inputs.bList['Vider'].config(command= self.inputs.reset)   # Reset the inputs
        
        # Event bindings
        self.bind('<Return>', self.check)   # Check the form when return key is pressed
        
        centralize(self)    # Centralize the window
        
        self.inputs.iList['Pseudo'].focus_set() # First input takes the focus
        
        self.deiconify()    # Deiconify it when it's all ready
        self.mainloop() # Mainloop as it is called
        try:
            self.destroy()  # Destroy after quitting the mainloop
        except:
            ...
        return
    ##################################################################################################################################################################
    def check(self, event= None):
        "Check the login"
        user = crypt(self.inputs.iList['Pseudo'].get()) # Username value
        pw= crypt(self.inputs.iList['Mot de passe'].get())    # Password value
        
        if self.inputs.verify():   # Check the database if the Entries were filled properly
            # Database connection
            conn, cur= connect()
            # Querying the database
            selectFrom(cur, 'Companies', ('uName',), (['uName = ', user, 'AND'], ['pass = ', pw, ''],))
            rowCount = len(cur.fetchall())
            if (rowCount == 0): # If the user or the password is wrong
                messagebox.showerror('Erreur', 'Le pseudo ou le mot de passe est erroné')
                # Erase the datas on the inputs
                self.inputs.reset()
                self.inputs.iList['Pseudo'].enter() # the first input gets the focus again
            else:
                #####################
                ### OPEN MAIN APP ###
                #####################
                self.quit()  # Destroy it when logged successfully
        else:
            self.errMess.set('Veuillez remplir correctement tous les champs')   # Error message if it's not filled correctly
            self.after(2000, self.suppr)    # Wait 2s then delete the message
    #####################################################################################################################################################################
    def suppr(self):
        "Delete the error message and recolor the Inputs border"
        self.errMess.set('')    # errMess reseting
##########################################################################################################################################################################