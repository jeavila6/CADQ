import math
import tkinter as tk
import tkinter.filedialog
import tkinter.font

from audio_player import AudioPlayer
from manage_port import open_port
from serial_reader import SerialReader
from serial_writer import SerialWriter

# settings
MIN_RATING = 0
MAX_RATING = 20
CANVAS_PAD_X = 5
CANVAS_PAD_Y = 5
DIAL_RADIUS = 30
DIAL_MAX_DEGREES = 270

# color pallet
COLOR_RED = '#ef9a9a'
COLOR_GREEN = '#a5d6a7'
COLOR_BLUE = '#bbdefb'
COLOR_GRAY = '#616161'
COLOR_WHITE = '#ffffff'


def rating_to_degrees(rating):
    """Return degrees by mapping rating from MIN_RATING-MAX_RATING range to 0-DIAL_MAX_DEGREES range."""
    degrees = float(rating - MIN_RATING) / float(MAX_RATING - MIN_RATING) * DIAL_MAX_DEGREES

    # adjust for symmetry (angles of 0 and DIAL_MAX_DEGREES will be on opposite ends of dial)
    if DIAL_MAX_DEGREES < 180:
        degrees += (180 - DIAL_MAX_DEGREES) / 2
    elif DIAL_MAX_DEGREES > 180:
        degrees -= (360 - DIAL_MAX_DEGREES) / 2

    return degrees


