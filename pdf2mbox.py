import argparse
import os.path
import sys
import magic
import mailbox
import email.utils

# CLI
parser = argparse.ArgumentParser(
            description='Generates an mbox from a PDF containing emails')
parser.add_argument('pdf_file', help='PDF file provided as input')
parser.add_argument('mbox_file', help='Mbox file generated as output')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')
cl_args = parser.parse_args()
pdf_filename = cl_args.pdf_file
mbox_filename = cl_args.mbox_file

# PDF file handling
if not os.path.exists(pdf_filename):
    sys.exit(f'error: {pdf_filename} does not exist.')
if not os.path.isfile(pdf_filename):
    sys.exit(f'error: {pdf_filename} is not a file.')
if magic.from_file(pdf_filename, mime=True) != 'application/pdf':
    sys.exit(f'error: {pdf_filename} is not a PDF file.')

print(f'{pdf_filename} {mbox_filename}')
exit()

from_addr = email.utils.formataddr(('Author',
                                    'author@example.com'))
to_addr = email.utils.formataddr(('Recipient',
                                  'recipient@example.com'))

payload = '''This is the body.
From (will not be escaped).
There are 3 lines.
'''

mbox = mailbox.mbox(mbox_filename)
mbox.lock()
try:
    msg = mailbox.mboxMessage()
    msg.set_unixfrom('author Sat Feb  7 01:05:34 2009')
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = 'Sample message 1'
    msg.set_payload(payload)
    mbox.add(msg)
    mbox.flush()

    msg = mailbox.mboxMessage()
    msg.set_unixfrom('author')
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = 'Sample message 2'
    msg.set_payload('This is the second body.\n')
    mbox.add(msg)
    mbox.flush()
finally:
    mbox.unlock()

print(open(mbox_filename, 'r').read())
