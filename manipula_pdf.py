import PyPDF2

# file_pdf = "~/Downloads/CARMEN.pdf"
#
# with open(caminho_pdf, "rb") as pdf_origin:
#     reader_pdf = PyPDF2.PdfReader(pdf_origin)
#     writer_pdf = PyPDF2.PdfWriter()
#
#     page_being_deleted = 3  # página a ser deletada, começando com 0
#
#     for page in range(len(leitor_pdf.pages)):
#         if page > page_being_deleted:
#             writer_pdf.add_page(reader_pdf.pages[page])
#
#     with open("~/Downloads/CARMEN 2.pdf", "wb") as new_pdf:
#         writer_pdf.write(new_pdf)
#
# print("Página atualizada com sucesso!")

# ----------------------------------------------------------------------------

path_pdf = [
    "~/Downloads/CARMEN 1.pdf",
    "~/Downloads/CARMEN 2.pdf"
]

writer_pdf = PyPDF2.PdfWriter()

for pdf in path_pdf:
    reader_pdf = PyPDF2.PdfReader(pdf)
    for page in range(len(reader_pdf.pages)):
        writer_pdf.add_page(reader_pdf.pages[page])

with open("~/Downloads/CARMEN - PDF combinados.pdf", "wb") as pdf_combined:
    writer_pdf.write(pdf_combined)

print("Arquivos PDF combinados com sucesso!")
