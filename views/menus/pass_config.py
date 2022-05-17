# -*- coding: Utf-8 -*-
# Password mofidying window
import tkinter as tk
from tkinter import messagebox
# Models
from models.database_basics import connect, selectFrom, update
# Utilities
from utils.crypto import crypt, decrypt
# View
from views.form_module import Form, centralize, borderColor

class PassConfig(tk.Toplevel):
	'The password modification window'
	def __init__(self, boss= None):
		tk.Toplevel.__init__(self, boss)
		# Resizing the window
		self.geometry('325x235')
		self.resizable(False, False)
		self.protocol('WM_DELETE_WINDOW', self.quit)
		self.title('Changement du mot de passe')
		# Centralization
		centralize(self)

		# The form
		'''def __init__(self, boss,
                 lList= (['Label', 2],), # A list of [Label, width of the Entry]
                 iFPad= (None, None),    # iFrame (padx, pady) Frame padding
                 **args # Other args given as key/value pairs
                 ):'''
		self.f= Form(self,
		    	(['Mot de passe actuel: ', 20], ['Nouveau mot de passe: ', 20],
		    	 ['Confirmez le nouveau\nmot de passe: ', 20],),
		    	 ((5, 5,), (10, 0,),)
		    	)
		self.f.iFrame.config(bd= 2, relief= tk.GROOVE)
		# self.f.config(bd= 2, relief= tk.SUNKEN)
		# input placing
		# self, start= 1, iNames= ('Label',), padx= (10, 5), pady= (0, 0), spans= (1,)
		self.f.placeInputs(iNames= ('Mot de passe actuel: ', 'Nouveau mot de passe: ', 'Confirmez le nouveau\nmot de passe: ',), pady= (10, 10), spans= (1, 1, 1,))
		# Input configurations to hide the password by default
		self.f.iList['Mot de passe actuel: '].config(show= '\u25cf')
		self.f.iList['Nouveau mot de passe: '].config(show= '\u25cf')
		self.f.iList['Confirmez le nouveau\nmot de passe: '].config(show= '\u25cf')
		# Make them needed
		self.f.iList['Mot de passe actuel: '].needed= 1
		self.f.iList['Nouveau mot de passe: '].needed= 1
		self.f.iList['Confirmez le nouveau\nmot de passe: '].needed= 1
		# Show password checkbutton
		self.active= tk.IntVar()
		self.active.set(0)
		tk.Checkbutton(self.f.iFrame, text= "Afficher le mot de passe", variable= self.active, command= self.showPasses).grid(row= 4, column= 1, columnspan= 2)

		# Button placing
		self.f.placeButtons(labels= ('Enregistrer',),
                     colors= (('green', 'white'),),  # [bg, fg]
                     side= 'right',
                     #anchor= None,
                     #bPad= ((10, 0), (0,0),),  # Button (padx, pady),
                     fPad= (10, (10, 0),)
                     )   # Frame (padx, pady))

		# Binding
		self.f.iList['Confirmez le nouveau\nmot de passe: '].bind('<Return>', self.set)
		# Button action controller
		self.f.bList['Enregistrer'].config(command= self.set)
		self.f.grid(row= 0, column= 0, sticky= tk.N, padx= (10, 5), pady= (10, 3))
		self.errMess= tk.Label(self, fg= 'red', font= 'Arial 10 bold')	# The error message label
		self.errMess.grid(row= 1, column= 0, sticky= tk.W+tk.E)

		# Last configs
		self.grab_set()
		self.f.iList['Mot de passe actuel: '].enter()
		self.changed= False	# To mark if the password has changed
		self.mainloop()

		# When exited then show success message
		if self.changed:
			messagebox.showinfo('Easy Pay', "Nouveau mot de passe enregistré")
		self.destroy()
	##################################################################################################################################################################################
	def showPasses(self, event= None):
		"To show passwords in both the password and the confirm password input"
		self.f.iList['Mot de passe actuel: '].showPass()
		self.f.iList['Nouveau mot de passe: '].showPass()
		self.f.iList['Confirmez le nouveau\nmot de passe: '].showPass()
		return
	###################################################################################################################################################################################
	def checkPasses(self):
		"Check the input validities"
		# Coloring the borders
		borderColor(self.f.iList['Mot de passe actuel: '])
		borderColor(self.f.iList['Nouveau mot de passe: '])
		borderColor(self.f.iList['Confirmez le nouveau\nmot de passe: '])

		# If the actual password is wrong
		pw= crypt(self.f.iList['Mot de passe actuel: '].get())    # Password value

		# Get the password in the database
		# Database connection
		conn, cur= connect()
		# Querying the database
		selectFrom(cur, 'Companies', ('pass', 'uName',), (['idCom = ', 1, ''],))
		req= cur.fetchone()	# Get the value as a tuple
		#print(decrypt(req[0]), ' ', decrypt(req[1]))
		cur.close()
		conn.close()

		# Check for empty entries
		for entry in self.f.iList.values():
			if entry.isVoid():
				borderColor(entry, 'red')
				req= False	# req will not be needed

		if not req:
			return 'Veuillez remplir les champs correctement'

		if (pw != req[0]):
			# Wrong current password
			borderColor(self.f.iList['Mot de passe actuel: '], 'red')	# Coloring the borders
			return 'Mot de passe actuel erroné'
		if self.f.iList['Nouveau mot de passe: '].get() != '' and self.f.iList['Nouveau mot de passe: '].get() != self.f.iList['Confirmez le nouveau\nmot de passe: '].get():
			# Make the inputs red when wrong
			borderColor(self.f.iList['Nouveau mot de passe: '], 'red')
			borderColor(self.f.iList['Confirmez le nouveau\nmot de passe: '], 'red')
			# Set error message
			
			return 'Vous avez entré deux valeurs différentes'
		return 'valid'
	######################################################################################################################################################################################
	def set(self, command= None):
		"Set the new password if it's validated successfully"
		msg= self.checkPasses()
		if (msg == 'valid'):
			self.withdraw()
			# Change the password
			newpass= crypt(self.f.iList['Nouveau mot de passe: '].get())	# The new password
			# Database connection
			conn, cur= connect()

			# Changes
			update(cur, 'Companies', (['pass', newpass],), (['idCom = ', 1, ''],))

			# Ask before committing
			if messagebox.askyesno('Easy pay', 'Modifier le mot de passe?'):
				conn.commit()	# Committing the changes
				# Closing the window
				self.changed= True	# Changed the password successfully
				self.quit()
			else:
				self.deiconify()	# remake it in the first plan
				self.f.iList['Mot de passe actuel: '].enter()	# Enter the first Entry
			cur.close()
			conn.close()
		else:
			# Set error message
			self.errMess.config(text= msg)

if __name__ == '__main__':
	fen= tk.Tk()	# Main window
	PassConfig(fen)
	fen.mainloop()