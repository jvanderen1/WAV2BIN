import tkinter as tk
import tkinter.filedialog as fd
from tkinter import messagebox as mb
from tkinter import ttk

from wav2bin.src.draw_graph import DrawGraph, FUNCTIONS
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from wav2bin.src.helper_functions import resource_path

from time import sleep

# The variables below are set for quick changes without the hassle of sifting through code . . .
INTERFACE_TITLE = "WAV2BIN (Version 1.3)"
ICON_NAME = 'App_Icon.ico'

STARTING_WAVEFORM = 0

ROWS, COLS = 8, 6

LINES_IN_DISPLAY = 4


class GraphicInterface(tk.Frame):
    """Used to create a graphic user interface for graphing, decoding, and exporting data

    Components:
        :param self.amplitude_entry_var: Holds entry for amplitude
        :param self.current_function_var: Holds entry for current function value
        :param self.current_waveform_func: Holds options for current waveform
        :param self.current_waveform_func_var: Holds option for waveform func
        :param self.current_waveform_var: Holds option for current waveform
        :param self.cycles_entry_var: Holds entry for entering cycles
        :param self.frequency_entry_var: Holds entry for entering frequency
        :param self.level_entry_var: Holds entry for entering level change
        :param self.graph_tool: Holds 'DrawGraph' object
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

        self.root.resizable(True, True)     # Allows window to be resized . . .

        # Setting weights for each row . . .
        for i in range(ROWS):
            self.root.rowconfigure(i, weight=1)
        for i in range(COLS):
            self.root.columnconfigure(i, weight=1)

        # Setting ttk styling . . .
        style = ttk.Style()
        style.configure('W.TButton', background='white')
        style.configure('W.TLabelframe', background='white', )

        # Variables used to keep track of options/entries in the GUI . . .
        self.current_waveform_var = tk.StringVar()      # Used for keeping track of visible waveform . . .
        self.current_function_var = tk.StringVar()      # Used for keeping track of function . . .
        self.current_waveform_func_var = tk.IntVar()    # Used for keeping track of selected waveform . . .
        self.amplitude_entry_var = tk.StringVar()       # Used for keeping track of amplitude entry . . .
        self.cycles_entry_var = tk.StringVar()          # Used for keeping track of cycles entry . . .
        self.frequency_entry_var = tk.StringVar()       # Used for keeping track of frequency entry . . .
        self.level_entry_var = tk.StringVar()           # Used for keeping track of level entry . . .

        # Components not yet initialized in this class are listed below . . .
        self.graph_tool = None

    # END def __init__() #

    def add_features(self):
        """Inserts every feature into the root's figure"""

        # Goes through and includes all features . . .
        self.__feature_graph_tool()
        self.__feature_waveform_menu()
        self.__feature_user_graph_change()
        self.__feature_clear()
        self.__feature_modify_function()
        self.__feature_export()

    # END def add_features() #

    def __amplitude_change(self, event):
        """Changes amplitude based on amplitude entry

        Keyword arguments:
            :param event: Holds event data (unused)
        """

        # If there's no graph, don't continue . . .
        if self.graph_tool.line_set[self.graph_tool.current_waveform].drawn and \
                        self.amplitude_entry_var.get() not in {'-', '', '.', '-.'}:
            amp = float(self.amplitude_entry_var.get())

            # Changes the graph's amplitude . . .
            self.graph_tool.change_amp(amp=amp)

            # Plots current graph . . .
            self.graph_tool.plot_current_data()

        # Clears the text entry data . . .
        self.amplitude_entry_var.set("")

    # END def __amplitude_change() #

    def __change_waveform(self, event):
        """Changes the current line figure within the graph feature

        Keyword arguments:
            :param event: Holds event data
        """

        # Takes the 2nd argument in "Waveform %d" string minus 1 to find the current waveform . . .
        # (i.e. "Waveform 0" -> index = 0)
        self.graph_tool.set_current_plot(int(event.split()[1]))

    # END def change_waveform() #

    def __clear_graph(self):
        """Clears the current graph"""

        self.graph_tool.clear_graph()

    # END def clear_graph() #

    def __export(self):
        """Exports data into a .bin file"""

        # Ask user if they would like to print graphs to pdf . . .
        response = mb.askyesno(title="Save Waveforms", message="Would you like to save your waveforms as a PDF?", icon=mb.QUESTION)

        try:
            with fd.asksaveasfile(mode='wb', initialfile='.bin', defaultextension=".bin", filetypes=[('Generic Binary File (*.bin)', '*.bin')]) as file:

                # Print out graphs to pdf if result == True . . .
                if response:
                    file_path = '.'.join(file.name.split('.')[:-1])
                    self.graph_tool.print_to_pdf(''.join([file_path, '.pdf']))

                dialog = PopupDialog(self.root)
                dialog.list_data(self.graph_tool.export_data(), file)
        except Exception:
            return

    # END def __export() #

    def __feature_clear(self):
        """Adds a button for clearing the graph"""

        clear_button = ttk.Button(master=self.root, text="Clear", command=self.__clear_graph, style='W.TButton')
        clear_button.config(width=50)
        clear_button.grid(row=3, column=4, columnspan=2, padx=25)

    # END def feature_clear() #

    def __feature_export(self):
        """Adds a button for exporting the graph data"""

        export_button = ttk.Button(self.root, text="Export", command=self.__export, style='W.TButton')
        export_button.config(width=150)
        export_button.grid(row=7, column=0, columnspan=6, padx=25, pady=10)

    # END def __feature_export #

    def __feature_waveform_menu(self):
        """Adds an options menu for changing current waveform"""

        # List of options generated . . .
        current_waveform_label = ttk.Label(self.root, text="Current Waveform", background='white')
        current_waveform_label.grid(row=4, column=0, sticky='e', padx=10)
        options = ["Waveform %d" % i for i in range(len(self.graph_tool.line_set))]

        current_waveform = ttk.OptionMenu(self.root, self.current_waveform_var, options[0], *options,
                                          command=self.__change_waveform)
        current_waveform.config(width=15)
        current_waveform.grid(row=4, column=1, columnspan=2, sticky='w', padx=20, pady=15)

    # END def feature_option_menu() #

    def __feature_graph_tool(self):
        """Adds the graph tool ('DrawGraph')"""

        self.graph_tool = DrawGraph()

        self.graph_tool.canvas = FigureCanvasTkAgg(self.graph_tool.fig, master=self.root)
        self.graph_tool.canvas.get_tk_widget().grid(row=0, column=0, rowspan=4, columnspan=4, sticky='nesw')

        self.graph_tool.set_current_plot(STARTING_WAVEFORM)

    # END def feature_graph_tool() #

    def __feature_modify_function(self):
        """Adds an options menu for functions to mix/overwrite, the mix/overwrite buttons, and labels"""

        # Adding a label frame around options . . .
        frame = ttk.LabelFrame(self.root, text="   Utilize Other Graphs   ", style='W.TLabelframe')
        frame.grid(row=5, column=0, rowspan=2, columnspan=6, sticky='nesw')

        # Function Options
        functions_label = ttk.Label(self.root, text="Functions", background='white')
        functions_label.grid(row=5, column=0, sticky='se', padx=10, pady=20)

        options = [key for key in FUNCTIONS]

        current_function = ttk.OptionMenu(self.root, self.current_function_var, options[0], *options,
                                          command=self.__function_changed)
        current_function.config(width=15)
        current_function.grid(row=5, column=1, columnspan=2, sticky='sw', padx=20, pady=20)

        # Select Waveform
        options = [i for i in range(len(self.graph_tool.line_set))]

        self.current_waveform_func = ttk.OptionMenu(self.root, self.current_waveform_func_var, options[0], *options)
        self.current_waveform_func.config(width=3)
        self.current_waveform_func.grid(row=5, column=3, sticky='sw', pady=20)
        self.current_waveform_func.grid_remove()  # Hides select Waveform options in the beginning . . .

        # Cycles
        vcmd = (self.register(self.__validate_positive_float), '%P')  # %P checks entry currently in entry box . . .
        cycles_label = ttk.Label(self.root, text="Cycles", background='white')
        cycles_label.grid(row=6, column=0, sticky='ne', padx=10, pady=20)
        cycles_entry = ttk.Entry(self.root, textvariable=self.cycles_entry_var, validate="key", validatecommand=vcmd)
        cycles_entry.config(width=18)
        cycles_entry.grid(row=6, column=1, columnspan=2, sticky='nw', padx=20, pady=20)

        # Mix Functions
        mix_func_button = ttk.Button(self.root, text="Mix Function", command=self.__mix_function, style='W.TButton')
        mix_func_button.config(width=20)
        mix_func_button.grid(row=5, column=4, columnspan=2, sticky='swe', padx=25, pady=20)

        # Overwrite Functions
        overwrite_func_button = ttk.Button(master=self.root, text="Overwrite Function",
                                           command=self.__overwrite_function)
        overwrite_func_button.config(width=20)
        overwrite_func_button.grid(row=6, column=4, columnspan=2, sticky='nwe', padx=25, pady=20)

    # END def __feature_modify_function() #

    def __feature_user_graph_change(self):
        """Adds entry to change current graph properties"""

        # Adding a label frame around options . . .
        frame = ttk.LabelFrame(self.root, text="   Basic Graph Properties   ", style='W.TLabelframe')
        frame.grid(row=0, column=4, rowspan=3, columnspan=2, sticky='nesw', pady=20, ipadx=5, ipady=5)

        # Frequency
        vcmd = (self.register(self.__validate_positive_int), '%S')  # %S checks entry currently being typed . . .
        frequency_label = ttk.Label(self.root, text="Frequency", background='white')
        frequency_label.grid(row=0, column=4, sticky='e')
        frequency_entry = ttk.Entry(self.root, textvariable=self.frequency_entry_var, validate="key", validatecommand=vcmd)
        frequency_entry.bind("<Return>", self.__frequency_change)
        frequency_entry.config(width=15)
        frequency_entry.grid(row=0, column=5, sticky='w', padx=20)

        # Amplitude
        vcmd = (self.register(self.__validate_float), '%P')         # %P checks entry currently in entry box . . .
        amplitude_label = ttk.Label(self.root, text="Amplitude", background='white')
        amplitude_label.grid(row=1, column=4, sticky='e')
        amplitude_entry = ttk.Entry(self.root, textvariable=self.amplitude_entry_var, validate="key", validatecommand=vcmd)
        amplitude_entry.bind("<Return>", self.__amplitude_change)
        amplitude_entry.config(width=15)
        amplitude_entry.grid(row=1, column=5, sticky='w', padx=20)

        # Level
        vcmd = (self.register(self.__validate_level), '%P')  # %S checks entry currently being typed . . .
        level_label = ttk.Label(self.root, text="Level", background='white')
        level_label.grid(row=2, column=4, sticky='e')
        level_entry = ttk.Entry(self.root, textvariable=self.level_entry_var, validate="key", validatecommand=vcmd)
        level_entry.bind("<Return>", self.__change_level)
        level_entry.config(width=15)
        level_entry.grid(row=2, column=5, sticky='w', padx=20)

    # END __feature_user_graph_change() #

    def __change_level(self, event):
        """Changes the level of the graph by a specific value

        Keyword arguments:
            :param event: Holds event data (unused)
        """
        if self.graph_tool.line_set[self.graph_tool.current_waveform].drawn:
            self.graph_tool.change_level(float(self.level_entry_var.get()))

        # Clears the text entry data . . .
        self.level_entry_var.set("")

    # END def __change_level() #

    def __frequency_change(self, event):
        """Used to change current waveforms frequency

        Keyword arguments:
            :param event: Holds event data (unused)
        """

        # If there's no graph (more specifically, function), don't draw . . .
        if self.graph_tool.line_set[self.graph_tool.current_waveform].drawn and \
                        self.frequency_entry_var.get() != '':

            freq = int(self.frequency_entry_var.get())

            # Frequency can't be smaller than 1 . . .
            if freq < 1:
                freq = 1

            # Frequency can't be larger than domain size . . .
            elif freq > self.graph_tool.x_max - self.graph_tool.x_min + 1:
                freq = self.graph_tool.x_max - self.graph_tool.x_min + 1

            # Changes the graph's frequency . . .
            self.graph_tool.change_freq(freq=freq)

            # Plots current graph . . .
            self.graph_tool.plot_current_data()

        # Clears the text entry data . . .
        self.frequency_entry_var.set("")

    # END def __frequency_change() #

    def __function_changed(self, event):
        """Called when a function selection has been made

        Keyword arguments:
            :param event: Holds event data (unused)
        """

        # Checks if function selected changed to "Waveform" . . .
        if self.current_function_var.get() == "Waveform":
            self.current_waveform_func.grid()

        # Will remove number option if not in function "Waveform" . . .
        elif self.current_waveform_func.winfo_manager() == "grid":
            self.current_waveform_func.grid_remove()

    # END __function_change() #

    def __mix_function(self):
        """Mixes current waveform with current function selected"""

        # Checks if user entered a valid cycle number . . .
        if self.cycles_entry_var.get() not in {'', '.'}:

            if self.current_waveform_func.winfo_manager() == "grid":
                self.graph_tool.change_function(name=self.current_function_var.get(),
                                                mix_func=True,
                                                cycles=float(self.cycles_entry_var.get()),
                                                wav_num=self.current_waveform_func_var.get())
            else:
                self.graph_tool.change_function(name=self.current_function_var.get(),
                                                mix_func=True,
                                                cycles=float(self.cycles_entry_var.get()))

        # Clears the text entry data . . .
        self.cycles_entry_var.set("")

    # END def __mix_function() #

    def __overwrite_function(self):
        """Overwrites current waveform with current function selected"""

        # Checks if user entered a valid cycle number . . .
        if self.cycles_entry_var.get() not in {'', '.'}:

            if self.current_waveform_func.winfo_manager() == "grid":
                self.graph_tool.change_function(name=self.current_function_var.get(),
                                                mix_func=False,
                                                cycles=float(self.cycles_entry_var.get()),
                                                wav_num=self.current_waveform_func_var.get())
            else:
                self.graph_tool.change_function(name=self.current_function_var.get(),
                                                mix_func=False,
                                                cycles=float(self.cycles_entry_var.get()))

        # Clears the text entry data . . .
        self.cycles_entry_var.set("")

    # END def __overwrite_function() #

    def __quit_program(self):
        """Closes current running program"""

        self.quit()  # Stops mainloop and prevents "Fatal Python Error: PyEval_RestoreThread: NULL tstate"
        self.destroy()  # on Windows . . .

    # END def __quit_program() #

    def __validate_float(self, value: str) -> bool:
        """Validates if user entry is a valid float

        Keyword Arguments:
            :param value: String holding potential candidate for float

        :returns: Pass or fail
        """

        # Checks if the string is empty, starting negative, or a valid float . . .
        if value in {'-', '', '.', '-.'}:
            return True
        else:
            try:
                float(value)
                return True
            except ValueError:
                self.bell()
                return False

    # END def __validate_float() #

    def __validate_level(self, value: str) -> bool:
        """Validates if user entry is between -256 and 255

        Keyword Arguments:
            :param value: String holding potential candidate for value

        :returns: Pass or fail
        """

        # Checks if the string is empty, starting negative, or a valid float . . .
        if value in {'-', '', '.', '-.'}:
            return True
        else:
            try:
                value = float(value)
                if value > 255.0 or value < -256.0:
                    self.bell()
                    return False
                else:
                    return True
            except ValueError:
                self.bell()
                return False

    # END def __validate_level() #

    def __validate_positive_int(self, value: str):
        """Validates if user entry is a valid positive int

        Keyword Argument:
            :param value: String holding potential candidate for positive int

        :returns: Pass or fail
        """

        # Checks if the character entered is an number . . .
        try:
            int(value)
            return True
        except ValueError:
            self.bell()
            return False

    # END def __validate_positive_int() #

    def __validate_positive_float(self, value: str):
        """Validates if user entry is a valid positive float

        Keyword Argument:
            :param value: String holding potential candidate for positive float

        :returns: Pass or fail
        """

        # Checks if the string is empty, starting negative, or a valid float . . .
        if value in {'', '.'}:
            return True
        else:
            try:
                float(value)
                return True
            except ValueError:
                self.bell()
                return False

                # END def __validate_positive_float() #


