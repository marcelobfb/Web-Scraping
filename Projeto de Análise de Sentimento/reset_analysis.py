
import sqlite3

def reset_sentiments():
    conn = sqlite3.connect('mercado_livre_reviews.db')
    cursor = conn.cursor()

    print("Resetando colunas de sentimento no banco de dados...")

    cursor.execute("UPDATE reviews SET sentiment_label = NULL, sentiment_score = NULL, analysis_timestamp = NULL")

    rows_affected = cursor.rowcount

    conn.commit()
    conn.close()

    print(f"{rows_affected} linhas foram resetadas com sucesso.")
    print("Agora você pode rodar o 'analyzer.py' novamente.")

if __name__ == '__main__':
    reset_sentiments()