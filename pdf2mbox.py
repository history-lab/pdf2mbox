import argparse
import os.path
import sys
import magic
import pdfparse
import aiosql
import psycopg2


# CLI
parser = argparse.ArgumentParser(
            description='Generates an mbox from a PDF containing emails')
parser.add_argument('pdf_file', help='PDF file provided as input')
parser.add_argument('mbox_file', help='Mbox file generated as output')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')
parser.add_argument('--csv', type=argparse.FileType('w', encoding='utf-8'),
                    help='generate CSV file output')
cl_args = parser.parse_args()
pdf_filename = cl_args.pdf_file
mbox_filename = cl_args.mbox_file
csv_filename = cl_args.csv

# File handling
if not os.path.exists(pdf_filename):
    sys.exit(f'error: {pdf_filename} does not exist.')
if not os.path.isfile(pdf_filename):
    sys.exit(f'error: {pdf_filename} is not a file.')
if magic.from_file(pdf_filename, mime=True) != 'application/pdf':
    sys.exit(f'error: {pdf_filename} is not a PDF file.')

# set up DB connection
conn = psycopg2.connect("")
conn.autocommit = True
db = aiosql.from_path("pdf2db.sql", "psycopg2")


# do that thing
# emails = pdfparse.parse(pdf_filename)
PDFDIR = os.getenv('PDFDIR')
pdfs = db.get_dc19pdf_list(conn)
for p in pdfs:
    f = pdfparse.PDF(PDFDIR + '/' + p[1], p[0])
    print(f.get_summary())
    db.upsert_file_stats(conn, file_id=f.file_id, pg_cnt=f.pgcnt,
                         email_cnt=len(f.emails), type_desc=f.filetype,
                         error_msg=f.error)
    for e in f.emails:
        # print(e.get_summary())  - TODO: make this run with verbose
        try:
            db.insert_email(conn, file_id=f.file_id,
                            file_pg_start=e.page_number, pg_cnt=e.page_count,
                            header_begin_ln=e.header.begin_ln,
                            header_end_ln=e.header.end_ln,
                            from_email=e.header.from_email,
                            to_emails=e.header.to,
                            cc_emails=e.header.cc, bcc_emails=e.header.bcc,
                            attachments=e.header.attachments,
                            importance=e.header.importance, sent=e.header.date,
                            subject=e.header.subject, body=e.body,
                            header_unprocessed=e.header.unprocessed)
        except Exception as exc:
            print(f'{e.page_number}: {exc}')
            continue
# pdf.write_csv(csv_filename)
