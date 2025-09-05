import sqlite3

class BankDatabase:
    def __init__(self, db_file="banks.db"):
        self.db_file = db_file
        self.create_table()
        self.populate_banks()
    
    def create_table(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS banks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE,
                name TEXT,
                address TEXT
            )
        ''')
        conn.commit()
        conn.close()
        
    def populate_banks(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM banks")
        if cursor.fetchone()[0] == 0:
            banks = [
                ("03", "BNA Kairouan Medina", "Banque Nationale Agricole, Kairouan Medina, Avenue de la République"),
                ("03-001", "BNA Kairouan Medina Agence Centrale", "Banque Nationale Agricole, Kairouan Medina, Rue Ali Belhouane"),
                ("02", "BIAT Kairouan", "Banque Internationale Arabe de Tunisie, Kairouan, Avenue Habib Bourguiba"),
                ("03", "BTS Kairouan", "Banque de Tunisie et des Emirats, Kairouan, Rue Ibn Khaldoun"),
                ("04", "ATB Kairouan", "Arab Tunisian Bank, Kairouan, Avenue Taher Haddad"),
                ("07", "AMEN BANK Kairouan", "Amen Bank, Kairouan, Rue de la Kasbah"),
                ("10", "UIB Kairouan", "Union Internationale de Banques, Kairouan, Avenue 7 Novembre"),
                ("16", "BTE Kairouan", "Banque de Tunisie, Kairouan, Avenue Taher Haddad"),
                ("18", "ATTIJARI BANK Kairouan", "Attijari Bank, Kairouan, Rue Ibn Khaldoun"),
                ("20", "UBCI Kairouan", "Union Bancaire pour le Commerce et l'Industrie, Kairouan, Avenue Habib Bourguiba"),
            ]
            
            cursor.executemany(
                "INSERT INTO banks (code, name, address) VALUES (?, ?, ?)",
                banks
            )
            conn.commit()
        conn.close()
    
    def get_bank_by_name(self, bank_name):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT code, name, address FROM banks WHERE name LIKE ?",
            (f"%{bank_name.strip()}%",))
        bank = cursor.fetchone()
        conn.close()
        return bank
        
    def get_all_bank_names(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM banks ORDER BY name")
        banks = [row[0] for row in cursor.fetchall()]
        conn.close()
        return banks