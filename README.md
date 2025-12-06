# kanyoPDF

PDF editor with merge and splti function.
If you are working with pdfs with only those functions (like me :D) its a good option for you.

## Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)
- pypdf

## Installation

**pip install -r requirements.txt**
(It will download pypdf and ttkthemese librarys)

## Usage

To run the application you can write **python kanyoPDF.py** or you can also double click kanyoPDF file in the folder if you downloaded it.

## Functions

**Merge PDFS**

**Split PDFS**

**Split ranged PDFS**

**Merge ranged PDFS**

**Delete PDFS by line**

**Delete all PDFS line**

## Saved file names

Splitted saved file names will be: {base_name}_szetvalogatva.pdf  (pdf_operations.py)

## Arcitecture

**app_ui.py - GUI components and the app**

**pdf_operations.py - Split and Merge functions**

**theme.py - colors and theme setup**

**kanyoPDF.py - Entrypoint to the app**



