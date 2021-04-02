"""poem (page-oriented e-mail) module

  Module contains functions for parsing text strings that
  represent pages in PDF files containing e-mails.
"""

import pdfemail


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


def _find_header(pgarr):
    """Return location where header begins, 0 if not found."""
    ln = 0
    lncnt = len(pgarr)
    # find the start of the header
    while ln < pdfemail.HeaderParser.max_start and ln < lncnt:
        lhs, rhs = tokenizer(pgarr[ln])
        if lhs.lower() in pdfemail.HeaderParser.field_tokens:
            break
        ln += 1
    else:                   # header not found
        ln = 0
    return ln


def _parse_header(pgarr, ln):
    header = {}
    while True:
        nlhs, rhs = tokenizer(pgarr[ln])
        if nlhs or rhs:
            if nlhs:         # new header component
                lhs = nlhs
                header[lhs] = rhs
            else:            # continuation of current component
                header[lhs] = header[lhs] + rhs
        else:  # both nlhs or rhs are null - blank line, end of Header
            break
        ln += 1
    return header, ln


def parse(page):
    """Parses a string representing a page of an email. Returns a
       dictionary containng header elements (if exists), rest of page is
       considered the body."""
    pgarr = page.splitlines()
    header = {}
    ln = _find_header(pgarr)
    # parse header, if found
    if ln:               # header found, parse it
        header, ln = _parse_header(pgarr, ln)
    body = '\n'.join(pgarr[ln::])
    return header, body


def parse2(page):
    """Parses a string representing a page of an email. Returns a
       dictionary containng header elements (if exists), rest of page is
       considered the body."""
    pgarr = page.splitlines()
    header = {}
    ln = _find_header(pgarr)
    # parse header, if found
    if ln:               # header found, parse it
        header, ln = _parse_header(pgarr, ln)
    body = '\n'.join(pgarr[ln::])
    return header, body


def _test_parse(pg):
    print('full page:')
    print(pg)
    header, body = parse(pg)
    print('header:')
    print(header)
    print('body:')
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
    _test_parse(example_page)
    example_page = """
    This is an example of a continuation page, which occurs when an email
    extends beyond a page.

    Thanks,
    Yogi
    """
    _test_parse(example_page)


if __name__ == "__main__":
    main()
