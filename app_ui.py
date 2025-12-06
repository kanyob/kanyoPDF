import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from pypdf import PdfReader, PdfWriter


from theme import setup_theme
from pdf_operations import merge_pdfs, split_from_table



class pdfApp:
    def __init__(self, root):
        self.root = root
        self.root.title("kanyoPDF")
        self.root.geometry("1000x600")
        self.root.maxsize(1000,600)
        self.root.minsize(1000,600)

        # Store PDF file data as list of dictionaries
        #filepath, filename, pages, from_page, to_page,
        self.pdf_files = []

        # Store row widgets for management
        self.row_widgets = []

        # Configure theme and get color palette
        self.colors = setup_theme(self.root)

        # Create the main content area
        self.create_main_content()

    def create_main_content(self):
        # Main content
        main_container = ttk.Frame(self.root, style="Main.TFrame", padding=20)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Top action bar
        self.create_action_bar(main_container)

        # Table/Grid area
        self.create_table_area(main_container)

        # Bottom action bar for merge/split operations
        self.create_bottom_action_bar(main_container)

    def create_action_bar(self, parent):
        """Create the top horizontal action bar."""
        action_frame = ttk.Frame(parent, style="Main.TFrame")
        action_frame.pack(fill=tk.X, pady=(0, 15))

        #  Add Files
        add_btn = tk.Button(
            action_frame,
            text="Fájlok hozzáadása",
            command=self.add_files,
            bg=self.colors['primary'],
            fg='#FFFFFF',
            font=('Segoe UI', 10, 'bold'),
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            activebackground=self.colors['primary_hover'],
            activeforeground='#FFFFFF',
            borderwidth=0,
            highlightthickness=0
        )
        add_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Hover effect for primary button
        add_btn.bind('<Enter>', lambda e: add_btn.config(bg=self.colors['primary_hover']))
        add_btn.bind('<Leave>', lambda e: add_btn.config(bg=self.colors['primary']))

        # Clear List
        clear_btn = tk.Button(
            action_frame,
            text="Lista törlése",
            command=self.clear_list,
            bg=self.colors['primary'],
            fg=self.colors['text'],
            font=('Segoe UI', 10, 'bold'),
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            activebackground=self.colors['primary_hover'],
            activeforeground=self.colors['text'],
            borderwidth=0,
            highlightthickness=0
        )
        clear_btn.pack(side=tk.LEFT)

        # Hover effect for "Lista törlése" button
        clear_btn.bind('<Enter>', lambda e: clear_btn.config(bg=self.colors['primary_hover']))
        clear_btn.bind('<Leave>', lambda e: clear_btn.config(bg=self.colors['primary']))

    def create_bottom_action_bar(self, parent):
        """Create the bottom action bar for merge/split operations."""
        action_frame = ttk.Frame(parent, style="Main.TFrame")
        action_frame.pack(fill=tk.X, pady=(15, 0))

        # Merge PDFs button
        merge_btn = tk.Button(
            action_frame,
            text="PDF-ek Összeolvasztás",
            command=self.merge_pdfs,
            bg=self.colors['primary'],
            fg='#FFFFFF',
            font=('Segoe UI', 10, 'bold'),
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            activebackground=self.colors['primary'],
            activeforeground=self.colors['primary_hover'],
            borderwidth=0,
            highlightthickness=0
        )
        merge_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Hover effect for merge button
        merge_btn.bind('<Enter>', lambda e: merge_btn.config(bg=self.colors['primary_hover']))
        merge_btn.bind('<Leave>', lambda e: merge_btn.config(bg=self.colors['primary']))

        # Split PDF button
        split_btn = tk.Button(
            action_frame,
            text="PDF-ek Szétválasztása",
            command=self.split_pdf,
            bg=self.colors['primary'],
            fg='#FFFFFF',
            font=('Segoe UI', 10, 'bold'),
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            activebackground=self.colors['primary'],
            activeforeground='#FFFFFF',
            borderwidth=0,
            highlightthickness=0
        )
        split_btn.pack(side=tk.LEFT)

        # Hover effect for split button
        split_btn.bind('<Enter>', lambda e: split_btn.config(bg=self.colors['primary_hover']))
        split_btn.bind('<Leave>', lambda e: split_btn.config(bg=self.colors['primary']))

    def create_table_area(self, parent):
        """Create the table/grid for PDF files."""
        # Container with dark background
        table_container = ttk.Frame(parent, style="Surface.TFrame")
        table_container.pack(fill=tk.BOTH, expand=True)

        # Create canvas and scrollbar for custom table
        canvas = tk.Canvas(
            table_container,
            bg=self.colors['surface'],
            highlightthickness=0,
            borderwidth=0
        )
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=canvas.yview)

        # Scrollable frame
        self.scrollable_frame = ttk.Frame(canvas, style="Surface.TFrame")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack scrollbar and canvas
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Store canvas reference
        self.canvas = canvas

        # Create table header
        self.create_table_header()

    def create_table_header(self):
        """Create the table header row."""
        header_frame = ttk.Frame(self.scrollable_frame, style="Surface.TFrame")
        header_frame.pack(fill=tk.X, padx=20, pady=(15, 5))

        # column configs
        columns = [
            ("#", 10),
            ("Fájl neve", 300),
            ("Oldalak", 70),
            ("Oldal választás", 100),
            ("Törlés", 70)
        ]

        for label, width in columns:
            header = tk.Label(
                header_frame,
                text=label,
                font=('Segoe UI', 11, 'bold'),
                fg=self.colors['text_secondary'],
                bg=self.colors['surface'],
                anchor='w'
            )
            header.pack(side=tk.LEFT, padx=5)
            header.config(width=int(width/7)) 

        # Add seperator line () 
        separator = tk.Frame(
            self.scrollable_frame,
            bg=self.colors['border'],
            height=1
        )
        separator.pack(fill=tk.X, padx=20, pady=(5, 10))

    def create_table_row(self, index, filename, pages, from_page=1, to_page=None,):
        """Create a single table row."""
        if to_page is None:
            to_page = pages

        row_frame = ttk.Frame(self.scrollable_frame, style="Surface.TFrame")
        row_frame.pack(fill=tk.X, padx=20, pady=2)

        # Add subtle hover effect
        def on_enter(e):
            row_frame.config(style="Main.TFrame")

        def on_leave(e):
            row_frame.config(style="Surface.TFrame")

        row_frame.bind('<Enter>', on_enter)
        row_frame.bind('<Leave>', on_leave)

        # Index column (#)
        index_label = tk.Label(
            row_frame,
            text=str(index),
            font=('Segoe UI', 11),
            fg=self.colors['text_secondary'],
            bg=self.colors['surface'],
            width=2,
            anchor='w'
        )
        index_label.pack(side=tk.LEFT, padx=5)

        # File name column
        filename_label = tk.Label(
            row_frame,
            text=filename,
            font=('Segoe UI', 11),
            fg=self.colors['text'],
            bg=self.colors['surface'],
            width=50,
            anchor='w'
        )
        filename_label.pack(side=tk.LEFT, padx=5)

        # Pages column
        pages_label = tk.Label(
            row_frame,
            text=str(pages),
            font=('Segoe UI', 11),
            fg=self.colors['text'],
            bg=self.colors['surface'],
            width=10,
            anchor='w'
        )
        pages_label.pack(side=tk.LEFT, padx=5)

        # Range column (from - to)
        range_frame = tk.Frame(row_frame, bg=self.colors['surface'])
        range_frame.pack(side=tk.LEFT, padx=5)

        # From page input
        from_var = tk.StringVar(value=str(from_page))
        from_entry = tk.Entry(
            range_frame,
            textvariable=from_var,
            font=('Segoe UI', 11),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            width=5,
            relief='solid',
            borderwidth=1,
            highlightthickness=0,
            highlightbackground=self.colors['border'],
            highlightcolor=self.colors['primary']
        )
        from_entry.pack(side=tk.LEFT, padx=2)

        # Add callback to update pdf_files data when from_page changes
        def update_from_page(*args):
            try:
                value = int(from_var.get())
                if 0 <= index - 1 < len(self.pdf_files):
                    self.pdf_files[index - 1]['from_page'] = value
            except ValueError:
                pass  

        from_var.trace('w', update_from_page)

        # Separator
        to_label = tk.Label(
            range_frame,
            text="to",
            font=('Segoe UI', 11),
            fg=self.colors['text_secondary'],
            bg=self.colors['surface']
        )
        to_label.pack(side=tk.LEFT, padx=5)

        # To page input
        to_var = tk.StringVar(value=str(to_page))
        to_entry = tk.Entry(
            range_frame,
            textvariable=to_var,
            font=('Segoe UI', 11),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            width=5,
            relief='solid',
            borderwidth=1,
            highlightthickness=0,
            highlightbackground=self.colors['border'],
            highlightcolor=self.colors['primary']
        )
        to_entry.pack(side=tk.LEFT, padx=2)

        # Add callback to update pdf_files data when to_page changes
        def update_to_page(*args):
            try:
                value = int(to_var.get())
                if 0 <= index - 1 < len(self.pdf_files):
                    self.pdf_files[index - 1]['to_page'] = value
            except ValueError:
                pass  

        to_var.trace('w', update_to_page)





        # Operation column (delete button)
        operation_frame = tk.Frame(row_frame, bg=self.colors['surface'])
        operation_frame.pack(side=tk.LEFT, padx=5)

        # Delete button
        delete_btn = tk.Button(
            operation_frame,
            text="🗑",
            font=('Segoe UI', 12),
            bg=self.colors['surface'],
            fg=self.colors['text_secondary'],
            relief='flat',
            width=3,
            cursor='hand2',
            borderwidth=0,
            command=lambda: self.delete_row(index)
        )
        delete_btn.pack(side=tk.LEFT, padx=2)
        delete_btn.bind('<Enter>', lambda e: delete_btn.config(fg=self.colors['error']))
        delete_btn.bind('<Leave>', lambda e: delete_btn.config(fg=self.colors['text_secondary']))

    def add_files(self):
        # "Fájlok hozzáadása" button click.
        file_paths = filedialog.askopenfilenames(
            title="PDF fájlok",
            filetypes=[("PDF files", "*.pdf")]
        )

        if not file_paths:
            return

        # Process each selected file
        added_count = 0
        for file_path in file_paths:
                # page count
                pdf_reader = PdfReader(file_path)
                page_count = len(pdf_reader.pages)

                # Add to pdf_files list
                self.pdf_files.append({
                    'filepath': file_path,
                    'filename': Path(file_path).name,
                    'pages': page_count,
                    'from_page': 1,
                    'to_page': page_count,
                })
                added_count += 1

        self.refresh_table()


    def refresh_table(self):
        # Clear all existing rows (keeping header and separator)
        for widget in self.scrollable_frame.winfo_children()[2:]:
            widget.destroy()



        self.row_widgets = []

        # recraet rows from pdf_files data
        for i, pdf_data in enumerate(self.pdf_files, 1):
            self.create_table_row(
                i,
                pdf_data['filename'],
                pdf_data['pages'],
                pdf_data['from_page'],
                pdf_data['to_page'],
            )

    def clear_list(self):
        #"Lista törlése" button clicked
        if not self.pdf_files:
            messagebox.showinfo("Üres lista", "A lista még üres.")
            return

        result = messagebox.askyesno(
            "Lista törlése",
            "Biztosan szeretnéd törölni a teljes listát?"
        )
        if result:
            self.pdf_files.clear()
            self.refresh_table()

    def delete_row(self, index):
        # delete one row
        idx = index - 1

        if idx < 0 or idx >= len(self.pdf_files):
            return

        filename = self.pdf_files[idx]['filename']

        result = messagebox.askyesno(
            "Fájl törlése",
            f"Biztosan törölni szeretnéd '{filename}'?"
        )
        if result:
            self.pdf_files.pop(idx)
            self.refresh_table()

    def merge_pdfs(self):
        merge_pdfs(self.pdf_files)

    def split_pdf(self):
        split_from_table(self.pdf_files)
