from dataclasses import dataclass, field
from typing import ClassVar
from collections import defaultdict
from mailbox import mbox, mboxMessage
from quopri import encodestring


@dataclass
class Header:
    from_email:     str
    to:             list[str]
    subject:        str
    date:           str
    cc:             list[str] = field(default_factory=list)
    bcc:            list[str] = field(default_factory=list)
    attachments:    list[str] = field(default_factory=list)
    begin_ln:       int = field(default_factory=int)   # start line number
    end_ln:         int = field(default_factory=int)   # finish line number


@dataclass
class Page:
    body:           str


@dataclass
class Email(Page):
    header:         Header
    pdf_filename:   str = field(default_factory=str)
    page_number:    int = field(default_factory=int)
    page_count:     int = field(default_factory=int)

    def add_mbox(self, mbox_file):
        print(self)
        return
        msg = mboxMessage()
        # set values
        tmbox = mbox(mbox_file)
        tmbox.lock()
        try:
            mbox_msg = mboxMessage(msg)
            mbox_msg.set_payload(encodestring(bytes(mbox_msg.get_payload(),
                                                    'utf-8')))
            mbox.add(mbox_msg)
            mbox.flush()
        finally:
            mbox.unlock()


@dataclass
class HeaderParser:
    pgarr:          list[str]
    _FIELD_TOKENS:  ClassVar[list[str]] = ['from', 'to', 'cc', 'bcc',
                                           'subject', 'date', 'sent',
                                           'attachments']
    _MAX_START:     ClassVar[int] = 12
    _header:        defaultdict(str) = field(
        default_factory=lambda: defaultdict(str))
    _ln:            int = 0                          # line position in page
    _token:         str = field(default_factory=str)  # last field token
    _lncnt:         int = 0                           # len(pgarr)

    def _find_start(self):
        self._ln = 0
        while (self._ln < self._MAX_START and self._ln < self._lncnt and
               self.pgarr[self._ln].find(':') == -1):
            self._ln += 1
            # print(f'in find start loop - ln: {self._ln}')
        if self._ln == self._MAX_START or self._ln == self._lncnt:
            return False    # Reached max header start position or page end
        else:
            self._header['begin_ln'] = self._ln
            return True     # Found the start of header

    def _tokenize(self):
        """Tokenizes a string if it represents an element of an email header"""
        line = self.pgarr[self._ln].strip()
        loc = line.find(':')
        if loc != -1:           # found add to header dictionary
            self._token = line[:loc].lower()
            if self._token in self._FIELD_TOKENS:
                self._header[self._token] = line[loc+1:].strip()
            else:
                print(f'Warning - unprocessed header element: {self._token}')
                print(line)
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
                      begin_ln=self._header['begin_ln'],
                      end_ln=self._header['end_ln'])

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
