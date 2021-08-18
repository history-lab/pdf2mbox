import aiosql
import psycopg2
import os
import pdfparse

PDFDIR = os.getenv('PDFDIR')
conn = psycopg2.connect("")
conn.autocommit = True
db = aiosql.from_path("pdf2db.sql", "psycopg2")




pdfs = db.get_dc19pdf_list(conn)
for p in pdfs:
    f = pdfparse.PDF(PDFDIR + '/' + p[1], p[0])
    print(f.get_summary())

    db.upsert_file_stats(conn, file_id=f.file_id, pg_cnt=f.pgcnt,
                         email_cnt=len(f.emails), type_desc=f.filetype,
                         error_msg=f.error)

#  stmts.insert_email(conn, file_id=32, file_pg_start=1, pg_cnt=4,
#                     header_begin_ln=2, header_end_ln=8,
#                     from_email='xx@abc.com',
#                     to_emails='yyy@def.com', cc_emails='zzz@def.com',
#                     attachments='a.pdf', importance='', subject='test email',
#                     body='line1\nline2\nline3')
