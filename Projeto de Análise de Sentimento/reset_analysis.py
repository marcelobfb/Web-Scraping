# reset_analysis.py
import sqlite3

def reset_sentiments():
    conn = sqlite3.connect('mercado_livre_reviews.db')
    cursor = conn.cursor()

    print("Resetando colunas de sentimento no banco de dados...")

    # Este comando apaga os valores das colunas de sentimento,
    # permitindo que o analyzer.py rode novamente sobre os mesmos dados.
    cursor.execute("UPDATE reviews SET sentiment_label = NULL, sentiment_score = NULL, analysis_timestamp = NULL")

    # Pega o número de linhas afetadas
    rows_affected = cursor.rowcount

    conn.commit()
    conn.close()

    print(f"{rows_affected} linhas foram resetadas com sucesso.")
    print("Agora você pode rodar o 'analyzer.py' novamente.")

if __name__ == '__main__':
    reset_sentiments()