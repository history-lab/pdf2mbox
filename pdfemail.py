from dataclasses import dataclass, field

# Used for parsing
HEADER_FIELDS = ['from', 'to', 'cc', 'bcc', 'subject', 'date', 'attachments']
HEADER_START_MAX = 12


@dataclass
class PDFEmailHeader:
    from_email:     str
    to:             list[str]
    subject:        str
    date:           str
    cc:             list[str] = field(default_factory=list)
    bcc:            list[str] = field(default_factory=list)
    attachments:    list[str] = field(default_factory=list)


def main():
    e1 = PDFEmailHeader('yogi.bear@cartoon.com',
                        ['booboo.bear@cartoon.com'],
                        'this afternoon',
                        'Thursday, March 25, 2021 06:16:10 AM')
    print(e1)


if __name__ == "__main__":
    main()
