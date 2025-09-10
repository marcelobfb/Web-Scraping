import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def scrape_reviews(product_url):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(product_url)

    print(f"Acessando a URL: {product_url}")
    time.sleep(5)

    conn = sqlite3.connect('mercado_livre_reviews.db')
    cursor = conn.cursor()

    try:
        review_elements = driver.find_elements(By.CLASS_NAME, 'ui-review-capability-comments__comment__content')
        
        print(f"Encontrados {len(review_elements)} comentários.")
        
        for element in review_elements:
            review_text = element.text
            if review_text: 
                print(f"Coletado: {review_text[:60]}...")
                cursor.execute(
                    "INSERT INTO reviews (product_url, review_text) VALUES (?, ?)",
                    (product_url, review_text)
                )
        
        conn.commit()
        print("Dados salvos no banco de dados com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    finally:
        conn.close()
        driver.quit()

if __name__ == '__main__':
    target_url = "https://produto.mercadolivre.com.br/MLB-3596160769-camiseta-feminina-dry-fit-malha-fria-fitnes-academia-7-cores-_JM?searchVariation=182269045505#polycard_client=search-nordic&searchVariation=182269045505&search_layout=grid&position=7&type=item&tracking_id=d3646fff-6225-489d-934a-0c583c78ef9c"
    scrape_reviews(target_url)