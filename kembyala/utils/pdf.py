from fpdf import FPDF
from datetime import datetime
import os

class PDFGenerator:
    def __init__(self):
        self.field_positions = {
            'bank_code': (6, 71),
            'branch_code': (14, 71),
            'account_number': (26, 71),
            'rib_key': (71, 71),
            'bank_code_2': (52, 25),
            'branch_code_2': (62, 25),
            'account_number_2': (75, 25),
            'rib_key_2': (120, 25),
            'amount_figures': (150, 30),
            'amount_figures_2': (150, 41),
            'amount_words': (13, 49),
            'amount_words_2': (150, 150),
            'beneficiary': (60, 44),
            'drawee': (150, 150),
            'drawee_2': (82, 75),
            'place_of_issue': (92, 10),
            'place_of_issue_2': (10, 60),
            'date_of_issue': (91, 15),
            'date_of_issue_2': (35, 60),
            'due_date': (55, 15),
            'due_date_2': (69, 60),
            'bank_address': (125, 70),
            'aval': (50, 82),
            'tire_address': (85, 84),
            'tire_address_2': (56, 88),
            'barcode': (150, 250)
        }
    
    def generate(self, data):
        pdf = FPDF(unit='mm', format='A4')
        pdf.add_page()
        
        try:
            pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
            pdf.set_font('DejaVu', '', 9)
        except:
            pdf.set_font('Arial', '', 9)
        
        for field, pos in self.field_positions.items():
            if field.endswith('_2'):
                base_field = field[:-2]
                if base_field in data:
                    pdf.text(pos[0], pos[1], data[base_field])
            elif field in data:
                pdf.text(pos[0], pos[1], data[field])
        
        if 'amount_words' in data:
            self._add_multiline_text(pdf, data['amount_words'], 
                                   self.field_positions['amount_words'][0], 
                                   self.field_positions['amount_words'][1], 
                                   max_width=120)
        
        pdf_dir = "generated_kembyala"
        os.makedirs(pdf_dir, exist_ok=True)
        beneficiary_short = data['beneficiary'][:20].replace(" ", "_")
        pdf_filename = f"kembyala_{beneficiary_short}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = os.path.join(pdf_dir, pdf_filename)
        pdf.output(pdf_path)
        
        return pdf_path
    
    def _add_multiline_text(self, pdf, text, x, y, max_width):
        lines = []
        words = text.split()
        current_line = ""
        
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if pdf.get_string_width(test_line) <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        for i, line in enumerate(lines):
            pdf.text(x, y + (i * 5), line)