import pgparse
import pdftotext

emails = []


def parse(pdf_filename):
    with open(pdf_filename, 'rb') as f:
        pdf = pdftotext.PDF(f)
    pgcnt = len(pdf)
    print(f'PDF page count: {pgcnt}')
    i = 0
    current_email = None
    while i < pgcnt:
        page = pgparse.parse(pdf[i])
        i += 1
        if isinstance(page, pgparse.Email):
            if current_email:
                emails.add(current_email)
            current_email = page
            current_email.pdf_filename = pdf_filename
            current_email.page_number = i
            current_email.page_count = 1
        elif (isinstance(page, pgparse.Page) and current_email):
            current_email.body += page.body
            current_email.page_count += 1
    if current_email:   # write last email
        emails.add(current_email)
    else:
        print('Warning: No emails found in PDF.')
