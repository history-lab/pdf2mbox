"""setup.py: the pacakging definitions."""
from setuptools import setup
import os


def get_long_description():
    """Generate the long description from the README.md contents."""
    with open(
        os.path.join(os.path.dirname(__file__), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(name="pdf2mbox",
      version="0.3.2",
      python_requires=">=3.8",
      long_description=get_long_description(),
      long_description_content_type="text/markdown",
      description="Extracts email metadata and text from a PDF file",
      author="Ben Lis, History Lab @ Columbia University",
      url="https://history-lab.github.io/pdf2mbox/",
      license="MIT License",
      install_requires=["xmpdf", "python-magic"],
      py_modules=["pdf2mbox"])
