
from playwright.sync_api import sync_playwright
import pandas as pd 
import time


# Configura o Pandas para exibir tudo sem cortar
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

url = "https://www.scrapethissite.com/pages/ajax-javascript/"

with sync_playwright() as p:
    browser = p.chromium.launch(
    headless=True,
    args=['--no-sandbox', '--disable-gpu']
)

    page = browser.new_page()
    page.goto(url)

    # Localiza os elementos dos anos
    elementos_anos = page.query_selector_all(".year-link")
    anos = [elem.get_attribute("id") for elem in elementos_anos]
    
    todos_filmes = []

    for ano in anos:
        print(f"Coletando ano: {ano}...")
        
        # Clica no botão do ano
        page.click(f"[id='{ano}']")
        time.sleep(1.5) # Pausa para renderização do AJAX

        # Captura as linhas da tabela
        linhas = page.query_selector_all("tr.film")
        
        for linha in linhas:
            titulo = linha.query_selector(".film-title").inner_text().strip()
            indicacoes = linha.query_selector(".film-nominations").inner_text().strip()
            premios = linha.query_selector(".film-awards").inner_text().strip()
            
            # Identifica se é o vencedor de Melhor Filme (presença do ícone de bandeira)
            best_picture_elem = linha.query_selector(".film-best-picture")
            melhor_filme = True if (best_picture_elem and best_picture_elem.query_selector("i")) else False
            
            todos_filmes.append({
                "ano_categoria": ano,
                "titulo": titulo,
                "indicacoes": indicacoes,
                "premios": premios,             # Vírgula adicionada
                "Melhor Filme": melhor_filme     # Variável agora extraída corretamente
            })

    browser.close()

# Estrutura em um DataFrame do Pandas e exibe no terminal
df = pd.DataFrame(todos_filmes)

print("\n" + "="*60)
print("LISTA COMPLETA DE FILMES")
print("="*60)
print(df)