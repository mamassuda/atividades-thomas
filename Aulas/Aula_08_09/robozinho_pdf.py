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

padrao_email = r'(?:Email|email|[\w.-]+@[\w.-]+\.\w+)'
#* Aqui envolve uma sequência de caracteres + @ + domínio + "." + extensão

padrao_data = r'\d{2}[-/\.][a-zA-Z0-0]{2,3}[-/\.]\d{2,5}(?:d\.[CG]\.?)?'
#* Formato de data: DD/MM/AAAA -> dígitos e "/" separando

padrao_nome = r'(?:Nome|nome):\s*\n?([\s\S]*?)(?=\n?(?:Data|Dt|Endereço|CPF|cpf|Tel|Telefone|$))'


padrao_telefone = r'\(?\d{2}\)?[\s\n]*\d{4,5}[-\s\n]*\d{4}'

#* ESSA FUNCTION SERVIU COMO BASE #*
#! #! #! ####################################### #! #! #! 
#! #! #! Criar um function para extrair os dados #! #! #!
#! #! #! ####################################### #! #! #! 

import pypdf
import re

padrao_cpf_flexivel = r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b'

def extrair_dados_pdf(caminho_arquivo):

    dados_coletados = {
        "cpfs": [],  # Lista para cpfs
        'nomes': [], # Lista para nomes
        'emails': [], # Lista emails
        'datas': [], # Lista datas 
        'telefones': [] # Lista números telefones
    }
   
    
    try:
        reader = pypdf.PdfReader(caminho_arquivo)
        
        for pagina in reader.pages:
            texto = pagina.extract_text()
            if not texto:
                continue

            # 1. Extrair CPFs
            cpfs = re.findall(padrao_cpf, texto)
            dados_coletados["cpfs"].extend(cpfs)

            # 2. Extrair Telefones
            tels = re.findall(padrao_telefone, texto)
            # Limpa quebras de linha dentro do telefone
            tels_limpos = [re.sub(r'\s+', ' ', t).strip() for t in tels]
            dados_coletados["telefones"].extend(tels_limpos)

            # 3. Extrair E-mails
            emails = re.findall(padrao_email, texto)
            dados_coletados["emails"].extend(emails)

            # 4. Extrair Datas
            datas = re.findall(padrao_data, texto)
            dados_coletados["datas"].extend(datas)

            # 5. Extrair Nomes (Trata nomes em múltiplas linhas)
            nomes_brutos = re.findall(padrao_nome, texto)

            # 6. Extrair Apelidos (AKA) 
            apelidos = re.findall()
            for nome in nomes_brutos:
                # Substitui quebras de linha e múltiplos espaços por um único espaço
                nome_limpo = re.sub(r'\s+', ' ', nome).strip()
                if nome_limpo:
                    dados_coletados["nomes"].extend([nome_limpo])

    except FileNotFoundError:
        print("Erro: Arquivo não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro geral: {e}")

    return dados_coletados




#######################! #! #! #! #################!
##!#!#! Aqui eu vou otimizar meu código      ##!#!#!
##!#!#! implementando uma nova estratégia    ##!#!#!
#######################! #! #! #! #################!


#! A tática aqui é separar em blocos   #!
#! os blocos são divididos pelo termo  #!
#! "Nome|nome", logo cada usuário é um #!
#! bloco de informações                #!



def extrair_cadastros_por_pessoa(caminho_pdf):
    reader = pypdf.PdfReader(caminho_pdf)
    texto_bruto = ""
    
    # 1. Extrai todo o texto do documento
    for pagina in reader.pages:
        texto = pagina.extract_text()
        if texto:
            texto_bruto += texto + " "

    # 2. Normaliza quebras de linha e múltiplos espaços num único espaço
    texto_limpo = re.sub(r'\s+', ' ', texto_bruto)

    # 3. Divide o texto contínuo em blocos individuais por cliente
    blocos = re.split(r'(?=(?:Nome|nome):)', texto_limpo)
    
    lista_clientes = []

    for bloco in blocos:
        if not bloco.strip():
            continue
            
        # Captura o texto completo entre os rótulos de cada campo
        nome = re.search(r'(?:Nome|nome):\s*(.*?)\s*(?=(?:Data|Dt|Endereço|CEP|Tel|Telefone|CPF|cpf|$))', bloco)
        data_nasc = re.search(r'(?:Data de nascimento|Dt nasc):\s*(.*?)\s*(?=(?:Endereço|CEP|Tel|Telefone|CPF|cpf|$))', bloco)
        endereco = re.search(r'Endereço:\s*(.*?)\s*(?=(?:CEP|Tel|Telefone|CPF|cpf|$))', bloco)
        cep = re.search(r'CEP:\s*(.*?)\s*(?=(?:Tel|Telefone|CPF|cpf|$))', bloco)
        tel = re.search(r'(?:Tel|Telefone):\s*(.*?)\s*(?=(?:CPF|cpf|$))', bloco)
        cpf = re.search(r'(?:CPF|cpf):\s*(.*?)\s*$', bloco)

        cliente = {
            "nome": nome.group(1).strip() if nome else None,
            "data_nascimento": data_nasc.group(1).strip() if data_nasc else None,
            "endereco": endereco.group(1).strip() if endereco else None,
            "cep": cep.group(1).strip() if cep else None,
            "telefone": tel.group(1).strip() if tel else None,
            "cpf": cpf.group(1).strip() if cpf else None
        }
        
        lista_clientes.append(cliente)

    return lista_clientes

# Execução do código
resultados = extrair_cadastros_por_pessoa("cadastro.pdf")

# Exibição dos resultados completos
for i, cliente in enumerate(resultados, 1):
    print(f"=== CLIENTE {i} ===")
    for chave, valor in cliente.items():
        print(f"{chave.upper()}: {valor}")
    print()


import pandas as pd

# Usando a função anterior para obter a lista de dicionários
resultados = extrair_cadastros_por_pessoa("cadastro.pdf")

# 1. Cria o DataFrame diretamente da lista
df = pd.DataFrame(resultados)

# 2. Formata o nome das colunas para exibição (Opcional)
df.rename(columns={
    "nome": "Nome Completo",
    "data_nascimento": "Data de Nascimento",
    "endereco": "Endereço",
    "cep": "CEP",
    "telefone": "Telefone",
    "cpf": "CPF"
}, inplace=True)

# Exibe o DataFrame formatado no terminal
print(df)

# ===============================================
# EXPORTAÇÃO (ESCOLHA O FORMATO DESEJADO)
# ===============================================

# Salvar em Excel
df.to_excel("cadastros_extraidos.xlsx", index=False)

# Salvar em CSV
df.to_csv("cadastros_extraidos.csv", index=False, encoding="utf-8-sig")


