import datetime
import logging
import os
import pickle
import random
import time

import pyautogui as pya
import pymsgbox
import pyperclip
from adict import adict

MAX_NUM_OPENABLES_AT_MAIN_SCREEN = 3
LOAD_GAME_WAITTIME_S = 10.

# set to None to start immediately, otherwise set to an hour between 0h (midnight) and 23h (11 pm).
STARTING_HOUR = None

logger = logging.getLogger("dddds")


def copy_clipboard():
    time.sleep(0.3)
    pya.hotkey('ctrl', 'c')
    time.sleep(.3)  # ctrl-c is usually very fast but your program may execute faster
    return pyperclip.paste()


# Payment Deposited	Student Paid $	Receipt Send?	Invoicing Notes	Notetaking Notes	Service cut off


def random_short_pause(min_wait_s=1 / 100., max_wait_s=1 / 40.):
    """

    :param min_wait_s:
    :param max_wait_s:
    :return: A uniformly distributed random result between (min, max).
    """
    time.sleep(random.uniform(min_wait_s, max_wait_s))


def random_long_pause(min_wait_s=0.6, max_wait_s=1.5):
    """
    Sleeps for approx 1. +/- 0.4 s pause.
    :param min_wait_s:
    :param max_wait_s:
    :return: A uniformly distributed random result between (min, max).
    """
    time.sleep(random.uniform(min_wait_s, max_wait_s))


def human_write(s, fast=False, triple_click_first=True):
    """
    Writes keystrokes with small random delays in between. Simulates life lol.
    :param fast: Write all keystrokes at once with no waits in between.
    :param s: The string to type.
    :param triple_click_first: Issues a triple-click to select all text at the current mouse position before typing
    the given keystrokes.
    """
    if triple_click_first:
        pya.tripleClick()

    # initial random wait before starting the string
    random_long_pause()

    # decidedly not human-like lol
    if fast:
        pya.write(s)
    # the usual behaviour
    else:
        for _ in s:
            pya.write(_)
            random_short_pause()

    # final random wait
    random_long_pause()


def human_move_cursor(pos, mouse_travel_time=1.):
    random_long_pause()
    pya.moveTo(int(pos[0]), int(pos[1]), mouse_travel_time, pya.easeInOutQuad)
    random_long_pause()


class PositionHelper:
    """
    Helps to iteratively capture a dictionary of positions and store them for future use.

    Implicitly expects to store the captured positions to a pickle file.

    Useful for capturing the screen locations needed to use pyautogui.

    Example:
        # create a helper at a specific root directory
        pos_helper = PositionHelper.load_or_create_helper(invoice_output_dir)

        key = "WHITE_SPACE_POSITION"
        p = pos_helper.get_position(key)
        pos_helper.save_positions()

    """

    DEFAULT_PICKLE_FILENAME = "positions_helper.pickle"

    def __init__(self, root_dir=None, helper_wait_time_s=1):
        """

        :param root_dir: The parent directory where this helper is stored. CWD by default.
        """

        # defaults
        self.delay_in_s = helper_wait_time_s
        self.positions = adict()
        if root_dir is None:
            root_dir = os.getcwd()
        self.root_dir = root_dir

        # override defaults if found in file
        pickle_file = self._pickle_path(root_dir)
        if os.path.isfile(pickle_file):
            print("Loading cursor positions from {}".format(pickle_file))
            obj = pickle.load(open(pickle_file, "rb"))
            self.positions = obj.positions
            print("  found {} stored positions".format(len(obj.positions)))
            self.delay_in_s = obj.delay_in_s

    @property
    def pickle_path(self):
        return self._pickle_path(self.root_dir)

    @staticmethod
    def _pickle_path(root_dir):
        return os.path.join(root_dir, PositionHelper.DEFAULT_PICKLE_FILENAME)

    def save_positions(self):
        print("Saving cursor positions to {}".format(self.pickle_path))
        pickle.dump(self, open(self.pickle_path, "wb"))

    def get_position(self, key, force_capture=False):
        """
        Captures a position if the position has not been captured before.

        :param key:
        :param force_capture: Prompt for a new position even if the key was found.
        :return: The position tuple for the given key.
        """
        if force_capture or key not in self.positions:
            pya.alert('place your cursor in the following textbox/button location:\n{}'.format(key))

            # check interval
            inc = 1.
            total_wait = 0.
            max_wait = self.delay_in_s

            # wait at cursor position
            while total_wait < max_wait:
                print("    ... capturing in {}s".format(max_wait - total_wait))
                time.sleep(inc)
                total_wait += inc

            # capture position
            tup = pya.position()
            self.positions[key] = tup

        return self.positions[key]


def open_and_close_dst():
    # boilerplate code for position acquisition
    k_app_menu = "pinned/docked app icon"
    k_white_space = "safe whitespace to click in the main game menu"
    k_quit = "quit button"
    k_quit_confirm_yes = "confirm quit yes button"

    # start the process
    ph = PositionHelper()

    logger.info("go to app pinned to the dock/taskbar of OS")
    human_move_cursor(ph.get_position(k_app_menu))
    pya.click()

    logger.info("letting game load")
    pymsgbox.alert("waiting for the game to load (10s)", timeout=10000)

    logger.info("collect unknown parameters on the user's time")
    pymsgbox.alert("wait for the game to start and we'll collect any missing mouse positions...", timeout=5000)
    for param in [k_white_space, k_quit, k_quit_confirm_yes]:
        ph.get_position(param)

    # save parameters
    ph.save_positions()

    _msg = "All parameters have been collected, please leave the game open and enjoy your day!"
    logger.info(_msg)
    pymsgbox.alert(_msg, timeout=10000)

    # click 'Agree' at mods dialogue (deprecated since 03-2021 QoL update)
    # human_move_cursor(ph.get_position(k_mod_agree))

    logger.info("opening items: clicking through open item dialog using whitespace")
    for i in range(MAX_NUM_OPENABLES_AT_MAIN_SCREEN):
        logger.info("  clicking through item dialog {}".format(i))
        time.sleep(7.)
        human_move_cursor(ph.get_position(k_white_space))
        pya.click()
        human_move_cursor(ph.get_position(k_white_space))
        pya.click()
        time.sleep(3.)

    _msg = "quitting game"
    logger.info(_msg)
    pymsgbox.alert(_msg, timeout=5000)
    human_move_cursor(ph.get_position(k_quit))
    pya.click()

    _msg = "confirm quit game"
    logger.info(_msg)
    pymsgbox.alert(_msg, timeout=5000)
    human_move_cursor(ph.get_position(k_quit_confirm_yes))
    pya.click()


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    while True:
        # try to wait for correct starting hour
        if STARTING_HOUR is None or not isinstance(STARTING_HOUR, int):
            logger.error("Not waiting for the starting hour '{}'".format(STARTING_HOUR))
        else:
            while datetime.datetime.now().hour != STARTING_HOUR:
                # wait 1/100th of an hour
                time.sleep(3600./100)

        _button_skip = "Skip"
        _button_collect_drops = "Collect Drops"
        pymsgbox.confirm("Preparing to automatically collect Don't Starve daily drops using python. Would you like "
                         "to skip collection, just this time? Definite Daily Drop Don't Starve (DDDDS) will run again "
                         "in about a day.", title="Would you like to skip?", buttons=(_button_skip,
                                                                                      _button_collect_drops),
                         timeout=10000.)

        open_and_close_dst()

        # repeat in one day
        time.sleep(24)