class PopupDialog(object):
    """Dialog used during execution of a tkinter window

    Components:
        :param: self.top: Figure used on top of a root figure
    """

    def __init__(self, parent):
        """Initializes all necessary variables

        Keyword arguments:
            :param parent: Tkinter root that will be referenced in this object
        """

        self.top = tk.Toplevel(parent)
        self.top.protocol("WM_DELETE_WINDOW", self._on_close)   # Redirects the windows close button to function . . .
        self.top.resizable(False, False)                        # Prevents window from being re-sized . . .

        self.key_pressed = False                                # Variable used to keep track of key press . . .

        icon = resource_path('imgs/' + ICON_NAME)
        self.top.iconbitmap(icon)

    # END def __init__() #

    def list_data(self, data_points: list, f):
        """Exports the given data to a file and displays the waveform values in hex

        Keyword arguments:
            :param data_points: List of points given to encode and display
            :param f: File being written to
        """

        listbox = tk.Listbox(self.top, width=165, height=50, font=(None, 10))
        listbox.bind("<Key>", self.__key)       # Binds key events to function . . .
        listbox.pack()

        for index in range(len(data_points)):

            # Waits until user presses another key to unlock . . .
            while self.key_pressed:
                listbox.update()

            # Write data to file . . .
            f.write(bytearray(data_points[index]))

            display = ['{0:02x}'.format(data) for data in data_points[index]]
            listbox.insert(tk.END, "Waveform %d:" % index)

            for i in range(LINES_IN_DISPLAY):
                listbox.insert(tk.END, ' '.join(display[i * len(display) // LINES_IN_DISPLAY:
                                                       (i+1) * len(display) // LINES_IN_DISPLAY]))
                listbox.yview(tk.END)
                self.top.update()
                sleep(0.1)

        self.top.destroy()

    # END def list_data() #

    def __key(self, event):
        """Function used to detect key press

        Keyword Arguments:
            :param event: Holds event data (unused)
        """

        self.key_pressed = not self.key_pressed

    # END def __key() #

    @staticmethod
    def _on_close():
        """Prevents user from closing dialog window"""
        return

    # END def _on_close() #
