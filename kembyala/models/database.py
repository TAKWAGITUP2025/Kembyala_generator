import sqlite3
from datetime import datetime
from sqlite3 import Error
import os
from ..utils.pdf import PDFGenerator

class KembyalaModel:
    def __init__(self, db_file="banks.db"):
        self.db_file = db_file
        self.pdf_generator = PDFGenerator()
        self.init_db()
    
    def init_db(self):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS kembyala")
            cursor.execute("DROP TABLE IF EXISTS audit_log")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS kembyala (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount_figures TEXT,
                    amount_words TEXT,
                    beneficiary TEXT,
                    drawee TEXT,
                    bank_code TEXT,
                    branch_code TEXT,
                    account_number TEXT,
                    rib_key TEXT,
                    place_of_issue TEXT,
                    date_of_issue TEXT,
                    due_date TEXT,
                    bank_address TEXT,
                    aval TEXT,
                    tire_address TEXT,
                    barcode_data TEXT,
                    pdf_path TEXT,
                    created_at TEXT
                )
            ''')
            conn.commit()
            conn.close()
        except Error as e:
            raise Exception(f"Database initialization failed: {str(e)}")
    
    def generate_kembyala(self, data):
        try:
            if not self._validate_data(data):
                raise Exception("Invalid data provided")
                
            rib_data = f"{data['bank_code']}{data['branch_code']}{data['account_number']}{data['rib_key']}"
            if len(rib_data) != 15:
                raise Exception("RIB must be exactly 15 digits (2+3+8+2)")
                
            pdf_path = self.pdf_generator.generate(data)
            self._save_to_db(data, pdf_path, rib_data)
            return pdf_path
        except Exception as e:
            raise Exception(f"Kembyala generation failed: {str(e)}")
    
    def _validate_data(self, data):
        required_fields = ['bank_code', 'branch_code', 'account_number', 'rib_key',
                         'amount_figures', 'amount_words', 'beneficiary']
        return all(data.get(field) for field in required_fields)
    
    def _save_to_db(self, data, pdf_path, rib_data):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO kembyala (
                amount_figures, amount_words, beneficiary, drawee,
                bank_code, branch_code, account_number, rib_key,
                place_of_issue, date_of_issue, due_date, bank_address,
                aval, tire_address, barcode_data, pdf_path, created_at
            )
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
      ''', (
          data['amount_figures'],
          data['amount_words'],
          data['beneficiary'],
          data['drawee'],
          data['bank_code'],
          data['branch_code'],
          data['account_number'],
          data['rib_key'],
          data['place_of_issue'],
          data['date_of_issue'],
          data['due_date'],
          data['bank_address'],
          data['aval'],
          data['tire_address'],
          rib_data,
          pdf_path,
          datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))

        
            
        conn.commit()
        conn.close()
    def get_bank_by_name(self, bank_name):
        """Get bank details by name from database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT code, name, address FROM banks WHERE name LIKE ?",
                (f"%{bank_name.strip()}%",)
            )
            bank = cursor.fetchone()
            conn.close()
            return bank
        except Error as e:
            raise Exception(f"Database error: {str(e)}")