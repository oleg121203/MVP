import sqlite3
from .ukrainian_standards_db import init_standards_db, add_standard  # Import from sibling module

def check_compliance(project_data, standard_code):
    init_standards_db()  # Ensure database is initialized
    conn = sqlite3.connect('standards.db')
    c = conn.cursor()
    c.execute("SELECT compliance_rules FROM standards WHERE standard_code = ?", (standard_code,))
    result = c.fetchone()
    conn.close()
    if result:
        rules = result[0]  # Compliance rules as string; in a real system, parse and compare with project_data
        return {"compliant": True, "details": rules} if 'compliant' in rules else {"compliant": False, "details": "Non-compliance detected"}
    return {"compliant": False, "details": "Standard not found"}

# Example usage: check_compliance({'some_key': 'value'}, 'DBN V.2.5-67:2013')
