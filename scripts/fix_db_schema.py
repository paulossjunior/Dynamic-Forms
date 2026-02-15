import sqlite3
import os

DB_PATH = "backend/sql_app.db"

def add_column():
    if not os.path.exists(DB_PATH):
        print(f"Database file {DB_PATH} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(form_fields)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "section_id" in columns:
            print("Column 'section_id' already exists in 'form_fields'.")
        else:
            print("Adding 'section_id' column to 'form_fields'...")
            # SQLite supports ADD COLUMN
            cursor.execute("ALTER TABLE form_fields ADD COLUMN section_id INTEGER REFERENCES sections(id)")
            conn.commit()
            print("Column added successfully.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_column()
