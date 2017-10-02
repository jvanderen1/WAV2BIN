import tkinter as tk
from src.GraphicInterface import GraphicInterface


def main():
    """Generates UI for the user"""

    root = tk.Tk()
    UI = GraphicInterface(root)     # Creates graphics object . . .
    UI.add_features()               # Adds graph, buttons, options, etc . . .
    UI.mainloop()                   # Starts UI . . .


# Program begins execution here . . .
if __name__ == '__main__':
    main()
