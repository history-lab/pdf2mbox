from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class HeaderParser:
    field_tokens:   ClassVar[list[str]] = ['from', 'to', 'cc', 'bcc',
                                           'subject', 'date', 'attachments']
    max_start:      ClassVar[int] = 12


@dataclass
class Header:
    from_email:     str
    to:             list[str]
    subject:        str
    date:           str
    cc:             list[str] = field(default_factory=list)
    bcc:            list[str] = field(default_factory=list)
    attachments:    list[str] = field(default_factory=list)


@dataclass
class Email:
    header:         Header
    body:           str


def main():
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
