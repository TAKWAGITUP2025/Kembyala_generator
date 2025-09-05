import tkinter as tk
from tkinter import ttk, messagebox
from kembyala.models.amount import AmountConverter
from datetime import datetime, timedelta

class DataEntryView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.amount_converter = AmountConverter()
        self.entries = {}
        self.create_widgets()
        self.initialize_default_values()
    
    def create_widgets(self):
        bank_frame = ttk.LabelFrame(self, text="Bank Information")
        bank_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(bank_frame, text="Bank Name:").grid(row=0, column=0, padx=5, pady=5)
        self.bank_name_var = tk.StringVar()
        self.bank_name_entry = ttk.Entry(bank_frame, textvariable=self.bank_name_var, width=40)
        self.bank_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        
        form_frame = ttk.LabelFrame(self, text="Kembyala Details")
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        fields = [
            ('bank_code', 'Code banque (2 chiffres):'),
            ('branch_code', 'Code agence (3 chiffres):'),
            ('account_number', 'Numéro de compte (8 chiffres):'),
            ('rib_key', 'Clé RIB (2 chiffres):'),
            ('amount_figures', 'Montant en chiffres:'),
            ('amount_words', 'Montant en lettres:'),
            ('beneficiary', 'Bénéficiaire:'),
            ('drawee', 'Tiré (personne à payer):'),
            ('place_of_issue', 'Lieu de création:'),
            ('date_of_issue', 'Date de création (YYYY-MM-DD):'),
            ('due_date', 'Date d\'échéance (YYYY-MM-DD):'),
            ('bank_address', 'Adresse bancaire:'),
            ('aval', 'Aval (garantie):'),
            ('tire_address', 'Adresse du tiré:'),
        ]
        
        for field, label in fields:
            row_frame = ttk.Frame(form_frame)
            row_frame.pack(fill=tk.X, padx=5, pady=5)
            ttk.Label(row_frame, text=label, width=25).pack(side=tk.LEFT)
            entry = ttk.Entry(row_frame, width=50)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.entries[field] = entry
        
        self.entries['amount_figures'].bind('<KeyRelease>', self.on_amount_change)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="Generate Kembyala", command=self.generate).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Generate RIB", command=self.generate_rib).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            bank_frame, 
            text="Fetch Bank Details", 
            command=self.fetch_bank_details
        ).grid(row=0, column=2, padx=5, pady=5)
    def on_amount_change(self, event):
        amount_str = self.entries['amount_figures'].get()
        words = self.amount_converter.convert_amount_to_words(amount_str)
        self.entries['amount_words'].delete(0, tk.END)
        self.entries['amount_words'].insert(0, words)
    
    def initialize_default_values(self):
        defaults = {
            'bank_code': '03',
            'branch_code': '001',
            'place_of_issue': 'Tunis',
            'date_of_issue' : datetime.now().strftime('%Y-%m-%d'),
            'due_date' : (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'),
            'beneficiary' : 'Ste Sib Distribution',
            'bank_address' : 'BNA Kairouan Medine'
        }
        for field, value in defaults.items():
            if field in self.entries:
                self.entries[field].delete(0, tk.END)
                self.entries[field].insert(0, value)
    
    def generate_rib(self):
        self.entries['bank_code'].delete(0, tk.END)
        self.entries['bank_code'].insert(0, "01")
        self.entries['branch_code'].delete(0, tk.END)
        self.entries['branch_code'].insert(0, "068")
        self.entries['account_number'].delete(0, tk.END)
        self.entries['account_number'].insert(0, "12345678")
        self.entries['rib_key'].delete(0, tk.END)
        self.entries['rib_key'].insert(0, "99")
    
    def generate(self):
        data = {field: entry.get() for field, entry in self.entries.items()}
        success = self.controller.generate_kembyala(data)
        if success:
            messagebox.showinfo("Success", "Kembyala generated successfully!")
            # Automatically open PDF after generation
        else:
            messagebox.showerror("Error", "Failed to generate Kembyala")
            

    def fetch_bank_details(self):
        bank_name = self.bank_name_var.get().strip()
        details = get_bank_details(bank_name)

        if details:
            self.entries['bank_code'].delete(0, tk.END)
            self.entries['bank_code'].insert(0, details["bank_code"])
            self.entries['branch_code'].delete(0, tk.END)
            self.entries['branch_code'].insert(0, details["branch_code"])
            self.entries['bank_address'].delete(0, tk.END)
            self.entries['bank_address'].insert(0, details["address"])
        else:
            messagebox.showerror("Error", f"No details found for bank: {bank_name}")
