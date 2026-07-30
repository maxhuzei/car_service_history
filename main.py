import tkinter as tk
from src.ui.main_app import MainApplication


def main() -> None:
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()

