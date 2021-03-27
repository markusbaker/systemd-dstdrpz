# systemd-dstdrpz
Automaically open your Don't Starve (Together) gifts with this set of simple scripts. Uses python and pyautogui to control the mouse and keyboard.

This project also includes a systemd configuration file that will automate the scheduling of  this Don't Starve (Together) item opener. Especially useful for linux users who would like to automatically collect their daily gifts without having to close and reopen the client themselves.

### Features:
* automates opening/closing of the Don't Starve Together client
* automates opening of daily (and other) gifts at startup
* easy to use: guides users through first-time setup with dialog boxes
* installs python dependencies easily using pipenv

### Requirements
* python >= 3.9
* python package 'pipenv'

### Installation
* clone the repo from github
* make sure you have pipenv installed
* run pipenv to install the dependencies

### Useage
* invoke from your own python projects
* add the systemd script to your system's /etc/systemd

### Project Life
* March 27, 2021: initial release

# Appendixes

### Install and useage on Ubuntu 20.04
* March 27 2021: python on Ubuntu is version 3.8 but version 3.9 is needed here
* [install python 3.9 using premade ppa](https://linuxize.com/post/how-to-install-python-3-9-on-ubuntu-20-04/)
* [install pip for python 3.9 using get-pip.py](https://stackoverflow.com/questions/65644782/how-to-install-pip-for-python-3-9-on-ubuntu-20-04)
* run `python3.9` instead of `python`