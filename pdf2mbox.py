"""pdf2mbox.py: Code file."""
import argparse
import os.path
import sys
import magic
import xmpdf
import mailbox
import importlib


class Mbox:
    """
    A class the represents an MBOX.

    ...
    Attributes
    ----------
    mbox_filename : str
        File name of associated MBOX

    Methods
    -------
    addmsg(em):
        Adds email to mbox
    """

    def __init__(self, mbox_filename):
        """
        Create Mbox and associates it with mbox_filename.

        Creates mbox_filename if it doesn't exist. Opens and appends if exists.
        """
        self.mbox = mailbox.mbox(mbox_filename)

    def _encode(self, s):
        """Replace non-ASCII characters."""
        if s:
            return s.encode('ascii', errors='backslashreplace').decode('ascii')
        else:
            return ''

    def addmsg(self, em):
        """Convert an Xmpdf email to mboxMessage format and add to MBOX."""
        self.mbox.lock()
        try:
            msg = mailbox.mboxMessage()
            msg.set_unixfrom(self._encode('Author' + self._encode(em.header.
                                                                  date)))
            msg['Date'] = em.header.date
            msg['From'] = self._encode(em.header.from_email)
            msg['To'] = self._encode(em.header.to)
            msg['Subject'] = self._encode(em.header.subject)
            msg.set_payload(self._encode(em.body))
            self.mbox.add(msg)
            self.mbox.flush()
        finally:
            self.mbox.unlock()


def pdf2mbox(pdf_filename, mbox_filename):
    """Extract emails from PDF file and store in MBOX File.

    Parameters
    ----------
    pdf_filename: str
        Name of PDF containing emails.
    mbox_filename: str
        Name of MBOX file that is destination for emails.

    Returns
    -------
    obj
        instance of Xmpdf class; contain representation of email collection
    """
    xms = xmpdf.Xmpdf(pdf_filename)
    mbox = Mbox(mbox_filename)
    for e in xms.emails:
        mbox.addmsg(e)
    return xms


# CLI
def cli():
    """Process command line arguments."""
    parser = argparse.ArgumentParser(description='Generates an mbox from a PDF \
    containing emails')
    parser.add_argument('pdf_file', help='PDF file provided as input')
    parser.add_argument('mbox_file', nargs='?', default='out.mbox',
                        help='Mbox file generated as output')
    parser.add_argument('--version', '-v', action='version',
                        version=f"%(prog)s \
                        {importlib.metadata.version('pdf2mbox')}")
    parser.add_argument('--overwrite', '-o', action="store_true",
                        help='overwrite MBOX file if it exists')
    parser.add_argument('--csv', nargs='?', const='out.csv',
                        type=argparse.FileType('w', encoding='utf-8'),
                        help='generate CSV file output')
    cl_args = parser.parse_args()
    pdf_filename = cl_args.pdf_file
    csv_filename = cl_args.csv
    mbox_filename = cl_args.mbox_file
    mbox_overwrite = cl_args.overwrite
    # File handling
    # PDF file
    if not os.path.exists(pdf_filename):
        sys.exit(f'error: {pdf_filename} does not exist.')
    if not os.path.isfile(pdf_filename):
        sys.exit(f'error: {pdf_filename} is not a file.')
    if magic.from_file(pdf_filename, mime=True) != 'application/pdf':
        sys.exit(f'error: {pdf_filename} is not a PDF file.')
    # MBOX
    if os.path.exists(mbox_filename):
        if mbox_overwrite:
            print(f'Overwriting {mbox_filename}')
            os.remove(mbox_filename)
        else:
            print(f'Appending email messages to {mbox_filename}')
    else:
        print(f'Writing email messages in MBOX format to {mbox_filename}')
    # csv
    if csv_filename:
        print(f'Writing csv to {csv_filename.name}')
    return pdf_filename, mbox_filename, csv_filename


if __name__ == '__main__':
    pdf_filename, mbox_filename, csv_filename = cli()
    xms = pdf2mbox(pdf_filename, mbox_filename)
    print(xms.info())
    if csv_filename:
        xms.to_csv(csv_filename)
