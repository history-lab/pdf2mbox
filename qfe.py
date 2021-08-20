"""An example script showing how to query the Fauci emails"""
import psycopg2
import aiosql

conn = psycopg2.connect("")   # credentials via env vars and .psqlrc
conn.autocommit = True
db = aiosql.from_path("pdf2db.sql", "psycopg2")
emails_db = db.get_emails_in_file(conn, file_id=1000)
emails = []                   # list of dicts


def convert_dict(edb):
    "Convert query return for single row to dict"
    email = {}
    email['email_id'] = edb[0]
    email['file_pg_start'] = edb[1]
    email['pg_cnt'] = edb[2]
    email['header_begin_ln'] = edb[3]
    email['header_end_ln'] = edb[4]
    email['from_email'] = edb[5]
    email['to_emails'] = edb[6]
    email['cc_emails'] = edb[7]
    email['bcc_emails'] = edb[8]
    email['attachments'] = edb[9]
    email['importance'] = edb[10]
    email['subject'] = edb[11]
    email['sent'] = edb[12]
    email['body'] = edb[13]
    email['header_unprocessed'] = edb[14]
    return email


def display_email(email):
    "Prints out email in an email format"
    print(
        f'ID:      {email["email_id"]}, PG: {email["file_pg_start"]}\n\n'
        f'From:    {email["from_email"]} \n'
        f'Sent:    {email["sent"]} \n'
        f'To:      {email["to_emails"]} \n'
        f'CC:      {email["cc_emails"]} \n'
        f'Subject: {email["subject"]}\n\n'
        f'{email["body"]}\n\n')
    input('Hit <RETURN> to continue')
    return


for e in emails_db:
    ed = convert_dict(e)
    display_email(ed)
    emails.append(ed)
