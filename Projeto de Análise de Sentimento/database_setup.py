import sqlite3

def create_database():
    conn=sqlite3.connect('mercado_livre_reviews.db')
    cursor=conn.cursor()
    
    print("Conectado ao banco de dados.")
    
    create_table_query="""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_url TEXT NOT NULL,
        review_text TEXT NOT NULL,
        sentiment_label TEXT,
        sentiment_score REAL,
        analysis_timestamp TIMESTAMP
    )
    """
    
    cursor.execute(create_table_query)
    print("Tabela 'reviws' verificada/criada com sucesso.")
    
    conn.commit()
    conn.close()
    print("Conexão Fechada.")
    
if __name__=='__main__':
    create_database()