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