class Application(tk.Frame):

    def __init__(self, device_name, master=None):
        tk.Frame.__init__(self, master)

        port = open_port(device_name)
        self.reader = SerialReader(port)
        self.reader.start()

        self.player = AudioPlayer()
        self.writer = None

        self.prev_rating = -1
        self.filename = None

        custom_font = tk.font.Font(family='Consolas', size=12, weight=tk.font.BOLD)

        # window properties
        self.master.title('Dial Reader')
        self.master.minsize(250, 180)
        self.winfo_toplevel().columnconfigure(0, weight=1)

        # button for loading file
        self.load_button = tk.Button(command=self.load_file, text='Load', bg=COLOR_BLUE, relief=tk.GROOVE,
                                     font=custom_font)
        self.load_button.grid(row=0, column=0, padx=3, sticky=tk.W+tk.E)

        # label for filename
        self.filename_label_text = tk.StringVar()
        self.filename_label_text.set('Load an audio file to start.')
        self.filename_label = tk.Label(textvariable=self.filename_label_text, font=custom_font)
        self.filename_label.grid(row=1, column=0)

        # button for starting/stopping playback (initially a disabled start button)
        self.start_stop_button = tk.Button(command=self.start_recording, text='Start', bg=COLOR_GREEN, relief=tk.GROOVE,
                                           state=tk.DISABLED, font=custom_font)
        self.start_stop_button.grid(row=2, column=0, padx=3, sticky=tk.W + tk.E)

        # canvas for drawing dial
        self.dial_canvas = tk.Canvas(height=(DIAL_RADIUS + CANVAS_PAD_X) * 2, width=(DIAL_RADIUS + CANVAS_PAD_Y) * 2)
        self.dial_canvas.grid(row=3, column=0)

        # label for rating
        self.rating_label_text = tk.StringVar()
        self.rating_label = tk.Label(textvariable=self.rating_label_text, font=custom_font)
        self.rating_label.grid(row=4, column=0)

        self.init_draw_dial()
        self.update_display()

    def load_file(self):
        """Display file dialog for selecting audio file."""

        # display file dialog, return if no selection was made
        self.filename = tk.filedialog.askopenfilename(parent=self, filetypes=[('AU files', '.au')])
        if not self.filename:
            return

        # update filename label, shorten filename if needed
        max_length = 20
        display_filename = ('...' + self.filename[-max_length:]) if len(self.filename) > max_length else self.filename
        self.filename_label_text.set(display_filename)

        # enable start/stop button
        self.start_stop_button.config(state=tk.NORMAL)

    def update_display(self):
        """Update dial display to match current rating."""

        # update rating label and dial drawing, ignore if rating has not changed
        curr_rating = self.reader.stream[0]
        if curr_rating != self.prev_rating:
            self.prev_rating = curr_rating
            self.rating_label_text.set('Rating: ' + '{:3s}'.format(curr_rating))
            self.update_draw_dial()

        # reschedule task
        self.master.after(1, self.update_display)

    def init_draw_dial(self):
        """Draws an empty dial on canvas."""

        # draw dial ticks, extend ticks for minimum and maximum rating
        tick_x0 = DIAL_RADIUS
        tick_y0 = DIAL_RADIUS
        for rating in range(MIN_RATING, MAX_RATING + 1):
            angle = rating_to_degrees(rating)
            tick_length = 10 if rating in [MIN_RATING, MAX_RATING] else 5
            tick_x1 = -(DIAL_RADIUS + tick_length) * math.cos(angle * math.pi / 180) + DIAL_RADIUS
            tick_y1 = -(DIAL_RADIUS + tick_length) * math.sin(angle * math.pi / 180) + DIAL_RADIUS
            self.dial_canvas.create_line(tick_x0, tick_y0, tick_x1, tick_y1, fill=COLOR_GRAY, width=2)

        # draw dial
        dial_diameter = DIAL_RADIUS * 2
        oval_x0 = 0
        oval_y0 = 0
        oval_x1 = oval_x0 + dial_diameter
        oval_y1 = oval_y0 + dial_diameter
        self.dial_canvas.create_oval(oval_x0, oval_y0, oval_x1, oval_y1, fill=COLOR_WHITE, width=3)

        # move all canvas objects for padding
        canvas_objects = self.dial_canvas.find_all()
        for canvas_object in canvas_objects:
            self.dial_canvas.move(canvas_object, CANVAS_PAD_X, CANVAS_PAD_Y)

    def update_draw_dial(self):
        """Draw dial marker to match current rating."""
        dial_marker_tag = 'dial_marker_tag'
        angle = rating_to_degrees(int(self.prev_rating))

        # delete old dial marker using tag
        self.dial_canvas.delete(dial_marker_tag)

        # draw new dial marker
        inner_radius = DIAL_RADIUS - 15
        line_x0 = -inner_radius * math.cos(angle * math.pi / 180) + DIAL_RADIUS
        line_y0 = -inner_radius * math.sin(angle * math.pi / 180) + DIAL_RADIUS
        line_x1 = -DIAL_RADIUS * math.cos(angle * math.pi / 180) + DIAL_RADIUS
        line_y1 = -DIAL_RADIUS * math.sin(angle * math.pi / 180) + DIAL_RADIUS
        line = self.dial_canvas.create_line(line_x0, line_y0, line_x1, line_y1, width=3)

        # tag new marker
        self.dial_canvas.addtag_withtag(dial_marker_tag, line)

        # move canvas object for padding
        self.dial_canvas.move(line, CANVAS_PAD_X, CANVAS_PAD_Y)

    def check_if_playing(self):
        """Stop recording as soon as audio has stopped playing."""
        if not self.player.is_playing():
            self.stop_recording()
        else:

            # reschedule task
            self.master.after(1, self.check_if_playing)

    def start_recording(self):
        """Start audio playback and recording of ratings."""
        self.player.play(self.filename)

        self.writer = SerialWriter(self.reader.stream)
        self.writer.start()

        # update start/stop button to be stop button
        self.start_stop_button.config(command=self.stop_recording, text='Stop', bg=COLOR_RED)

        self.check_if_playing()

    def stop_recording(self):
        """Stop audio playback and recording of ratings."""

        if self.player.is_playing():
            self.player.stop()
            return

        text = self.writer.stop()

        # update start/stop button to be start button
        self.start_stop_button.config(command=self.start_recording, text='Start', bg=COLOR_GREEN)

        # open save dialog, return if no selection was made
        filepath = tk.filedialog.asksaveasfile(parent=self, mode='w', defaultextension='.txt')
        if filepath is None:
            return

        # save recording to file
        filepath.write(text)
        filepath.close()
