import tkinter as tk
from tkinter import ttk, filedialog
import webbrowser
import os

class PreviewView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
    
    def create_widgets(self):
        self.preview_label = ttk.Label(self, text="Kembyala will appear here after generation", wraplength=800)
        self.preview_label.pack(pady=50)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Print", command=self.print_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Save PDF", command=self.save_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Open PDF", command=self.open_pdf).pack(side=tk.LEFT, padx=5)
    
    def print_pdf(self):
        if not getattr(self.controller, "current_pdf", None):
            messagebox.showerror("Error", "No PDF generated yet")
            return
        try:
            if os.name == 'nt':  # Windows
                os.startfile(self.controller.current_pdf, "print")
            else:  # macOS/Linux
                os.system(f"lp '{self.controller.current_pdf}'")
        except Exception as e:
            messagebox.showerror("Print Error", str(e))
    
    def save_pdf(self):
        if not getattr(self.controller, "current_pdf", None):
            messagebox.showerror("Error", "No PDF generated yet")
            return
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile=os.path.basename(self.controller.current_pdf)
        )
        if filename:
            shutil.copy(self.controller.current_pdf, filename)
            messagebox.showinfo("Success", f"Saved to {filename}")
    
    def open_pdf(self):
        """Open the current PDF using the default PDF viewer."""
        if not getattr(self.controller, "current_pdf", None):
            messagebox.showerror("Error", "No PDF generated yet")
            return
        try:
            pdf_path = self.controller.current_pdf
            system_name = platform.system()
            if system_name == "Windows":
                os.startfile(pdf_path)
            elif system_name == "Darwin":  # macOS
                os.system(f"open '{pdf_path}'")
            else:  # Linux/others
                os.system(f"xdg-open '{pdf_path}'")
        except Exception as e:
            messagebox.showerror("Open PDF Error", str(e))
    
    def auto_open_pdf(self):
        """Call this after generating a PDF to automatically open it."""
        if getattr(self.controller, "current_pdf", None):
            self.open_pdf()