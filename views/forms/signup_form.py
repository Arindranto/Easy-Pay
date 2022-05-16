# -*- coding: Utf-8 -*-
# Sign up window
import tkinter as tk
from tkinter import messagebox
# Models
from models.database_basics import connect, insertInto
# Utilities
from utils.crypto import crypt
# View
from views.form_module import centralize, Form, MonoTL, borderColor, MASKS

#########################################################################################################################################
class SignUp(MonoTL):
    "Sign up form: we use grid placement method"
    def __init__(self, boss= None):
        "Constructor"
        MonoTL.__init__(self, boss, title= "Easy Pay")   # Parent class instanciation 
        self.resizable(False, False)    # Make it unresizable
        self.withdraw()
        
        try:    # Icon placing
            self.iconbitmap('icons/person.ico')
        except:
            pass
            
        # Company form
        self.fUser= Form(self,
                         lList= (['Nom', 20],
                         ['Adresse', 20],
                         ['Pseudo', 20],
                         ['Mot de passe', 20],
                         ['Confirmez', 20],),
                         iFPad= ((15, 5), (10, 0))
                         )
        # Admin form
        self.fBio= Form(self,
                        lList= (['Nom', 20],
                        ['Prénom', 20],
                        ['Adresse', 20],
                        ['Email', 20],
                        ['Téléphone', 15],),
                        #iPad= (5, (5, 3)),
                        iFPad= ((5, 15), (10, 0))
                        )
        # Title part
        tk.Label(self, text= 'Inscription', font= 'Arial 18 bold', fg= 'blue').grid(row= 0, column= 0, columnspan= 2, pady= (10, 0))
        # Title for each forms
        tk.Label(self.fUser.iFrame, text= "ENTREPRISE", font= 'Arial 11 bold').grid(row= 0, column= 1, columnspan= 2, padx= 20, pady= (5, 0))
        tk.Label(self.fBio.iFrame, text= "ADMINISTRATEUR", font= 'Arial 11 bold').grid(row= 0, column= 1, columnspan= 2, padx= 20, pady= (5, 0))
        
        # Hide the password in confirm password input
        self.fUser.iList['Confirmez']['show']= '\u25cf'
        # Checkbutton for showing and hiding the passwords
        tk.Checkbutton(self.fUser.iFrame, text= "Afficher le mot de passe", command= self.showPasses).grid(row= 6, column= 2)

        # Placing the inputs 
        # Company form
        self.fUser.placeInputs(iNames= ('Nom', 'Adresse', 'Pseudo', 'Mot de passe', 'Confirmez',),
                              padx= (10, 5), pady= (10, 5),
                              spans= (1, 1, 1, 1, 1,)
                              )
        # Admin form
        self.fBio.placeInputs(iNames= ('Nom', 'Prénom', 'Adresse', 'Email', 'Téléphone',),
                              padx= (10, 5), pady= (10, 5),
                              spans= (1, 1, 1, 1, 1,)
                              )
        # Styling the Frame
        self.fBio.iFrame.config(bd= 2, relief= tk.GROOVE)
        self.fUser.iFrame.config(bd= 2, relief= tk.GROOVE)
        # Button configuration
        self.fBio.placeButtons(labels= ('Vider', 'Valider'),
                          colors= (['light grey', 'black'], ['green', 'white'],),
                          side= 'right',
                          bPad= ((5, 5), 5),
                          fPad= (10, (0, 0)))
        # Commands
        self.fBio.bList['Valider'].config(command= self.check)
        self.fBio.bList['Vider'].config(command= self.reset)
        # Placing the frames
        self.fUser.grid(row= 1, column= 0,  sticky= tk.N + tk.S)
        self.fBio.grid(row= 1, column= 1, sticky= tk.N)
        
        # Error message label
        self.errMess= tk.StringVar()
        tk.Label(self, textvariable= self.errMess, fg= 'red', font= 'Arial 10 bold').grid(row= 2, column= 0, columnspan= 2, pady= (0, 10))

        # Other binds
        self.fUser.iList['Confirmez'].bind('<Return>', self.fBio.iList['Nom'].enter)
        self.fBio.iList['Téléphone'].bind('<Return>', self.check)   # Last input to check method
        
        # Inputs regexes
        self.fBio.iList['Email'].mask= MASKS['email']    # Email check
        self.fBio.iList['Téléphone'].mask= MASKS['phone']    # Phone number check
        # Adresses
        self.fBio.iList['Adresse'].mask= MASKS['alphanum']
        self.fUser.iList['Adresse'].mask= MASKS['alphanum']
        
        self.fUser.iList['Nom'].focus_set() # Set the focus to the first input

        self.deiconify()    # Deiconify it to take the focus when all things are ready
        centralize(self) # Make it in the center
        self.mainloop() # Start in a main loop immediately
        try:
            self.destroy()  # Destroy after quitting the main loop
        except:
            ...
        return
    ##########################################################################################################################################
    def showPasses(self, event= None):
        "To show passwords in both the password and the confirm password input"
        self.fUser.iList['Mot de passe'].showPass()
        self.fUser.iList['Confirmez'].showPass()
        return
    ##########################################################################################################################################
    def checkPasses(self):
        "Check the equality of the two inputs"
        if self.fUser.iList['Mot de passe'].get() != '' and self.fUser.iList['Mot de passe'].get() != self.fUser.iList['Confirmez'].get():
            # Make the inputs red when wrong
            borderColor(self.fUser.iList['Mot de passe'], 'red')
            borderColor(self.fUser.iList['Confirmez'], 'red')
            # Set error message
            self.errMess.set('Vous avez entré deux valeurs différentes')
            return 0
        return 1
    ##########################################################################################################################################
    def check(self, event= None):
        "To check and validate the sign up form"
        filled= self.fUser.verify() * self.fBio.verify()
        if filled:
            # Check if the Password and Confirm password has the same values
            if self.checkPasses():
                etp= crypt(self.fUser.iList['Pseudo'].get())  # Crypt the username
                pw= crypt(self.fUser.iList['Mot de passe'].get())   # Crypt the password
                
                # Db connection
                con, cur= connect()
                # fUser values (company informations)
                insertInto(cur, 'Companies', ('uName', 'cName', 'cAdr', 'pass',),
                            (etp, self.fUser.iList['Nom'].get().title(), self.fUser.iList['Adresse'].get().title(), pw)
                            )
                # fBio values
                insertInto(cur, 'Persons', ('idPers', 'pLast', 'pFirst', 'pAdr', 'pEmail', 'pPhone', 'Fun',),
                            (
                              0,
                              self.fBio.iList['Nom'].get().title(),
                              self.fBio.iList['Prénom'].get().title(),
                              self.fBio.iList['Adresse'].get().title(),
                              self.fBio.iList['Email'].get(),   # We can't lower emails
                              self.fBio.iList['Téléphone'].get(),
                              0 # __Admin__ function)
                            )
                            )
                con.commit()    # Commitment
                # Db close
                cur.close()
                con.close()
                
                self.withdraw() # Withdraw
                self.quit()  # Quit the main loop
                
                # WELCOME MESSAGE
                messagebox.showinfo('Easy Pay', "Bienvenue!")
        else:   # Invalid inputs
            self.errMess.set('Veuillez compléter les champs correctement')  # Error message
            self.after(2000, self.erase)    # Erase after 2s
        return
    ###############################################################################################################################################
    def reset(self):
        "For resetting all the inputs"
        self.fBio.reset()
        self.fUser.reset()
        return
    ###############################################################################################################################################
    def erase(self):
        "Erase the error message"
        self.errMess.set('')
        return
####################################################################################################################################################
if __name__ == '__main__':        
    base= tk.Tk()
    SignUp(base)
    base.mainloop()