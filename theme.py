from tkinter import ttk


def setup_theme(root):
    colors = {
        'bg': '#464646',           
        'surface': '#3C3C3C',
        'primary': "#1860B8",
        'primary_hover': "#74B3FA",
        'text': '#EEEEEE',
        'text_secondary': '#AAAAAA',
        'border': '#2D2D2D',
    }

    root.configure(bg=colors['bg'])

    style = ttk.Style()
    style.theme_use('equilux')

    # Configure  table
    style.configure(
        "PDFTable.Treeview",
        background=colors['surface'],
        foreground=colors['text'],
        fieldbackground=colors['surface'],
        borderwidth=0,
        font=('Segoe UI', 9),
        rowheight=70
    )

    style.configure(
        "PDFTable.Treeview.Heading",
        background=colors['bg'],
        foreground=colors['text'],
        borderwidth=0,
        font=('Segoe UI', 9, 'bold'),
        relief='flat'
    )
    '''
     style.map(
        "PDFTable.Treeview",
        background=[('selected', colors['primary'])],
        foreground=[('selected', '#FFFFFF')]
    )
    style.map(
        "PDFTable.Treeview.Heading",
        background=[('active', colors['primary'])]
    )
    '''

    # Configure Frame style
    style.configure(
        "Main.TFrame",
        background=colors['bg']
    )
    style.configure(
        "Surface.TFrame",
        background=colors['surface']
    )

    '''
    # Configure Entry style
    style.configure(
        "Range.TEntry",
        fieldbackground=colors['surface'],
        borderwidth=2,
        relief='solid'
    )
    '''

    return colors
