# pdf2mbox
a command-line utility and Python package for converting PDF emails to MBOX
format

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

## OS Dependencies
If you encounter errors installing pdf2mbox, please check the OS-level
dependencies of both the [pdftotext](https://pypi.org/project/pdftotext/)
and [python-magic](https://pypi.org/project/python-magic/) packages to ensure
you have the required libraries installed, as pdf2mbox utilizes both these
packages.

## Notes
* Assumes an email ends when a new email begins
* Works best with a standard email header (i.e., From:, To:, Sent:, Subject:)
* The initial development of this package was funded in part by The Mellon
Foundation’s “Email Archives: Building Capacity and Community” program.
