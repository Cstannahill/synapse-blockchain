# synapse/database/database_manager.py

import pyodbc
import json

# Function to get database connection


def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=your_server_name;'
        'DATABASE=synapse_blockchain;'
        'UID=your_username;'
        'PWD=your_password;'
    )
    return conn

# Function to save a block to the database


def save_block_to_db(block):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Blocks (BlockIndex, Timestamp, Transactions, PreviousHash, Hash, MiningValidator)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            block.index,
            block.timestamp,
            json.dumps([tx.to_dict() for tx in block.transactions]),
            block.previous_hash,
            block.hash,
            block.mining_validator
        ))
        conn.commit()
    except Exception as e:
        print(f"Error saving block: {e}")
    finally:
        cursor.close()
        conn.close()

# Additional functions for loading, updating, or deleting blocks can also be added here
