import pandas as pd
import sqlite3
 
# Constants
DB_FILENAME = 'arxiv_wildfire_database.db'
EXCEL_FILENAME = 'arxiv_wildfire_excel.xlsx'
JSON_FILENAME = 'arxiv_wildfire_intervals.json'


def save_data(df: pd.DataFrame):
    if df.empty:
        print("No data to save.")
        return
 
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    # Create table with generated_summary column
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS arxiv_papers (
            id TEXT PRIMARY KEY,
            updated TEXT,
            published TEXT,
            title TEXT,
            summary TEXT,
            authors TEXT,
            affiliations TEXT,
            doi TEXT,
            comment TEXT,
            journal_ref TEXT,
            primary_category TEXT,
            categories TEXT,
            link_alternate TEXT,
            link_pdf TEXT,
            generated_summary TEXT
        )
    ''')
 
    inserted = 0
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT OR IGNORE INTO arxiv_papers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['id'], row['updated'], row['published'], row['title'], row['summary'], row['authors'],
            row['affiliations'], row['doi'], row['comment'], row['journal_ref'], row['primary_category'],
            row['categories'], row['link_alternate'], row['link_pdf'], row['generated_summary']
        ))
        inserted += cursor.rowcount
 
    conn.commit()
 
    # Export full DB to Excel, including generated_summary
    full_df = pd.read_sql_query("SELECT * FROM arxiv_papers", conn)
    full_df.to_excel(EXCEL_FILENAME, index=False)
 
    conn.close()
    print(f"Inserted {inserted} new records.")
 
def main():
    try:
        df = pd.read_csv('temp.csv')
    except Exception as e:
        print('Error reading csv file', str(e))
        return
    if not df.empty:
        save_data(df)
    else:
        print("No new data fetched.")

 
if __name__ == "__main__":
    main()