import matplotlib

matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import numpy as np
import scipy.signal
import warnings

from collections import OrderedDict

warnings.simplefilter('ignore', np.RankWarning)  # Turns off warning for large polynomial degrees . . .

# The variables below are set for quick changes without the hassle of sifting through code . . .
POLY_DEG = 25

x_AXIS_TITLE = "Sample # (ROM Address)"
y_AXIS_TITLE = "Amplitude"

x_MIN, x_MAX = 0, 255
y_MIN, y_MAX = 0, 255

x_MINOR_TICKS, x_MAJOR_TICKS = 61, 4
y_MINOR_TICKS, y_MAJOR_TICKS = 29, 8

WAVEFORM_COUNT = 32

DRAW_WINDOW = 1.5  # Used to give user leeway when drawing on graph . . .

PAGES = 4
FIG_COUNT = 8


class DrawGraph(object):
    """Used in conjunction with tkinter to allow hand-drawn graphs to be generated

    Components:
        :param self.__Enter_cid: CID for entering axis
        :param self.__Exit_cid: CID for exiting axis
        :param self.__Motion_cid: CID for moving mouse
        :param self.ax: Holds the axis within self.fig
        :param self.canvas: The visual plot on top of self.ax
        :param self.current_waveform: Index to keep track of current waveform
        :param self.current_x: Temp variable for hand drawing (for x)
        :param self.current_y: Temp variable for hand drawing (for y)
        :param self.fig: Holds figure lines will be in
        :param self.line: Line plotted on axis
        :param self.line_set: List of 'LinePoints' objects
        :param self.x_max: Upper x bound
        :param self.x_min: Lower x bound
        :param self.y_max: Upper y bound
        :param self.y_mid_point: Mid point location on y axis
        :param self.y_min: Lower y bound
    """

    def __init__(self):
        """ Initializes all necessary variables """

        self.fig = plt.figure()     # Generates a figure for the plot to lie on . . .

        self.ax = create_graph(x_axis=x_AXIS_TITLE, y_axis=y_AXIS_TITLE,
                               x_min=x_MIN, x_max=x_MAX,
                               y_min=y_MIN, y_max=y_MAX,
                               x_major_ticks=x_MAJOR_TICKS, x_minor_ticks=x_MINOR_TICKS,
                               y_major_ticks=y_MAJOR_TICKS, y_minor_ticks=y_MINOR_TICKS,
                               fig=self.fig, subplot_section=[1, 1, 1])

        # The minimum/maximum values for x and y plot points are recorded . . .
        self.x_min = x_MIN
        self.x_max = x_MAX
        self.y_min = y_MIN
        self.y_max = y_MAX

        self.y_mid_point = (self.y_max + self.y_min) / 2

        # To better differentiate plot points, a list of lines are kept . . .
        self.line_set = [LinePoints() for i in range(WAVEFORM_COUNT)]

        self.line = self.ax.plot(0, 0)[0]  # Returns 1st (and only) line generated to graph . . .

        # Components not yet initialized in this class are listed below . . .

        self.canvas = None  # Canvas used for the user to draw graph on . . .
        self.current_waveform = None  # Index used for keeping track of working waveform . . .

        # Each event id is tracked for enabling/disabling proper events . . .
        self.__Motion_cid = None
        self.__Enter_cid = None
        self.__Exit_cid = None

        # Variable used to reduce component tracing . . .
        self.current_x = None
        self.current_y = None

    # END def __init__() #

    def change_amp(self, amp: float):
        """Changes the current waveform's amplitude

        Keyword arguments:
            :param amp: Amplitude factor used
        """

        # Multiplies given amplitude to the data . . .
        self.line_set[self.current_waveform].y *= amp

        # Changes if data is still in bounds (and takes action, if needed) . . .
        self.__check_plot_details()

    # END def change_amp() #

    def change_freq(self, freq: int):
        """Changes the current waveform's frequency

        Keyword arguments:
            :param freq: Frequency factor used
        """

        append_data = 0  # Used for appending any missing points . . .
        y_point = 0  # Keeps track of new y data point . . .
        y_array = np.array([])  # Keeps track of set of new y data points . . .

        # Performs an averaging of the data points for frequency change . . .
        for i in range(self.x_max - self.x_min + 1):
            y_point += self.line_set[self.current_waveform].y[i]

            if (i + 1) % freq == 0:  # Captures set of points and puts them in np.array . . .
                y_array = np.append(y_array, [y_point / freq])
                y_point = 0

        # Creates any multiple copies of line for frequency change . . .
        self.line_set[self.current_waveform].y = np.tile(y_array, [freq])

        # Fills in any missing data points (if needed) . . .
        while self.line_set[self.current_waveform].y.size < (self.x_max - self.x_min + 1):
            self.line_set[self.current_waveform].y = np.append(self.line_set[self.current_waveform].y,
                                                               self.line_set[self.current_waveform].y[append_data])
            append_data += 1

        # Changes if data is still in bounds (and takes action, if needed) . . .
        self.__check_plot_details()

    # END def change_freq() #

    def change_function(self, name: str, mix_func: bool, cycles: float, wav_num: int = None):
        """Changes the current waveform by either mixing or overwriting waveform with function

        Keyword arguments:
            :param name: Name of function being used
            :param mix_func: Boolean used to control whether user mixes function or not
            :param cycles: Provides number of cycles function will happen
            :param wav_num: Used to index another waveform user created
        """

        x_array = np.linspace(self.x_min,
                              self.x_max,
                              self.x_max - self.x_min + 1)
        y_array = np.array([])

        # Looks at what function user has selected . . .
        if name in {"Sine", "Cosine", "Square", "Sawtooth"}:
            # To fill the graph, a custom frequency is generated (using name and cycles as an input)
            freq = (cycles * 2 * np.pi) / (self.x_max - self.x_min)
            y_array = (self.y_max - self.y_mid_point) * FUNCTIONS[name](freq * x_array) + self.y_mid_point

        elif name == "Random":
            # To use random, cycles will be casted as an int . . .
            cycles = self.__round_int(cycles)
            if cycles < 1:
                cycles = 1

            y_array = (self.y_max - self.y_min) * np.random.random_sample((x_array.size // cycles,)) + self.y_min
            y_array = np.tile(y_array, [cycles])

            # Makes sure there's enough y data points . . .
            append_index = 0
            while y_array.size < (self.x_max - self.x_min + 1):
                y_array = np.append(y_array, y_array[append_index])

        else:  # name == "Waveform"

            # Checks to see if there is a waveform that can be copied . . .
            if not self.line_set[wav_num].drawn:
                return  # Does nothing if array is empty . . .

            # To use random, cycles will be casted as an int . . .
            cycles = self.__round_int(cycles)
            if cycles < 1:
                cycles = 1
            y_point = 0

            # Performs an averaging of the data points for frequency change . . .
            for i in range(self.x_max - self.x_min + 1):
                y_point += self.line_set[wav_num].y[i]

                if (i + 1) % cycles == 0:  # Captures set of points and puts them in np.array . . .
                    y_array = np.append(y_array, [y_point / cycles])
                    y_point = 0

            # Creates any multiple copies of line for frequency change . . .
            y_array = np.tile(y_array, [cycles])

            # Makes sure there's enough y data points . . .
            append_index = 0
            while y_array.size < (self.x_max - self.x_min + 1):
                y_array = np.append(y_array, y_array[append_index])

        # Checks whether the user selected to mix and if the line is drawn . . .
        if mix_func and self.line_set[self.current_waveform].drawn:
            self.line_set[self.current_waveform].y += y_array
        else:
            self.line_set[self.current_waveform].x = x_array
            self.line_set[self.current_waveform].y = y_array
            self.line_set[self.current_waveform].drawn = True

            if self.__Enter_cid is not None:
                self.canvas.mpl_disconnect(self.__Enter_cid)
                self.__Enter_cid = None

        self.__check_plot_details()
        self.plot_current_data()

    # END def change_function() #

    def change_level(self, level: int):
        """Changes the level of the current plot

        Keyword Arguments:
            :param level: amount graph needs to move
        """

        self.line_set[self.current_waveform].y += level  # Adds level value to graph . . .
        self.__check_plot_details()
        self.plot_current_data()

    # END def change_level() #

    def clear_graph(self):
        """Clears 'LinePoints' data"""

        # No need to clear if graph is already cleared . . .
        if not self.line_set[self.current_waveform].drawn:
            return

        self.line_set[self.current_waveform] = LinePoints()  # Resets current line . . .

        # Re-references current_x and current_y for drawing . . .
        self.current_x = self.line_set[self.current_waveform].x
        self.current_y = self.line_set[self.current_waveform].y

        self.plot_current_data()

        # Re-enable entering axis . . .
        self.__Enter_cid = self.canvas.mpl_connect('axes_enter_event', self.__enter_axes)

    # END def clear_graph() #

    def export_data(self) -> list:
        """Exports data from graph to a file provided

        returns: list of data from graph in binary form
        """

        data_to_return = []

        for line in self.line_set:
            if not line.drawn:
                data_to_return.append([self.y_min] * (self.x_max - self.x_min + 1))
            else:
                data_to_return.append(np.rint(line.y).astype(int))  # Ensures ints are being received . . .

        return data_to_return

    # END def export_data() #

    def print_to_pdf(self, file_name: str):
        """Exports graph data to pdfs

        Keyword arguments:
            :param file_name: Name of file being saved to
        """

        # Opens pdf for printing graphs to . . .
        pp = PdfPages(file_name)
        fig = plt.figure()

        # Creates 'fig_count' amount of axis' for printing on same page . . .
        ax = []
        for i in range(FIG_COUNT):

            # Creates graphs that look the same . . .
            ax.append(create_graph(x_axis='', y_axis='',
                                   x_min=x_MIN, x_max=x_MAX,
                                   y_min=y_MIN, y_max=y_MAX,
                                   x_major_ticks=x_MAJOR_TICKS, x_minor_ticks=x_MINOR_TICKS,
                                   y_major_ticks=y_MAJOR_TICKS, y_minor_ticks=y_MINOR_TICKS,
                                   fig=fig, subplot_section=[4, 2, i + 1]))
            ax[i].set_yticklabels([])
            ax[i].set_xticklabels([])

        # Prepares each axis for each page . . .
        for page in range(PAGES):

            # Plots data . . .
            for current_figure in range(FIG_COUNT):
                ax[current_figure].plot(self.line_set[page * FIG_COUNT + current_figure].x,
                                        self.line_set[page * FIG_COUNT + current_figure].y,
                                        color='b')

            # Saves current subplots to page . . .
            pp.savefig()

            # Removes last plotted data . . .
            for current_figure in range(FIG_COUNT):
                ax[current_figure].lines.pop(0)

        pp.close()

    # END def __print_to_pdf() #

    def plot_current_data(self):
        """Plots current data"""

        self.line.set_data(self.line_set[self.current_waveform].x, self.line_set[self.current_waveform].y)
        self.canvas.draw()

    # END def __plot_current_data() #

    def set_current_plot(self, current_waveform: int):
        """Plots current line and reflects changes through canvas

        Keyword arguments:
            :param current_waveform: Index of waveform desired to be used
        """

        self.current_waveform = current_waveform  # Current waveform number is updated . . .
        self.ax.set_title("Waveform %d" % current_waveform)  # Axis title is updated for current waveform . . .
        self.plot_current_data()

        # Will only allow the user to draw a line if LinePoints.drawn is True . . .
        if not self.line_set[self.current_waveform].drawn:

            # Variables current_x and current_y are only used for hand-drawing . . .
            self.current_x = self.line_set[self.current_waveform].x
            self.current_y = self.line_set[self.current_waveform].y

            # Reset most cid values . . .
            self.__Motion_cid = None
            self.__Exit_cid = None

            # If 'axes_enter_event' already enabled, no need to re-enable . . .
            if self.__Enter_cid is None:
                self.__Enter_cid = self.canvas.mpl_connect('axes_enter_event', self.__enter_axes)

    # END def set_current_line() #

    def __check_plot_details(self):
        """Checks to make sure plot is right size and is made up of integers"""

        # Only go into here when a y value overflows over the desired boundaries . . .
        if self.line_set[self.current_waveform].y.max() > self.y_max or \
           self.line_set[self.current_waveform].y.min() < self.y_min:
            self.__rescale_to_fit()

    # END def __check_plot_details() #

    def __curve_fit(self):
        """Creates a line of best fit for the current plotted data"""

        # Converts x and y points to numpy array . . .
        self.line_set[self.current_waveform].x = np.array(self.line_set[self.current_waveform].x)
        self.line_set[self.current_waveform].y = np.array(self.line_set[self.current_waveform].y)

        coefficients = np.polyfit(self.line_set[self.current_waveform].x,  # Creates coefficients for a polynomial of
                                  self.line_set[self.current_waveform].y,  # of degree POLY_DEG . . .
                                  POLY_DEG)

        # Creates a function using the coefficients . . .
        f = np.poly1d(coefficients)

        self.line_set[self.current_waveform].x = np.linspace(self.x_min,  # Creates an equally spaced set of x points
                                                 self.x_max,  # at every integer . . .
                                                 self.x_max - self.x_min + 1)
        self.line_set[self.current_waveform].y = f(self.line_set[self.current_waveform].x)

        self.__check_plot_details()
        self.plot_current_data()
        self.line_set[self.current_waveform].drawn = True  # A waveform is considered drawn at this point . . .

    # END def __curve_fit() #

    def __enter_axes(self, event):
        """Method called after axis has been entered

        Keyword arguments:
            :param event: Holds event data
        """

        # Makes sure user enters from left side of window . . .
        if event.xdata <= self.x_min + DRAW_WINDOW:
            self.current_x.append(event.xdata)
            self.current_y.append(event.ydata)

            if self.__Motion_cid is None:
                self.__Motion_cid = self.canvas.mpl_connect('motion_notify_event', self.__hand_draw_on_graph)

            if self.__Exit_cid is None:
                self.__Exit_cid = self.canvas.mpl_connect('axes_leave_event', self.__exit_axes)

    # END def __enter_axes() #

    def __exit_axes(self, event):
        """Method called after axis has been left

        Keyword arguments:
            :param event: Holds event data (unused)
        """

        # All events are disabled when user leaves axis . . .
        self.canvas.mpl_disconnect(self.__Motion_cid)
        self.canvas.mpl_disconnect(self.__Enter_cid)
        self.canvas.mpl_disconnect(self.__Exit_cid)

        # Points are processed once the cursor leaves the axis . . .
        self.__curve_fit()

        self.__Motion_cid = None
        self.__Enter_cid = None
        self.__Exit_cid = None

    # END def __exit_axes() #

    def __hand_draw_on_graph(self, event):
        """Allows the user to draw proper functions on graph

        Keyword arguments:
            :param event: Holds event data
        """

        # Prevents the user from plotting non-functions . . .
        # self.line_set[self.current_waveform].x[-1] returns the maximum x, in this case . . .

        if event.xdata > self.current_x[-1]:
            # A list append is much faster than a numpy append . . .
            self.current_x.append(event.xdata)
            self.current_y.append(event.ydata)
            self.line.set_data(self.current_x, self.current_y)
            self.canvas.draw()

    # END def __hand_draw_on_graph() #

    def __rescale_to_fit(self):
        """Corrects plot data that overflows over the y boundaries"""

        # Below, this algorithm is used to compress the graph . . .
        overflow = (np.absolute(self.line_set[self.current_waveform].y - self.y_mid_point)).max()

        self.line_set[self.current_waveform].y -= self.y_mid_point
        self.line_set[self.current_waveform].y *= (self.y_max - self.y_mid_point) / overflow
        self.line_set[self.current_waveform].y += self.y_mid_point

    # END def __rescale_to_fit() #

    @staticmethod
    def __round_int(num: float) -> int:
        """Rounds numbers to nearest integer

        Keyword arguments:
            :param num: Number to be rounded

        :returns: Rounded integer
        """

        return int(num + .5)

        # END def __round_int() #


class LinePoints(object):
    """
    Holds coordinates for x and y plots (along with if they were drawn or not)

    Components:
        :param self.x: Holds all x plot data (first as a list, for speed reasons, then converted to numpy array)
        :param self.y: Holds all y plot data (first as a list, for speed reasons, then converted to numpy array)
        :param self.drawn: Indicates whether or not graph has been drawn
    """

    def __init__(self):
        """Initializes all necessary variables"""

        self.x = []
        self.y = []
        self.drawn = False

        # END def __init__() #


def create_graph(x_axis: str, y_axis: str,
                 x_min: int, x_max: int,
                 y_min: int, y_max: int,
                 x_major_ticks: int, x_minor_ticks: int,
                 y_major_ticks: int, y_minor_ticks: int,
                 fig, subplot_section) -> object:
    """
    Creates a graph

    Keyword arguments:
        :param x_axis: x axis title
        :param y_axis: y axis title
        :param x_min: lower x bound
        :param x_max: upper x bound
        :param y_min: lower y bound
        :param y_max: upper y bound
        :param x_major_ticks: major x ticks count
        :param x_minor_ticks: minor x ticks count
        :param y_major_ticks: major y ticks count
        :param y_minor_ticks: minor y ticks count
        :param fig: figure to be plotted on
        :param subplot_section: section of figure for plot

    :returns: axis to that figure
    """

    ax = fig.add_subplot(*subplot_section)  # Places the figure in a specific spot . . .

    # The x and y axis titles are set here . . .
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)

    # Prevents the graph axes from changing . . .
    ax.set_autoscale_on(False)

    # Sets background ticks in the graph, for better visual appearance . . .
    x_minor_ticks = np.linspace(0, 255, x_minor_ticks)
    x_major_ticks = np.linspace(0, 255, x_major_ticks)
    y_minor_ticks = np.linspace(0, 255, y_minor_ticks)
    y_major_ticks = np.linspace(0, 255, y_major_ticks)

    ax.set_xticks(x_major_ticks)
    ax.set_xticks(x_minor_ticks, minor=True)
    ax.set_yticks(y_major_ticks)
    ax.set_yticks(y_minor_ticks, minor=True)

    plt.grid(which='both')
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)

    # Sets the graphs boundaries . . .
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    return ax


# END def create_graph() #


# Dictionary used to hold all functions used . . .
FUNCTIONS = OrderedDict([("Sine", np.sin),
                         ("Cosine", np.cos),
                         ("Square", scipy.signal.square),
                         ("Sawtooth", scipy.signal.sawtooth),
                         ("Random", None),
                         ("Waveform", None)])
