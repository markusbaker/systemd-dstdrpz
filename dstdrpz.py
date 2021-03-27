import pymsgbox

from xbpy.pyautogui import PositionHelper, human_move_cursor, human_write
import pyautogui as pya
import time
import logging


MAX_NUM_OPENABLES_AT_MAIN_SCREEN = 5
LOAD_GAME_WAITTIME_S = 10.


def open_and_close_dst():
    logger = logging.getLogger(open_and_close_dst.__name__)

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

    open_and_close_dst()
