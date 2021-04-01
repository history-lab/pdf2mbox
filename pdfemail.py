from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class PDFEmailHeader:
    from_email:     str
    to:             list[str]
    subject:        str
    date:           str
    cc:             list[str] = field(default_factory=list)
    bcc:            list[str] = field(default_factory=list)
    attachments:    list[str] = field(default_factory=list)
    # constants used in parsing
    field_tokens:   ClassVar[list[str]] = ['from', 'to', 'cc', 'bcc',
                                           'subject', 'date', 'attachments']
    max_start:      ClassVar[int] = 12


def main():
    e1 = PDFEmailHeader('yogi.bear@cartoon.com',
                        ['booboo.bear@cartoon.com'],
                        'this afternoon',
                        'Thursday, March 25, 2021 06:16:10 AM')
    print(e1)


if __name__ == "__main__":
    main()
