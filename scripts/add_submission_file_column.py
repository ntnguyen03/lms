"""Small helper to add the ``file_path`` column to the ``submission`` table in the local
SQLite DB (lms.db).

Run from project root (where your ``lms.db`` is):

    python .\scripts\add_submission_file_column.py

This script will:
 - check for lms.db in current folder (or try to locate a .db file)
 - back it up to lms.db.bak (if exists, will not overwrite)
 - attempt to ALTER TABLE to add the column (SQLite supports ADD COLUMN)
 - report success or errors

Non-destructive: if column already exists, it will exit without changes.
"""
import sqlite3
import os
import shutil

DB_PATH = os.environ.get('DATABASE_URL')
# Normalize env-style sqlite URL like sqlite:///lms.db
if DB_PATH and DB_PATH.startswith('sqlite:///'):
    DB_PATH = DB_PATH.replace('sqlite:///', '')

# If not provided via env, default to lms.db in current working dir
if not DB_PATH:
    DB_PATH = 'lms.db'

print(f"Current working directory: {os.getcwd()}")
print(f"Looking for database file: {DB_PATH}")

# If the path doesn't exist, try to locate a .db file in common locations
if not os.path.exists(DB_PATH):
    # Check instance folder
    instance_candidate = os.path.join(os.getcwd(), 'instance', 'lms.db')
    if os.path.exists(instance_candidate):
        DB_PATH = instance_candidate
        print(f"Found database in instance folder: {DB_PATH}")
    else:
        # recursively search for any .db file in this repo (pick lms.db if found)
        found = None
        for root, dirs, files in os.walk(os.getcwd()):
            for fname in files:
                if fname.endswith('.db'):
                    if fname == 'lms.db':
                        found = os.path.join(root, fname)
                        break
                    if not found:
                        found = os.path.join(root, fname)
            if found:
                break
        if found:
            DB_PATH = found
            print(f"Auto-detected database file: {DB_PATH}")

if not os.path.exists(DB_PATH):
    print("Database file not found. Make sure you're running this from the project root where lms.db is located,")
    print("or set the DATABASE_URL environment variable to point to your sqlite file (e.g. sqlite:///path/to/lms.db).")
    raise SystemExit(1)

# Backup
backup_path = DB_PATH + '.bak'
if not os.path.exists(backup_path):
    shutil.copy2(DB_PATH, backup_path)
    print(f"Backup created: {backup_path}")
else:
    print(f"Backup already exists: {backup_path}")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Check if column already exists
try:
    cur.execute("PRAGMA table_info(submission);")
    cols = [row[1] for row in cur.fetchall()]
    if 'file_path' in cols:
        print('Column `file_path` already exists in submission table. No action taken.')
        conn.close()
        raise SystemExit(0)

    # Add column
    cur.execute("ALTER TABLE submission ADD COLUMN file_path VARCHAR(255);")
    conn.commit()
    print('Column `file_path` added successfully.')
except sqlite3.OperationalError as oe:
    print('SQLite OperationalError:', oe)
except Exception as e:
    print('Error:', e)
finally:
    conn.close()
