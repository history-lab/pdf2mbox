# pdf2mbox
a command-line utility and Python package for converting PDF emails to MBOX format

## Installation

    pip install pdf2mbox

## Usage

    # from the command line
    % python -m pdf2mbox --help
    usage: pdf2mbox.py [-h] [--version] [--overwrite] [--csv [CSV]]
                       pdf_file [mbox_file]

    Generates an mbox from a PDF containing emails

    positional arguments:
      pdf_file         PDF file provided as input
      mbox_file        Mbox file generated as output

    optional arguments:
      -h, --help       show this help message and exit
      --version, -v    show program's version number and exit
      --overwrite, -o  overwrite MBOX file if it exists
      --csv [CSV]      generate CSV file output

      # from within python
      from pdf2mbox import pdf2mbox
      pe = pdf2mbox(pdf_file, mbox_file) # pe contains dict of emails

## Notes
* The initial development of this package was funded in part by The Mellon Foundation’s “Email Archives: Building Capacity and Community” program.
