import argparse
import os.path
import sys
import magic
import pdftotext
import quopri
import email
import email.utils
import mailbox

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

# Extract text from pdf
with open(pdf_filename, 'rb') as f:
    pdf = pdftotext.PDF(f)

# pdf_page = io.StringIO()
pdf_page = pdf[0]

# print(pdf_page)
# print(type(pdf_page))
msg = email.message_from_string(pdf_page)
i = 0
for k, v in msg.items():
    i += 1
    print(f'{i}. msg[{k}] {v}')
print(msg.get_payload())
print(f'{pdf_filename} {mbox_filename}')

mbox = mailbox.mbox(mbox_filename)
mbox.lock()
try:
    mbox_msg = mailbox.mboxMessage(msg)
    mbox_msg.set_payload(quopri.encodestring(bytes(mbox_msg.get_payload(),
                                                   'utf-8')))
    mbox.add(mbox_msg)
    mbox.flush()
finally:
    mbox.unlock()

msg_read = open(mbox_filename, 'r').read()
print(type(msg_read))
# print(open(mbox_filename, 'r').read())
