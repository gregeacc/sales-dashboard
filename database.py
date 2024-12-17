import sqlite3
import pandas as pd
from datetime import datetime

class SalesDatabase:
    def __init__(self, db_path='sales.db'):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Date TEXT NOT NULL,
                    Product TEXT,
                    Sales_Amount REAL,
                    Opportunity_Status TEXT,
                    Total_Sales REAL
                )
            ''')

    def import_from_csv(self, csv_path):
        df = pd.read_csv(csv_path)
        with sqlite3.connect(self.db_path) as conn:
            df.to_sql('sales', conn, if_exists='replace', index=False)
        return True

    def get_all_data(self):
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query('SELECT * FROM sales', conn)
            df['Date'] = pd.to_datetime(df['Date'])
            return df

    def get_column_names(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('SELECT * FROM sales LIMIT 1')
            return [description[0] for description in cursor.description]