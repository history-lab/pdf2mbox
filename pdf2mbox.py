import argparse
import os.path
import sys
import magic
import pdftotext
import pdfemail

# CLI
parser = argparse.ArgumentParser(
            description='Generates an mbox from a PDF containing emails')
parser.add_argument('pdf_file', help='PDF file provided as input')
parser.add_argument('mbox_file', help='Mbox file generated as output')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')
cl_args = parser.parse_args()
pdf_filename = cl_args.pdf_file
mbox_filename = cl_args.mbox_file

# File handling
if not os.path.exists(pdf_filename):
    sys.exit(f'error: {pdf_filename} does not exist.')
if not os.path.isfile(pdf_filename):
    sys.exit(f'error: {pdf_filename} is not a file.')
if magic.from_file(pdf_filename, mime=True) != 'application/pdf':
    sys.exit(f'error: {pdf_filename} is not a PDF file.')


def convert(pdf_filename, mbox_filename):
    with open(pdf_filename, 'rb') as f:
        pdf = pdftotext.PDF(f)
        pgcnt = len(pdf)
        print(f'PDF page count: {pgcnt}')
        i = 0
        current_email = None
        while i < pgcnt:
            page = pdfemail.parse(pdf[i])
            i += 1
            if isinstance(page, pdfemail.Email):
                if current_email:
                    current_email.add_mbox(mbox_filename)
                current_email = page
                current_email.pdf_filename = pdf_filename
                current_email.page_number = i
                current_email.page_count = 1
            elif (isinstance(page, pdfemail.Page) and current_email):
                current_email.body += page.body
                current_email.page_count += 1
        if current_email:   # write last email
            current_email.add_mbox(mbox_filename)
        else:
            print('Warning: No emails found in PDF.')


if __name__ == "__main__":
    convert(pdf_filename, mbox_filename)
