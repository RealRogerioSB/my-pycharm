import pandas as pd
import pdfplumber as pdf


# Função para extrair tabelas do PDF.
def extrair_tabelas_pdf(file_path):
    tabelas = []

    with pdf.open(file_path) as f:
        for page in f.pages:
            tabelas_paginas = page.extract_tables()

            for tabela in tabelas_paginas:
                tabelas.append(pd.DataFrame(tabela[1:], columns=tabela[0]))

    return tabelas


# Função para salvar tabelas no Excel.
def salvar_tabelas_em_excel(tabelas, output_file):
    with pd.ExcelWriter(output_file) as writer:
        for i, tabela in enumerate(tabelas):
            tabela.to_excel(writer, sheet_name=f"Página {i + 1}", index=False)

    print("Exportação de PDF para Excel com sucesso!")


# Caminho do PDF de entrada e arquivo Excel de saída
# pdf_file = r"C:\Users\F8719981\Downloads\Planilha de Cálculo  UDO ELIMAR NEUMANN JUNIOR.pdf"
pdf_file = r"C:\Users\F8719981\Downloads\CARMEN.pdf"
xls_file = r"C:\Users\F8719981\Downloads\saida.xlsx"

# Extrair tabelas e salvar no Excel.
salvar_tabelas_em_excel(extrair_tabelas_pdf(pdf_file), xls_file)
