import pgparse
import pdftotext
import magic
from os.path import basename


class PDF:
    def __init__(self, file_id, pdf_filename):
        self.file_id = file_id
        self.filename = pdf_filename
        self.filetype = magic.from_file(self.filename)
        self.emails = []
        # convert to text
        with open(self.filename, 'rb') as f:
            self.pdf = pdftotext.PDF(f)
            self.pgcnt = len(self.pdf)
        self.__parse()

    def __parse(self):
        i = 0
        current_email = None
        while i < self.pgcnt:
            page = pgparse.parse(self.pdf[i])
            i += 1
            if isinstance(page, pgparse.Email):
                if current_email:
                    self.emails.append(current_email)
                current_email = page
                current_email.pdf_filename = self.filename
                current_email.page_number = i
                current_email.page_count = 1
            elif (isinstance(page, pgparse.Page) and current_email):
                current_email.body += page.body
                current_email.page_count += 1
            if current_email:   # write last email
                self.emails.append(current_email)

    def get_summary(self):
        return f'{self.file_id}) {basename(self.filename)}: ' \
               f'{self.filetype}; ' \
               f'{self.pgcnt} pages, {len(self.emails)} emails'
