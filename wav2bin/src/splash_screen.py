import tkinter as tk
from tkinter import ttk

from wav2bin.src.helper_functions import resource_path

# The variables below are set for quick changes without the hassle of sifting through code . . .
INTERFACE_TITLE = "WAV2BIN (Version 1.3)"
ICON_NAME = 'App_Icon.ico'
IMAGE_NAME = 'App_Icon.gif'


class SplashScreen(tk.Frame):
    """Used to create a splash screen with an image and text

    Components:
        :param self.graphic: Label which holds an image for window
        :param self.name_label: Label which holds text (for name)
        :param self.root: Holds graphics root figure
    """

    def __init__(self, root):
        """Initializes all necessary variables

        Keyword arguments:
            :param root: Tkinter root that will be referenced in this object
        """

        self.root = root

        # Changes icon . . .
        icon = resource_path('imgs/' + ICON_NAME)
        root.iconbitmap(icon)

        # Creates a graphic frame for features to be added . . .
        tk.Frame.__init__(self, root)
        self.root.wm_title(INTERFACE_TITLE)
        self.root['bg'] = 'white'

        self.root.protocol("WM_DELETE_WINDOW", self.__quit_program)  # Makes the window close button quit program . . .

        self.root.resizable(False, False)   # Prevents window from being resized . . .

        # Quit after 4 seconds . . .
        self.root.after(4000, self.__quit_program)

    # END def __init__() #

    def add_features(self):
        """Inserts every feature into the root's figure"""

        # Goes through and includes all features . . .
        self.__feature_image()
        self.__feature_text()

    # END def add_features() #

    def __feature_image(self):
        """Adds an image in window"""

        # Setup image for graphic . . .
        image_path = resource_path('imgs/' + IMAGE_NAME)
        image = tk.PhotoImage(file=image_path)
        sub_image = image.subsample(5, 5)

        self.graphic = ttk.Label(image=sub_image, background='white')
        self.graphic.image = sub_image
        self.graphic.grid(row=0, column=0)

    def __feature_text(self):
        """Adds text in window"""

        self.name_label = ttk.Label(text="By: Joshua Van Deren", background='white')
        self.name_label.config(font=('Arial', 15))
        self.name_label.grid(row=1, column=0)

    # END def __feature_image() #

    def __remove_grid_features(self):
        """Removes current items inside tkinter grid"""

        self.graphic.grid_forget()
        self.name_label.grid_forget()

    # END def __feature_image() #

    def __quit_program(self):
        """Closes current running program"""

        self.__remove_grid_features()
        self.quit()

    # END def __quit_program() #

