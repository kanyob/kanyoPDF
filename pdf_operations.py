import os
from pathlib import Path
from tkinter import filedialog, messagebox

from pypdf import PdfReader, PdfWriter




def merge_pdfs(pdf_files):
    
    # Merge PDFs
    if not pdf_files:
        messagebox.showwarning(
            "Üres lista",
            "Adj hozzá PDF fájlokat."
        )
        return False

    # Where to save the merged
    output_path = filedialog.asksaveasfilename(
        title="KanyoPDF-Merge",
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not output_path:
        return False  #cancelled

    try:
        pdf_writer = PdfWriter()

        # Read the pdfs and add to the columns.
        for pdf_data in pdf_files:

            try:
                pdf_reader = PdfReader(pdf_data['filepath'])
                total_pages = len(pdf_reader.pages)

                # Get page range
                from_page = max(1, min(pdf_data['from_page'], total_pages))
                to_page = max(1, min(pdf_data['to_page'], total_pages))

                # Ensure from_page <= to_page
                if from_page > to_page:
                    from_page, to_page = to_page, from_page

                # Add specified page range (convert to 0-indexed)
                for page_num in range(from_page - 1, to_page):
                    pdf_writer.add_page(pdf_reader.pages[page_num])

            except Exception as e:
                messagebox.showerror(
                    "Hiba",
                    f"Nem sikerült a {pdf_data['filename']} hozzáadni:\n{str(e)}"
                )
                return False

        # Check if pages were added
        if len(pdf_writer.pages) == 0:
            messagebox.showwarning(
                "Hiba",
                "Nem voltak odldalak kiváalsztva."
            )
            return False

        # Write the merged PDF

        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)

        messagebox.showinfo(
            "Sikeres",
            f"A fájl helye: {output_path}"
        )
        return True

    except Exception as e:
        messagebox.showerror(
            "Hiba",
            f"Hiba történt:\n{str(e)}"
        )
        return False


def split_from_table(pdf_files):

    # Merge PDFs
    if not pdf_files:
        messagebox.showwarning(
            "Üres lista",
            "Adj hozzá PDF fájlokat"
        )
        return False

    # Where to save the merged
    output_dir = filedialog.askdirectory(
        title="Szétválasztás"
    )

    if not output_dir:
        return False  #cancelled
    

    total_pages_split = 0

    try:
        # Process each PDF in the table
        for pdf_data in pdf_files:

                pdf_reader = PdfReader(pdf_data['filepath'])
                total_pages = len(pdf_reader.pages)

                # Get page range (1-indexed from user, convert to 0-indexed)
                from_page = max(1, min(pdf_data['from_page'], total_pages))
                to_page = max(1, min(pdf_data['to_page'], total_pages))

                # Ensure from_page <= to_page
                if from_page > to_page:
                    from_page, to_page = to_page, from_page

                # Get the base filename without extension
                base_name = Path(pdf_data['filepath']).stem

                # Split each page in the range into a separate file
                for page_num in range(from_page - 1, to_page):
                    pdf_writer = PdfWriter()
                    pdf_writer.add_page(pdf_reader.pages[page_num])

                    # Create output filename 
                    output_filename = f"{base_name}_szetvalogatva.pdf"
                    output_path = os.path.join(output_dir, output_filename)

                    # Write the page to a file
                    with open(output_path, 'wb') as output_file:
                        pdf_writer.write(output_file)

                    total_pages_split += 1


        if total_pages_split > 0:
            messagebox.showinfo(
                "Sikeres",
                f"Sikeresen szétválasztottál {total_pages_split} oldalt!\n\n"
                f"Fájlok helye: {output_dir}"
            )
            return True

    except Exception as e:
        messagebox.showerror(
            "Hiba",
            f"Próbáld újra:\n{str(e)}"
        )
        return False


