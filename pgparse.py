from dataclasses import dataclass, field
from typing import ClassVar
from collections import defaultdict
from os.path import basename


@dataclass
class Header:
    from_email:     str
    to:             list[str]
    subject:        str
    date:           str
    cc:             list[str] = field(default_factory=list)
    bcc:            list[str] = field(default_factory=list)
    attachments:    list[str] = field(default_factory=list)
    importance:     str = field(default_factory=str)
    begin_ln:       int = field(default_factory=int)   # start line number
    end_ln:         int = field(default_factory=int)   # finish line number
    unprocessed:    list[str] = field(default_factory=list)


@dataclass
class Page:
    body:           str


@dataclass
class Email(Page):
    header:         Header
    pdf_filename:   str = field(default_factory=str)
    page_number:    int = field(default_factory=int)
    page_count:     int = field(default_factory=int)

    def get_summary(self):
        summary = f'{basename(self.pdf_filename)}: ' \
                  f'{self.page_number}, {self.page_count}; ' \
                  f'{self.header.subject};' \
                  f'{self.header.from_email}; {self.header.to}'
        return summary


@dataclass
class HeaderParser:
    pgarr:          list[str]
    _FIELD_TOKENS:  ClassVar[list[str]] = ['from', 'to', 'cc', 'bcc',
                                           'subject', 'date', 'sent',
                                           'importance', 'attachments']
    _MAX_START_LN:     ClassVar[int] = 12        # max start line for header
    _MAX_COL_COLON: ClassVar[int] = 14        # rt most column for header colon
    _header:        defaultdict(str) = field(
        default_factory=lambda: defaultdict(str))
    _ln:            int = 0                           # line position in page
    _token:         str = field(default_factory=str)  # last field token
    _lncnt:         int = 0                           # len(pgarr)

    def _get_token(self, str):
        # fix erroneous OCR spaces
        return str.lower().replace(' ', '')

    def _find_start(self):
        self._ln = 0
        while True:
            if self._ln == self._MAX_START_LN:  # reached _MAX_START_LN
                return False
            if self._ln == self._lncnt:         # reached end of page
                return False
            loc = self.pgarr[self._ln][:self._MAX_COL_COLON].find(':')
            if loc != -1:
                self._token = self._get_token(self.pgarr[self._ln][:loc])
                if self._token in self._FIELD_TOKENS:
                    return True     # Found the start of header
            self._ln += 1

    def _tokenize(self):
        """Tokenizes a string if it represents an element of an email header"""
        line = self.pgarr[self._ln].strip()
        loc = line.find(':')
        if loc != -1:           # found add to header dictionary
            # self._token = line[:loc].lower().replace(' ', '')
            self._token = self._get_token(line[:loc])
            if self._token in self._FIELD_TOKENS:
                self._header[self._token] = line[loc+1:].strip()
            else:
                if self._header['unprocessed']:
                    self._header['unproccessed'] = \
                     self._header['unprocessed'].append(line)
                else:
                    self._header['unprocessed'] = [line]
                # print(f'Warning - unprocessed header element: {self._token}')
                # print(line)
        elif self._token in self._FIELD_TOKENS:
            # existing token value carried onto next line
            self._header[self._token] += line

    def _next_line(self):
        """Returns True if there is another line in the header.
           False otherwise. Side effect: always increments ln."""
        self._ln += 1
        if self._ln >= self._lncnt:                # Reached end of page
            return False
        elif self.pgarr[self._ln].strip() == '':   # Blank line indicates EOH
            return False
        else:
            return True

    def _convert_obj(self):
        """Create a PDFEmailHeader object based on the contents of the
        self._header dictionary. If required fields are missing, it raises
        warnings and returns None."""
        if not self._header['date']:
            self._header['date'] = self._header['sent']
        return Header(from_email=self._header['from'],
                      to=self._header['to'],
                      cc=self._header['cc'],
                      bcc=self._header['bcc'],
                      subject=self._header['subject'],
                      date=self._header['date'],
                      attachments=self._header['attachments'],
                      importance=self._header['importance'],
                      begin_ln=self._header['begin_ln'],
                      end_ln=self._header['end_ln'],
                      unprocessed=self._header['unprocessed'])

    def parse(self):
        self._lncnt = len(self.pgarr)         # lines in page
        if self._find_start():                # find the start of the header
            while True:                       # while in header
                self._tokenize()              # process header line
                if not self._next_line():     # end of header
                    break
            self._header['end_ln'] = self._ln
            header_obj = self._convert_obj()  # convert _header to object
            return header_obj
        else:                                 # no header
            return None


def parse(page):
    """Parses a string representing a PDF page. returns either a Page object or
    an Email object depending on whether the page has an email header."""
    pgarr = page.splitlines()
    hp = HeaderParser(pgarr)
    header = hp.parse()
    if header:
        body = '\n'.join(pgarr[header.end_ln::])
        return Email(header=header, body=body)
    else:
        body = '\n'.join(pgarr)
        return Page(body=body)


def main():
    example_page = """
    From:       yogi.bear@cartoon.com
    To:         booboo.bear@cartoon.com
    Subject:    this afternoon
    Date:       Thursday, March 25, 2021 06:16:10 AM
    Status:     Urgent

    Hi Booboo:

    Let's go see the ranger this afternoon at 2 o'clock, ok?

    Yogi
    """
    pg = parse(example_page)
    print(type(pg))
    print(pg)
    example_page = """
    Up next:

    This is an example of a continuation page, which occurs when an email
    extends beyond a page.

    Thanks,
    Yogi
    """
    pg = parse(example_page)
    print(type(pg))
    print(pg)

    exit()
    e1 = Email(header=Header(from_email='yogi.bear@cartoon.com',
                             to=['booboo.bear@cartoon.com'],
                             subject='this afternoon',
                             date='Thursday, March 25, 2021 06:16:10 AM'),
               body="""Hi Booboo:

               Let's go see the ranger this afternoon at 2 o'clock, ok?

               Yogi""")
    print(e1)


if __name__ == "__main__":
    main()
