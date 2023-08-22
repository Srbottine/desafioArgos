import PyPDF2
import re
import tabula

class Arte:
    def __init__(self):
        self.plr_ingredientes = ""
        self.plr_alergenicos = ""
        self.plr_endereco = ""
        self.plr_industria = ""
        self.plr_nutricional = []

    def lerPlr(self, pdf_filename):
        # Abre o arquivo PDF
        pdf_file = open(pdf_filename, 'rb')

        # Cria um objeto PdfReader
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Extrai todo o texto do PDF
        all_text = ""
        for page in pdf_reader.pages:
            all_text += page.extract_text()

        # Usa expressões regulares para encontrar as informações com base nos rótulos das seções
        ingredientes_match = re.search(r'Ingredientes:(.*?)ALÉRGICOS:', all_text, re.DOTALL)
        alergenicos_match = re.search(r'ALÉRGICOS:(.*?)Claims-Others:', all_text, re.DOTALL)
        endereco_match = re.search(r't : I(.*?)Si', all_text, re.DOTALL)
        industria_match = re.search(r'33.033.028/ 0020-47.(.*?)Quality & Handling Information', all_text, re.DOTALL)

        # Extrair tabelas INFORMAÇÃO NUTRICIONAL usando tabula
        nutricional_tables = tabula.read_pdf(pdf_filename, pages="3", multiple_tables=True)

        # Definir as informações com base nos resultados correspondentes
        if ingredientes_match:
            self.plr_ingredientes = ingredientes_match.group(1).strip()
        if alergenicos_match:
            self.plr_alergenicos = alergenicos_match.group(1).strip()
        if endereco_match:
            self.plr_endereco = endereco_match.group(1).strip()
        if industria_match:
            self.plr_industria = industria_match.group(1).strip()
        if self.plr_industria:
            self.plr_industria = self.plr_industria.replace("Signature Line Text :", "").strip()

        # Filtrar e extrair tabelas INFORMAÇÃO NUTRICIONAL
        for table in nutricional_tables:
            table_text = table.to_string(index=False, header=False, justify="left")
            if "Porção" in table_text:
                
                self.plr_nutricional.append(table_text)
            

        # Fechar o arquivo PDF
        pdf_file.close()

# Exemplo de uso:
arte = Arte()
arte.lerPlr('plr_desafio.pdf')

# Acessar as informações extraídas
print("Ingredientes:")
print(arte.plr_ingredientes)
print("\nAlergênicos:")
print(arte.plr_alergenicos)
print("\nEndereços:")
print(arte.plr_endereco)
print("\nIndústria:")
print(arte.plr_industria)
print("\nTabelas INFORMAÇÃO NUTRICIONAL:")
for table in arte.plr_nutricional:
    print(table)
