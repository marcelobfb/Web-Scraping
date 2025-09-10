import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import textwrap

def create_dashboard(limit_reviews_to_show=5):
    conn = sqlite3.connect('mercado_livre_reviews.db')

    query_chart = "SELECT sentiment_label FROM reviews WHERE sentiment_label IS NOT NULL AND sentiment_label != 'ERROR'"
    query_list = f"SELECT review_text, sentiment_label FROM reviews WHERE sentiment_label IS NOT NULL AND sentiment_label != 'ERROR' LIMIT {limit_reviews_to_show}"

    try:
        df_chart = pd.read_sql_query(query_chart, conn)
        df_list = pd.read_sql_query(query_list, conn)

        if df_chart.empty:
            print("Não há dados analisados para gerar o dashboard.")
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), gridspec_kw={'width_ratios': [1, 1.5]})

        sentiment_counts = df_chart['sentiment_label'].value_counts()
        colors = []
        labels = sentiment_counts.index
        for label in labels:
            if label == 'POSITIVE': colors.append('#2ca02c')
            elif label == 'NEGATIVE': colors.append('#d62728')
            else: colors.append('#ff7f0e')

        ax1.pie(sentiment_counts, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, textprops={'fontsize': 12})
        ax1.set_title('Distribuição de Sentimentos', fontsize=16)

        ax2.set_title('Amostra das Análises', fontsize=16)

        ax2.axis('off')

        text_y_position = 0.95
        
        if df_list.empty:
            ax2.text(0, 0.5, "Nenhum review para listar.", fontsize=12, ha='left', va='center')
        else:
            for index, row in df_list.iterrows():
                sentiment = row['sentiment_label']
                review_text = row['review_text']

                header = f"SENTIMENTO: {sentiment}"
                wrapped_text = "\n".join(textwrap.wrap(f'"{review_text}"', width=80))
                
                text_color = '#2ca02c' if sentiment == 'POSITIVE' else '#d62728'

                ax2.text(0, text_y_position, header, fontsize=12, weight='bold', color=text_color, ha='left', va='top')
                text_y_position -= 0.05 
                ax2.text(0, text_y_position, wrapped_text, fontsize=10, ha='left', va='top', style='italic')
                text_y_position -= 0.15 

        fig.tight_layout(pad=3.0)
        plt.savefig('sentimento_dashboard_completo.png')
        print("Dashboard completo salvo como 'sentimento_dashboard_completo.png'")
        
        plt.show()

    except Exception as e:
        print(f"Ocorreu um erro ao gerar o dashboard: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    create_dashboard(limit_reviews_to_show=5)