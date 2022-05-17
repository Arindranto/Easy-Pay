# -*- coding: Utf-8 -*-

# Define the app menu to allow user to control the options and get some help on how to use the app
import tkinter as tk
from views.menus.pass_config import PassConfig

##############################################################################################################################################################################
class MenuFrame(tk.Frame):
    "Menu for the easy_pay app that contains some undevelopped options yet that are kept commented until application update"
    def __init__(self, boss, **kwargs):
        tk.Frame.__init__(self, boss, **kwargs)
        # oMenu= tk.Menubutton(self, text= 'Options', font= 'Arial 9', highlightthickness= 1, highlightbackground= '#aaaaaa', height= 1)   # Option menu
        # hMenu= tk.Menubutton(self, text= 'Aide', font= 'Arial 9', highlightthickness= 1, highlightbackground= '#aaaaaa', height= 1) # Help menu 
        
        oMenu= tk.Menubutton(self, text= 'Options', relief= tk.RIDGE, font= 'Arial 9')   # Option menu
        hMenu= tk.Menubutton(self, text= 'Aide', relief= tk.RIDGE, font= 'Arial 9', state= 'disabled') # Help menu

        # Option menu consists of:
            # Change password
            # Export data
        m1= tk.Menu(oMenu, tearoff= 0)
        # m1.add_command(label= 'Sauvegarde...', command= None) # Data saving option
        
        # Cascade menu for the data backup options
        # cm= tk.Menu(m1, tearoff= 0)
        # cm.add_command(label= 'Sauvegarde locale', command= None)
        
        # ccm= tk.Menu(cm, tearoff= 0)
        # ccm.add_command(label= 'Fichier .csv', command= None, state= 'disabled')
        # ccm.add_command(label= 'Fichier .db', command= None, state= 'disabled')
        
        # cm.add_cascade(label= 'Sauvegarde locale', menu= ccm)
        # cm.add_command(label= 'Sauvegarde en ligne', command= None, state= 'disabled')
        
        # m1.add_cascade(label= 'Exporter les données', menu= cm)   # Data exportation
        
        # m1.add_command(label= 'Importer les données ', command= None, state= 'disabled')  # data importation
        
        # m1.add_separator()
        show_menu= tk.Menu(m1, tearoff= 0)  # Show or hide employees
        
        def update_empTree():
            "To update the empTree in self.master"
            self.master.master.show_active.set(self.show_active.get()) # The show_all parameter is set to 1 if we need the active employees
            self.master.master.show_inactive.set(self.show_inactive.get()) # The show_all parameter is set to 1 if we need the inactive employees
            self.master.master.refresh() # Update the trees of the MainApp object
        
        # Which employee to show or not
        self.show_inactive= tk.IntVar()
        self.show_active= tk.IntVar()
        
        # Initialize the variables
        self.show_inactive.set(0)   # Hide inactives
        self.show_active.set(1) # Show actives
        
        # Menus
        show_menu.add_checkbutton(label= 'Salariés actifs', command= update_empTree, variable= self.show_active)
        show_menu.add_checkbutton(label= 'Salariés inactifs', command= update_empTree, variable= self.show_inactive)
        
        m1.add_cascade(label= 'Afficher', menu= show_menu)  # Show or hiding employees option
        m1.add_command(label= 'Modifier le mot de passe', command= lambda arg= self.master.master.master: PassConfig(arg))   # Password changing option
        
        m1.add_separator()
        
        m1.add_command(label= 'Quitter', command= self.master.master.ask_destroy)  # Quitter la fenetre principal
        oMenu.config(menu= m1)
        
        # Help menu consists of:
            # Using tips
            # About the developper
        # def say_hi():
            # print('Hi')
        # m1= tk.Menu(hMenu, tearoff= 0)
        # m1.add_command(label= 'Utilisation', command= say_hi, state= 'disabled')
        # m1.add_command(label= 'A propos...', command= say_hi, state= 'disabled')
        
        # hMenu.config(menu= m1)
        # m1.add_command(label= 'Sauvegarde...', command= None)
        
        # Packing the menus
        oMenu.pack(side= tk.LEFT)
        hMenu.pack(side= tk.LEFT)
###########################################################################################################################################################################