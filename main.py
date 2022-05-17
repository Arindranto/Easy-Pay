# -*-coding: Utf-8 -*-

###############################################################
##                                                           ##
##   ####         ####     ######   #######   #####    ###   ##
##   ######     ######    ###  ###    ###     ######   ###   ##
##   ###  ### ###  ###   ###    ###   ###     ### ###  ###   ##
##   ###    ###    ###   ##########   ###     ###  ### ###   ##
##   ###           ###   ###    ###   ###     ###   ######   ##
##   ###           ###   ###    ### #######   ###    #####   ##
##                                                           ##
###############################################################

import tkinter as tk
from tkinter import ttk, messagebox
# Models
from models.database_basics import connect, create, selectFrom
# Utilities
import utils.app_state as app
# Views
from views.form_module import centralize
from views.forms.login_form import Login
from views.forms.signup_form import SignUp
from views.frames.employee_frame import EmployeeFrame
from views.frames.salary_frame import SalaryFrame
from views.menus.app_menu import MenuFrame

###############################################################################################################################################################
class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)    # Instanciation
        
        self.withdraw() # Hide it at first
        self.state= app.read() # (Database path and OpenWindowCount)
        # print(self.state)
        if not self.state[1]:   # If there is no open window
            # Check the username count in the database
            # Little database check
            con, cur= connect()
             # Get the number of usernames
            selectFrom(cur, 'Companies', ('COUNT(uName)', ))
            uCount= cur.fetchone()[0]
            cur.close()
            con.close()
            
            # Indicate which employees to show
            self.show_inactive= tk.IntVar()
            self.show_active= tk.IntVar()
            self.show_inactive.set(0)
            self.show_active.set(1)
            
            # Basic configuration
            self.minsize(800, 500)  # Minsize
            self.geometry('800x500')    # Dimension
            self.title('Easy Pay')  # Title
            
            # Try the app icon
            try:
                self.iconbitmap('icons/app_icon.ico')
            except:
                ...
            
            # Some style (UNSTUDIED YET)
            style= ttk.Style()
            style.theme_use('clam')
            style.configure('Treeview', rowheight= 25, foreground= '#000000', fieldbackground= "#ffffff")
            style.configure('Treeview.Heading', font= ('Arial', 10, 'bold'))
            style.map('Treeview', background= [('selected', '#000066',)], foreground= [('selected', '#ffffff',)])
            
            frame= tk.Frame(self)   # Main container in the app
            self.menu= MenuFrame(frame, bd= 1, relief= tk.GROOVE)   # Menu
            self.nb= ttk.Notebook(frame)   # Notebook widget
            
            # Placing them
            self.menu.grid(row= 1, sticky= tk.W+tk.E, pady= (0, 5))
            self.nb.grid(row= 2, sticky= tk.N+tk.S+tk.E+tk.W, padx= 1)

            self.frames= (EmployeeFrame(self.nb), SalaryFrame(self.nb))    # The frames in the Notebook (employee and salary)
            
            # Adding frame to the notebooks
            self.nb.add(self.frames[0], text= 'Salariés')  # Employees frame
            self.nb.add(self.frames[1], text= 'Historique de paiments')  # Payments frame
            
            # Tag configuration for styling purposes
            # Inactive persons are written in red
            self.frames[0].empTree.tree.tag_configure('inactive', background= '#dd0000', foreground= '#ffffff') # For licencied employee
            self.frames[1].salTree.tree.tag_configure('inactive', background= '#dd0000', foreground= '#ffffff') # For licencied employee
            # Overdated persons are written in purple
            self.frames[0].empTree.tree.tag_configure('overdate', background= '#ff9900', foreground= '#ffffff', font= (None, 9, 'bold')) # For overdated employee
            self.frames[1].salTree.tree.tag_configure('overdate', background= '#ff9900', foreground= '#ffffff', font= (None, 9, 'bold')) # For overdated employee
            
            # Place the main frame
            frame.pack(expand= 1, fill= 'both')
            
            self.bind('<Control-u>', self.refresh)  # Updating shortcut
            
            # Make the notebook expand
            frame.grid_columnconfigure(self.nb, weight= 1)
            frame.grid_rowconfigure(self.nb, weight= 1)
            
            centralize(self)    # Centralize the app
            
            app.create(db= self.state[0], appstate= 1)   # Change the open window count
            
            if uCount == 1: # If only one username is recognized, signup form is showed
                SignUp(self)
            else:   # Else login form
                Login(self)
            try:
                self.deiconify()    # Deiconify if the user was authenticated
                # Ask before closing the app
                self.protocol('WM_DELETE_WINDOW', self.ask_destroy)
            except:
                ...
        else:   # If there is already an open window
            messagebox.showerror('', 'Une occurence de l\'application est en cours d\'exécution')
            self.destroy()
        return
    
    #####################################################################################################################################################################################################
    def refresh(self, event= None):
        "Will update the 2 treeviews of the app"
        # Pagination setting
        self.frames[0].pg.set(1)
        self.frames[1].pg.set(1)
        # Uodate the trees
        self.frames[0].update()
        self.frames[1].update()
        return

    #######################################################################################################################################################################################################
    def _destroy(self):
        "Personalized destroy method to avoid thread crashing and db blocking"
        self.withdraw() # Withdraw the window
        
        app.create(db= self.state[0], appstate= 0)   # Terminate the app_state
        
        # Join thread to avoid database bloking
        # Counter threads
        try:
            self.frames[0].counter.join()
        except:
            ...
        try:
            self.frames[1].counter.join()
        except:
            ...
        # Query threads
        try:
            self.frames[0].blue.join()
        except:
            ...
        try:
            self.frames[1].blue.join()
        except:
            ...

        self.destroy() # Destroy the window and terminate the program
    
    ####################################################################################################################################################################################################################
    def ask_destroy(self):
        "Ask before destroying the window"
        if messagebox.askyesno('Easy Pay', "Voulez-fermer l'application?"):
            app.create(db= self.state[0], appstate= 0)   # Terminate the app_state
            self.destroy()
    
#########################################################################################################################################################################################################################
# Run the main app
MainApp().mainloop()