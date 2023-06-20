#-*- coding: Utf-8-*-
import tkinter as tk
from views.form_module import centralize

class About(tk.Toplevel):
	"About the app"
	def __init__(self, boss= None):
		tk.Toplevel.__init__(self, boss)
		self.resizable(False, False)
		self.title("A propos...")
		container= tk.Text(self)
		text= """
			Easy Pay: Gestion de paiement des salariés pour les ETI
			Version: 1.0.0
			Développeur: Safidy Herinirina Arindranto ANDRIANTSOA
			Dernière mise à jour: 20 Juin 2023
		"""
		container.tag_configure('centered_text', justify= 'center')
		container.insert('1.0', text)
		container.tag_add('centered_text', '1.0', 'end')
		container.pack()
		container.focus_set()
		container.config(state= 'disabled')
		# self.grab_set()
		centralize(self)
		# self.mainloop()
		return