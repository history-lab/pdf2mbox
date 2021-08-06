import argparse
import os.path
import sys
import magic
import pdfparse

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
if csv_filename:
    print(csv_filename)

# do that thing
# emails = pdfparse.parse(pdf_filename)
pdf = pdfparse.PDF(pdf_filename)
print(pdf.get_summary())

for e in pdf.emails:
    print(e.get_summary())
