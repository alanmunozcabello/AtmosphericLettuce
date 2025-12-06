import sqlite3
import os

DB_PATH = "src/data/DataBase.db"

# Función backup de la tabla de codigos de recuperacion
def fix_table():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS codigos_recuperacion (
                correo TEXT PRIMARY KEY,
                codigo TEXT NOT NULL,
                expiracion DATETIME NOT NULL
            )
        """)
        conn.commit()
        print("✅ Table 'codigos_recuperacion' created successfully.")
    except Exception as e:
        print(f"❌ Error creating table: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    fix_table()
