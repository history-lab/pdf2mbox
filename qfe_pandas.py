"""An example script showing how to query the Fauci emails"""
import psycopg2
import pandas as pd

conn = psycopg2.connect("")   # credentials via env vars or .psqlrc

query = """
select email_id, file_pg_start, pg_cnt, header_begin_ln, header_end_ln,
    from_email, to_emails, cc_emails, bcc_emails, attachments, importance,
    subject, sent, body, header_unprocessed
from covid19.emails
where file_id = 1000;
"""

fe = pd.read_sql(query, conn)
print(fe.head())
