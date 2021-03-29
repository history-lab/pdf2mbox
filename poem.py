"""poem (page-oriented e-mail) module

  Module contains functions for parsing text strings that
  represent pages in PDF files containing e-mails.
"""
HEADER_FIELDS = ['from', 'to', 'cc', 'bcc', 'subject', 'date', 'attachments']
HEADER_START_MAX = 12


def tokenizer(line):
    """Tokenizes a string if it represents an element of an email header"""
    line = line.strip()
    loc = line.find(':')
    if loc != -1:           # found :
        key = line[:loc]
        value = line[loc+1:].strip()
    else:
        key = value = ''
    return key, value


def parse(page):
    """Parses a string representing a page of an email. Returns a
       dictionary containng header elements (if exists), rest of page is
       considered the body."""
    ln = 0
    header = {}
    pgarr = page.splitlines()
    lncnt = len(pgarr)
    # find the start of the header
    while ln < HEADER_START_MAX and ln < lncnt:
        lhs, rhs = tokenizer(pgarr[ln])
        ln += 1
        if lhs.lower() in HEADER_FIELDS:
            header[lhs] = rhs
            break
    # parse header, if found
    while header:
        nlhs, rhs = tokenizer(pgarr[ln])
        ln += 1
        if nlhs or rhs:      # header continues
            if nlhs:         # new header component
                lhs = nlhs
                header[lhs] = rhs
            else:            # continuation of current component
                header[lhs] = header[lhs] + rhs
        else:  # both nlhs or rhs are null - blank line, end of Header
            break
    body = '\n'.join(pgarr[ln::])
    return header, body


def test_parse(pg):
    print('full page:')
    print(pg)
    header, body = parse(pg)
    print(f'header:')
    print(header)
    print(f'body:')
    print(body)

def main():
    example_page = """
    From:       yogi.bear@cartoon.com
    To:         booboo.bear@cartoon.com
    Subject:    this afternoon
    Date:       Thursday, March 25, 2021 06:16:10 AM

    Hi Booboo:

    Let's go see the ranger this afternoon at 2 o'clock, ok?

    Yogi
    """
    test_parse(example_page)


if __name__ == "__main__":
    main()
