import sqlite3

def init_standards_db(db_path='standards.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS standards
                 (id INTEGER PRIMARY KEY, standard_code TEXT, description TEXT, compliance_rules TEXT)''')
    conn.commit()
    conn.close()

# Example function to add a standard
def add_standard(standard_code, description, compliance_rules):
    conn = sqlite3.connect('standards.db')
    c = conn.cursor()
    c.execute("INSERT INTO standards (standard_code, description, compliance_rules) VALUES (?, ?, ?)",
              (standard_code, description, compliance_rules))
    conn.commit()
    conn.close()

# To use: init_standards_db(); add_standard('DBN V.2.5-67:2013', 'Building norms for HVAC', 'Detailed rules...')
