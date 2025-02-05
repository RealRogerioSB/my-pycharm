import PyPDF2

caminho_pdf = "~/Downloads/CARMEN.pdf"  # arquivo PDF original

with open(caminho_pdf, "rb") as pdf_original:
    leitor_pdf = PyPDF2.PdfReader(pdf_original)
    escritor_pdf = PyPDF2.PdfWriter()

    pagina_para_deletar = 3  # página a ser deletada, começando com 0

    for numero_pagina in range(len(leitor_pdf.pages)):
        if numero_pagina > pagina_para_deletar:
            escritor_pdf.add_page(leitor_pdf.pages[numero_pagina])

    with open("~/Downloads/CARMEN_new.pdf", "wb") as novo_pdf:  # arquivo PDF atualizado
        escritor_pdf.write(novo_pdf)

print("Página atualizada com sucesso!")
