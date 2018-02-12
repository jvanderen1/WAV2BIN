import tkinter as tk
from GraphicInterface import GraphicInterface
from SplashScreen import SplashScreen


def main():
    """Generates UI for the user"""

    root = tk.Tk()

    # Shows splash for a short time . . .
    UI = SplashScreen(root)
    UI.add_features()
    UI.mainloop()

    # After splash, goes to program . . .
    UI = GraphicInterface(root)     # Creates graphics object . . .
    UI.add_features()               # Adds graph, buttons, options, etc . . .
    UI.mainloop()                   # Starts UI . . .


# Program begins execution here . . .
if __name__ == '__main__':
    main()
