import aiosql
import psycopg2
from PyPDF2 import PdfFileReader, PdfFileWriter
INPUT_PDF_FILE = "./test/input/leopold-nih-foia-anthony-fauci-emails.pdf"
OUTPUT_FILE_PREFIX = "./test/pdf-previews/fauci_"


def gen_pdf_preview(pg_number):
    print(pg_number)
    idx = pg_number - 1
    pg = input_pdf.getPage(idx)
    pdf_writer = PdfFileWriter()
    pdf_writer.addPage(pg)
    with open(f'{OUTPUT_FILE_PREFIX}{pg_number}.pdf', 'wb') as output_pdf:
        pdf_writer.write(output_pdf)


input_pdf = PdfFileReader(INPUT_PDF_FILE)
conn = psycopg2.connect("")
conn.autocommit = True
db = aiosql.from_path("pdf2db.sql", "psycopg2")
emails = db.get_fauci_emails_pg_start(conn)
for e in emails:
    gen_pdf_preview(e[0])
