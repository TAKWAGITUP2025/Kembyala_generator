import tkinter as tk
from tkinter import ttk, messagebox  # ADD messagebox import here
import os
import subprocess
import platform
from .views.data_entry import DataEntryView
from .views.preview import PreviewView
from .views.database_view import DatabaseView
from .models.database import KembyalaModel

class KembyalaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kembyala Generator")
        self.root.geometry("1200x900")
        self.model = KembyalaModel()
        self.current_pdf = None
        self.create_ui()
    
    def create_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.data_tab = DataEntryView(self.notebook, self)
        self.preview_tab = PreviewView(self.notebook, self)
        self.db_tab = DatabaseView(self.notebook, self)
        
        self.notebook.add(self.data_tab, text="Data Entry")
        self.notebook.add(self.preview_tab, text="Preview")
        self.notebook.add(self.db_tab, text="Database")
    
    def open_pdf(self, pdf_path):
        """Open PDF file with the default system viewer"""
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', pdf_path))
            elif platform.system() == 'Windows':  # Windows
                os.startfile(pdf_path)
            else:  # Linux variants
                subprocess.call(('xdg-open', pdf_path))
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Could not open PDF: {str(e)}")  # FIXED: messagebox
            return False
    
    def generate_kembyala(self, data):
        try:
            pdf_path = self.model.generate_kembyala(data)
            self.current_pdf = pdf_path
            
            # Update preview tab
            if hasattr(self.preview_tab, 'update_preview'):
                self.preview_tab.update_preview()
            
            # Automatically open the generated PDF
            self.open_pdf(pdf_path)
            
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))  # FIXED: messagebox
            return False
    
    def get_bank_details(self, bank_name):
        """Controller method to fetch bank details"""
        return self.model.get_bank_by_name(bank_name)
    
    def get_bank_and_branch_code(self, bank_name):
        """Controller method to get bank and branch codes"""
        return self.model.get_bank_and_branch_code(bank_name)