import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from sqlite3 import Error
import os
import webbrowser

class DatabaseView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.db_file = "banks.db"
        self.create_widgets()
        self.load_kembyala()
    
    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=(
            'ID', 'Beneficiary', 'Amount', 'Bank', 'Due Date', 'Created'
        ), show='headings')
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Beneficiary', text='Bénéficiaire')
        self.tree.heading('Amount', text='Montant')
        self.tree.heading('Bank', text='Banque')
        self.tree.heading('Due Date', text='Échéance')
        self.tree.heading('Created', text='Créé le')
        
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Refresh", command=self.load_kembyala).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Open Selected", command=self.open_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_selected).pack(side=tk.LEFT, padx=5)
    
    def load_kembyala(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, beneficiary, amount_figures, bank_code, due_date, created_at
                FROM kembyala
                ORDER BY created_at DESC
            ''')
            for row in cursor.fetchall():
                self.tree.insert('', tk.END, values=row)
            conn.close()
        except Error as e:
            messagebox.showerror("Database Error", str(e))
    
    def open_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a kembyala first")
            return
        
        item = self.tree.item(selected[0])
        kembyala_id = item['values'][0]
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('SELECT pdf_path FROM kembyala WHERE id = ?', (kembyala_id,))
            result = cursor.fetchone()
            if result and result[0]:
                webbrowser.open(result[0])
            else:
                messagebox.showerror("Error", "PDF path not found")
            conn.close()
        except Error as e:
            messagebox.showerror("Database Error", str(e))
    
    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a kembyala first")
            return
        
        item = self.tree.item(selected[0])
        kembyala_id, beneficiary = item['values'][0], item['values'][1]
        
        if not messagebox.askyesno("Confirm Delete", f"Delete kembyala for {beneficiary}?"):
            return
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('SELECT pdf_path FROM kembyala WHERE id = ?', (kembyala_id,))
            result = cursor.fetchone()
            pdf_path = result[0] if result else None
            
            cursor.execute('DELETE FROM kembyala WHERE id = ?', (kembyala_id,))
            conn.commit()
            conn.close()
            
            if pdf_path and os.path.exists(pdf_path):
                try:
                    os.remove(pdf_path)
                except Exception as e:
                    messagebox.showwarning("File Deletion Failed", str(e))
            
            self.load_kembyala()
            messagebox.showinfo("Success", "Kembyala deleted successfully")
        except Error as e:
            messagebox.showerror("Database Error", str(e))