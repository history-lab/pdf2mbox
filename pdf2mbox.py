import argparse
import os.path
import sys
import magic
import xmpdf
import mailbox
import email.utils


class Mbox:
    def __init__(self, mbox_filename):
        self.mbox = mailbox.mbox(mbox_filename)

    def _encode(self, s):
        if s:
            return s.encode('ascii', errors='backslashreplace').decode('ascii')
        else:
            return ''

    def addmsg(self, em):
        self.mbox.lock()
        try:
            msg = mailbox.mboxMessage()
            msg.set_unixfrom(self._encode('Author' + self._encode(em.header.
                                                                  date)))
            msg['From'] = email.utils.formataddr(('Author', self._encode(
                                                  em.header.from_email)))
            msg['To'] = email.utils.formataddr(('Recipient', self._encode(
                                                em.header.to)))
            msg['Subject'] = self._encode(em.header.subject)
            msg.set_payload(self._encode(em.body))
            self.mbox.add(msg)
            self.mbox.flush()
        finally:
            self.mbox.unlock()


# CLI
parser = argparse.ArgumentParser(
            description='Generates an mbox from a PDF containing emails')
parser.add_argument('pdf_file', help='PDF file provided as input')
parser.add_argument('mbox_file', nargs='?', default='out.mbox',
                    help='Mbox file generated as output')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')
parser.add_argument('--csv', type=argparse.FileType('w', encoding='utf-8'),
                    help='generate CSV file output')
cl_args = parser.parse_args()
pdf_filename = cl_args.pdf_file
csv_filename = cl_args.csv
mbox_filename = cl_args.mbox_file

# File handling
if not os.path.exists(pdf_filename):
    sys.exit(f'error: {pdf_filename} does not exist.')
if not os.path.isfile(pdf_filename):
    sys.exit(f'error: {pdf_filename} is not a file.')
if magic.from_file(pdf_filename, mime=True) != 'application/pdf':
    sys.exit(f'error: {pdf_filename} is not a PDF file.')

om = xmpdf.Xmpdf(pdf_filename)
print(mbox_filename)
print(om.info())
mbox = Mbox(mbox_filename)
# mbox.addmsg(om.emails[0])
for i in range(100):
    print(i)
    mbox.addmsg(om.emails[i])
# print(om.to_json())
# if csv_filename:
#    om.to_csv(csv_filename)
