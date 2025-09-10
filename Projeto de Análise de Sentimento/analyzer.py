# analyzer.py (Usando o modelo base "neuralmind/bert-base-portuguese-cased")

import sqlite3
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import traceback

def analyze_sentiments():
    """
    Analisa os sentimentos usando o modelo de base 'neuralmind/bert-base-portuguese-cased'.
    AVISO: A precisão para análise de sentimento será baixa, pois este modelo não é 
    especializado nesta tarefa.
    """
    try:
        print("Carregando modelo de base (BERTimbau do repositório Neuralmind)...")
        model_name = "neuralmind/bert-base-portuguese-cased"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        print("Modelo carregado.")

        conn = sqlite3.connect('mercado_livre_reviews.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id, review_text FROM reviews WHERE sentiment_label IS NULL")
        reviews_to_analyze = cursor.fetchall()

        if not reviews_to_analyze:
            print("\nNenhum review novo para analisar. Se quiser re-analisar tudo, rode o script 'reset_analysis.py' primeiro.")
            conn.close()
            return

        print(f"Analisando {len(reviews_to_analyze)} novos reviews...")

        for review_id, review_text in reviews_to_analyze:
            inputs = tokenizer(review_text, return_tensors="pt", truncation=True, max_length=512)
            with torch.no_grad():
                logits = model(**inputs).logits
            
            predicted_class_id = logits.argmax().item()
            
            # A lógica assume que a Classe 1 é Positiva. A precisão do modelo aqui é baixa.
            sentiment = 'POSITIVE' if predicted_class_id == 1 else 'NEGATIVE'
            
            probabilities = torch.nn.functional.softmax(logits, dim=-1)[0]
            score = probabilities[predicted_class_id].item()

            print(f"  - ID {review_id}: Análise concluída (Classe: {predicted_class_id} -> {sentiment})")

            cursor.execute(
                "UPDATE reviews SET sentiment_label = ?, sentiment_score = ?, analysis_timestamp = CURRENT_TIMESTAMP WHERE id = ?",
                (sentiment, score, review_id)
            )

        conn.commit()
        conn.close()
        print("\nAnálise final concluída. Banco de dados atualizado.")
    except Exception as e:
        print("\n--- OCORREU UM ERRO DURANTE A ANÁLISE ---")
        full_traceback = traceback.format_exc()
        print(full_traceback)

if __name__ == '__main__':
    analyze_sentiments()