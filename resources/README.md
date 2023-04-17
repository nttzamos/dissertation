This folder contains all non-Python files needed for the execution of the application. Such files include:

* Icons (in SVG/PNG/ICO format) needed for various buttons
* The database of the application (and its backup)
* Translations for the Greek & English languages

Other than the aforementioned files, this folder is supposed to contain a `books` subfolder consisting of all the books from the 6 primary school education grades in PDF format. However, due to its large size this folder has not been uploaded to the project's repository.

These PDF files are referenced by the `shared/pdf_parser.py` file and were used to extract all text included in the books and save it to the text files inside the `unprocessed` folder (the corresponding ZIP files were then created manually).
