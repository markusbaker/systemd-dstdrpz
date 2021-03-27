# systemd-dstdrpz
Automaically open your Don't Starve (Together) gifts with this set of simple scripts. Uses python and pyautogui to control the mouse and keyboard.

This project also includes a systemd configuration file that will automate the scheduling of  this Don't Starve (Together) item opener. Especially useful for linux users who would like to automatically collect their daily gifts without having to close and reopen the client themselves.

### Features:
* automates opening/closing of the Don't Starve Together client
* automates opening of daily (and other) gifts at startup
* easy to use: guides users through first-time setup with dialog boxes
* installs python dependencies easily using pipenv

### Requirements
* python installed
* python package 'pipenv'

### Useage
* clone the repo from github
* make sure you have pipenv installed
* run pipenv to install the dependencies
* (optional) add the systemd script to your system's /etc/systemd

### Project Life
* March 27, 2021: initial release
