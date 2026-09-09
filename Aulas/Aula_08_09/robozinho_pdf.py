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


ler_pdf("Aula_08_09/cadastro.pdf")        

#! #! #! ############################## #! #! #! 
#! #! #! Aqui vou listar alguns moldes  #! #! #! 
#! #! #! de "strings" para encontrar    #! #! #! 
#! #! #! CPF, CNPJ, E-mail, Datas e etc #! #! #! 
#! #! #! ############################## #! #! #! 

padrao_cpf = [r'\d{3}\.\d{3}\.\d{3}-\d{2}',
              r'\d{9}-\d{2}']
            
#* Aqui eu digo: "3 dígitos" + " . " + "3 dígitos" + "." + "3 dígitos " + " - " + "2 dígitos"

padrao_email = r'[\w.-]+@[\w.-]+\.\w+'
#* Aqui envolve uma sequência de caracteres + @ + domínio + "." + extensão

padrao_data = r'\d{2}/\d{2}/\d{4}' 
#* Formato de data: DD/MM/AAAA -> dígitos e "/" separando

padrao_nome = r'Nome:\s*(.+)'



#! #! #! ####################################### #! #! #! 
#! #! #! Criar um function para extrair os dados #! #! #!
#! #! #! ####################################### #! #! #! 

def extrair_dados_pdf(caminho_arquivo):
    reader = pypdf.PdfReader(caminho_arquivo)
    for i, pagina in enumerate(reader.pages):
        texto = pagina.extract_text()

        for j in padrao_cpf:

            cpfs = re.findall(i, texto)

            if cpfs:
                print(f"Página {i + 1} contém os CPFs: {cpfs}")

extrair_dados_pdf("Aula_08_09/cadastro.pdf")