import pypdf
import re
from pypdf import PdfReader

#! #! #! ######################################### #! #! #! 
#! #! #! Aqui vou criar uma function para ler PDFs #! #! #!
#! #! #! ######################################### #! #! #! 

def ler_pdf(caminho_pdf):
    try:                                                      #! Utilizar a função try para caso #!
        reader = pypdf.PdfReader(caminho_pdf)                 #! dê algum erro, eu saiba onde o  #!
        print(f"Total de páginas: {len(reader.pages)}\n")     #! erro ocorreu. (try e except)    #!

        #* Laço de repetição até ler todas as páginas #* 

        for i, pagina in enumerate(reader.pages):                       #! Aqui conto as páginas e #!
            texto = pagina.extract_text()                               #! aviso caso haja alguma  #!
            print(f"=== Página {i + 1} ===")                            #! sem texto detectável    #!
            print(texto if texto else "[Página sem texto detectável]")

    except FileNotFoundError:                               #! Possíveis erros que possam #!
        print("Erro: Arquivo não foi encontrado.")          #! acontecer ao ler o arquivo #!
    except Exception as e:                                  #! solicitado                 #! 
        print(f"Ocorreu um erro: {e}")


#? Aqui temos uma função para ler o PDF #?
# ler_pdf("cadastro.pdf")        

#! #! #! ############################## #! #! #! 
#! #! #! Aqui vou listar alguns moldes  #! #! #! 
#! #! #! de "strings" para encontrar    #! #! #! 
#! #! #! CPF, CNPJ, E-mail, Datas e etc #! #! #! 
#! #! #! ############################## #! #! #! 

#! Padrão flexível:
#*  \.? -> O ponto é opcional
#*  -?  -> O hífen é opcional
#*  \b  -> Garante limites numéricos para não pegar 
#*  trechos de números maiores (como protocolos)



padrao_cpf = r'\d{3}\.\d{3}\.\d{3}-\d{2}'
#* Aqui eu digo: "3 dígitos" + " . " + "3 dígitos" + "." + "3 dígitos " + " - " + "2 dígitos"

#* Procura 'CPF', 'Cpf' e 'cpf', seguido opcionalmente de ':', '.' ou espaços, 
#* e captura APENAS o número de 11 dígitos que vem logo depois.

padrao_cpf_flexivel = r'(?:CPF|cpf|Cpf)[:\s\.]*(\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b)'
#! tipo flexível para CPF

padrao_email = r'(?:Email|email|[\w.-]+@[\w.-]+\.\w+'
#* Aqui envolve uma sequência de caracteres + @ + domínio + "." + extensão

padrao_data = r'\d{2}/\d{2}/\d{4}' 
#* Formato de data: DD/MM/AAAA -> dígitos e "/" separando

padrao_nome = r'Nome:\s*(.+)'

padrao_telefone = 



#! #! #! ####################################### #! #! #! 
#! #! #! Criar um function para extrair os dados #! #! #!
#! #! #! ####################################### #! #! #! 

import pypdf
import re

padrao_cpf_flexivel = r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b'

def extrair_dados_pdf(caminho_arquivo):
    cpfs_coletados = []  # Lista para cpfs
    nomes_coletados = [] # Lista para nomes
    email_coletados = [] # Lista emails
    data_coletados = [] # Lista datas 
    
    try:
        reader = pypdf.PdfReader(caminho_arquivo)
        
        for i, pagina in enumerate(reader.pages):
            texto = pagina.extract_text()
            linhas = texto.splitlines()
            
            for linha in linhas:
                if "cpf" in linha.lower():
                    try:
                        resultado = re.findall(padrao_cpf_flexivel, linha)
                        if resultado:
                            # .extend() adiciona os itens da lista 'resultado' na lista acumuladora
                            cpfs_coletados.extend(resultado)
                    except Exception as e_regex:
                        print(f" Parte CPF | Erro ao processar regex na linha: {e_regex}")

            for linha2 in linhas:
                if "nome" in linha.lower()
                    try:
                        resultado = re.findall(padrao_nome, linha2)
                        if resultado:
                            nome_coletados.extend(resultado)

                    except Exception as e_regex:
                        print(f" Parte Nome | Erro ao processar regex na linha: {e_regex}")

            for linha3 in linhas:
                if "Tel" in linha.lower():
                    try:
                        resultado = re.findall(padrao_cpf_flexivel, linha)
                        if resultado:
                            # .extend() adiciona os itens da lista 'resultado' na lista acumuladora
                            cpfs_coletados.extend(resultado)
                    except Exception as e_regex:
                        print(f" Parte Tel | Erro ao processar regex na linha: {e_regex}")
            
            for linha4 in linhas:
                if "nome" in linha.lower()
                    try:
                        resultado = re.findall(padrao_nome, linha2)
                        if resultado:
                            nome_coletados.extend(resultado)

                        except Exception as e_regex:
                             print(f" Parte Nome | Erro ao processar regex na linha: {e_regex}")    


    except FileNotFoundError:
        print("Erro: Arquivo não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    # Retorna a lista completa acumulada ao término da leitura
    return cpfs_coletados

# --- Uso do script ---
# Guardamos o retorno da função dentro da variável 'lista_final_cpfs'
lista_final_cpfs = extrair_dados_pdf("cadastro.pdf")

# Exibição do resultado
print("Lista final de CPFs armazenados:", lista_final_cpfs)