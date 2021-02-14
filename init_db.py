import sqlite3


def insert_to_price(company, connection, cursor):
    query = f"""
    INSERT INTO company VALUES
        (NULL, ?, ?, ?, ?, ?, 
    )
    """

def insert_to_company(company, connection, cursor):
    query = f"""
    SELECT * FROM company
    WHERE ticker = '{company.ticker}'
    """
    result = cursor.execute(query).fetchone()
    if not result:
        query = f"""
        INSERT INTO company VALUES
            (NULL, ?, ?, ?, ?, ?)
        """
        cursor.execute(
            query, 
            (company.full_name, company.ticker, company.sector,
             company.website, company.summary
            )
        )
    connection.commit()

if __name__ == "__main__":
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    create_table = """
    CREATE TABLE company ( 
        company_id INTEGER PRIMARY KEY,
        full_name TEXT, 
        ticker TEXT,
        sector TEXT,
        website TEXT,
        summary TEXT
    )
    """
    cursor.execute(create_table)
    connection.commit()

    create_table = """
    CREATE TABLE price (
        price_id INTEGER PRIMARY KEY,
        company_id INTEGER,
        open REAL,
        close REAL,
        high REAL,
        low REAL,
        volume REAL,
        price_day INTEGER
    )
    """
    cursor.execute(create_table)
    connection.commit()

    connection.close()
