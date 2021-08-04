import aiosql
import psycopg2
import os
# import pdfemail         # right now it's a symbolic link to pdf2mbox

PDFDIR = os.getenv('PDFDIR')
conn = psycopg2.connect("")
conn.autocommit = True
stmts = aiosql.from_path("pdf2db.sql", "psycopg2")

# pdfs = sql.get_dc19pdf_list(conn)
# for p in pdfs:
#    print(p[1])

#
# pdf_list = os.listdir(PDFDIR)
# print(pdf_list)
#
stmts.insert_email(conn, file_id=32, file_pg_start=1, pg_cnt=4,
                   header_begin_ln=2, header_end_ln=8, from_email='xx@abc.com',
                   to_emails='yyy@def.com', cc_emails='zzz@def.com',
                   attachments='a.pdf', importance='', subject='test email',
                   body='line1\nline2\nline3')
