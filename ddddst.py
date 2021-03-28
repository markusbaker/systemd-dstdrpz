import datetime
import logging
import os
import pickle
import random
import time

import pyautogui as pya
import pymsgbox
from adict import adict

MAX_NUM_OPENABLES_AT_MAIN_SCREEN = 3
LOAD_GAME_WAITTIME_S = 10.

# set to None to start immediately, otherwise set to an hour between 0h (midnight) and 23h (11 pm).
STARTING_HOUR = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ddddst")


def human_move_cursor(pos, mouse_travel_time=0.7):
    pya.moveTo(int(pos[0]), int(pos[1]), mouse_travel_time, pya.easeInOutQuad)


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

    def __init__(self, root_dir=None, helper_wait_time_s=0.3):
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
            pya.alert('place your cursor in the following textbox/button location:\n{}.\n\nPress the Enter key when '
                      'ready and wait for the next prompt.'.format(key))

            # wait at cursor position
            time.sleep(self.delay_in_s)

            # capture position
            tup = pya.position()
            self.positions[key] = tup

        return self.positions[key]


def open_and_close_dst():
    # boilerplate code for position acquisition
    k_app_menu = "pinned/docked app icon"
    k_white_space = "safe whitespace to click in the main game menu"
    k_quit = "quit button"
    k_quit_confirm_yes = "confirm quit YES button"
    k_quit_confirm_no = "confirm quit NO button"

    # start the process
    ph = PositionHelper()

    logger.info("go to app pinned to the dock/taskbar of OS")
    human_move_cursor(ph.get_position(k_app_menu))
    pya.click()

    logger.info("letting game load")
    pymsgbox.alert("waiting for the game to load (10s)", timeout=30000)

    missing_params = [_ for _ in [k_white_space, k_quit, k_quit_confirm_yes, k_quit_confirm_no] if _ not in ph.positions ]
    if len(missing_params)>0:
        logger.info("collect unknown parameters")
        pymsgbox.alert("now we'll collect any missing mouse positions...", timeout=5000)
        quit_dialog_open = False
        for param in missing_params:
            # be helpful, open the quit dialog
            if param in [k_quit_confirm_no, k_quit_confirm_yes] and not quit_dialog_open:
                pymsgbox.alert("relax while I open the quit menu for you... ", timeout=2000)
                human_move_cursor(ph.get_position(k_white_space))
                pya.click()
                human_move_cursor(ph.get_position(k_quit))
                pya.click()
                quit_dialog_open = True
            ph.get_position(param)
    
        if quit_dialog_open:
            human_move_cursor(ph.get_position(k_white_space))
            pya.click()
            human_move_cursor(ph.get_position(k_quit_confirm_no))
            pya.click()
            quit_dialog_open = False
    
        _msg = "All parameters have been collected, please leave the game open and enjoy your day!"
        logger.info(_msg)
        pymsgbox.alert(_msg, timeout=6000)

        # save parameters
        ph.save_positions()
    
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


    while True:
        # try to wait for correct starting hour
        if STARTING_HOUR is None or not isinstance(STARTING_HOUR, int) or (STARTING_HOUR < 0 or STARTING_HOUR > 23):
            logger.info("Not waiting for a particular starting hour, got parameter '{}'".format(STARTING_HOUR))
        else:
            logger.info("Waiting for a particular starting hour, got time '{}h'".format(STARTING_HOUR))
            while datetime.datetime.now().hour != STARTING_HOUR:
                time.sleep(60)

        _button_skip = "Skip"
        _button_collect_drops = "Collect Drops Now"
        r = pymsgbox.confirm("Preparing to automatically collect Don't Starve daily drops using python. Would you like "
                         "to skip collection, just this time? Definite Daily Drop Don't Starve (DDDDS) will run again "
                         "in about a day.", title="Would you like to skip?", buttons=(_button_skip,
                                                                                      _button_collect_drops),
                         timeout=10000)
        
        if r in ['Timeout', _button_collect_drops]:
            logger.info("Collecting drops now!")
            open_and_close_dst()

        # repeat in about one day
        logger.info("Sleeping for about a day.")
        time.sleep(23.8*3600)
        logger.info("Running again at {}".format(datetime.datetime.now()))

