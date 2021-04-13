We're at a pre-release stage of development. You can monitor progress by watching [the repo](https://github.com/history-lab/pdf2mbox).

## motivation
Archivists and others involved in creating email archives for historical and research purposes are the intended users of pdf2mbox. 

Many emails released under Freedom of Information Act (FOIA) requests are in PDF format with a single PDF often containing hundreds of emails. Email archiving systems for historical research and preservation, such as ePADD and DArcMail, are natural destinations for FOIAed emails. Unfortunately, these systems don't currently accept PDFs as input, but they take MBOX as input. Thus, pdf2mbox will enable PDF emails to be processed by these solutions. Users will first convert email PDFs to MBOX using pdf2mbox as a pre-processing step.

Information is lost when exporting an email in PDF format from an email system. However, in most cases, we believe enough information is retained in an email PDF to create a proxy of the original email acceptable for use by historians and other researchers.

## usage
pdf2mbox is open source and distributed under the MIT license. Developed in Python, pdf2mbox will be available as a PyPI package and installable via `pip install pdf2mbox`. Here is how to run pdf2mbox as a command-line utility: 
```
% python pdf2mbox.py -h
usage: pdf2mbox.py [-h] [--version] pdf_file mbox_file

Generates an mbox from a PDF containing emails

positional arguments:
  pdf_file    PDF file provided as input
  mbox_file   Mbox file generated as output

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
```
  
## use cases
1. conversion of a single PDF
2. conversion of a directory of PDFs 

## about us
Columbia University's [History Lab](http://history-lab.org) is developing pdf2mbox as part of its **Creating Email Archives from PDFs: The Covid-19 Corpus** project.  The project is also developing an extensive collection of FOIAed emails on the initial governmental and public health response to the Covid-19 pandemic in the United States. This email collection will be accessible via: 
- a website interface with search and analytical tools
- an application programming interface (API)
- item-level catalog entries integrated into Columbia University Libraries' Government Information Portal

The project is funded in part by The Mellon Foundation's "Email Archives: Building Capacity and Community" program.
