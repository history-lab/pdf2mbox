import aiosql
import psycopg2
import requests
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
# INPUT_PDF_FILE = "./test/input/leopold-nih-foia-anthony-fauci-emails.pdf"
# OUTPUT_FILE_PREFIX = "./test/pdf-previews/fauci_"
OUTPUT_DIR = "./test/pdf-previews/dc19/"
TMP_DIR = "./test/tmp/"


def download_pdf(url, dfile):
    response = requests.get(url)
    with open(dfile, 'wb') as f:
        f.write(response.content)


def gen_pdf_preview(file_name, pg_number):
    idx = pg_number - 1
    pg = input_pdf.getPage(idx)
    pdf_writer = PdfFileWriter()
    pdf_writer.addPage(pg)
    with open(f'{OUTPUT_DIR}{file_name}-{pg_number}.pdf', 'wb') as output_pdf:
        pdf_writer.write(output_pdf)


conn = psycopg2.connect("")
conn.autocommit = True
db = aiosql.from_path("pdf2db.sql", "psycopg2")
emails = db.get_dc19_emails_pg_start(conn)
for e in emails:
    file_id, source_url, foiarchive_file, pg_list = e
    print(f'{file_id}, {source_url}, {foiarchive_file}')
    tmpfile = TMP_DIR + foiarchive_file
    download_pdf(source_url, tmpfile)
    input_pdf = PdfFileReader(tmpfile, strict=False)
    for p in pg_list:
        # print(f'*** generating new email starting on pg {p}')
        file_name = foiarchive_file[:-4]
        gen_pdf_preview(file_name, p)
    os.remove(tmpfile)
