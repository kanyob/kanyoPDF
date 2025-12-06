from ttkthemes import ThemedTk
from app_ui import pdfApp


def main():
    #Entry point
    
    root = ThemedTk(theme="equilux")
    app = pdfApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
