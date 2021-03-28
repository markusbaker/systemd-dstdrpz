# systemd-dstdrpz 
> _aka Definite Daily Drop Don't Starve Together_

> _aka DDDDST_

What a dream! This python script automaically opens your Don't Starve Together client and opens your **login gifts**. Configure the program directly in the script (`ddddst.py`) by setting the values of the ALL_CAPS constants at the top.

The first time it runs, the program launches into a config mode that collects locations on screen using your mouse pointer. Dialog boxes will ask you to:
* hover the mouse to a specific place
* press the enter key to move on

The prompts on screen will guide you, eventually indicating that the setup is complete. The program will remain running forever, waiting about 24 hours before it wakes up and checks for the time again.

This project also includes a systemd configuration file that will automate the scheduling of  this Don't Starve Together automatic daily gift opener. Especially useful for linux users who would like to automatically collect their daily gifts without having to close and reopen the client themselves.

### Features
* automates opening/closing of the Don't Starve Together client
* automates opening of daily (and other) gifts at startup
* easy to use: guides users through first-time setup with dialog boxes
* installs python dependencies easily using pipenv
* leverages virtualenv with pipenv for quick setup

### Requirements
* python >= 3.9
* python package 'pipenv' (requires virtualenv)
* remaining requirements are in Pipfile  
* a pinned link to the game on your screen that is always visible

### Installation
* clone the repo from github
* make sure you have pipenv installed
* run pipenv to install the dependencies
* load the service script into systemd
~~~
# INCOMPLETE SETUP INSTRUCTIONS (aka setup inspiration)
# please feel free to contribute to this!

# download the code
git clone https://github.com/markusbaker/systemd-dstdrpz.git`  

# open the downloaded directory
cd systemd-dstdrpz

# make sure pipenv is installed
python -m pip install pipenv

# install the Pipfile dependencies
# also automatically creates a new virtual environment
python -m pipenv install
~~~

### Useage
The simplest useage directly invokes the python script:
```python
python ddddst.py
``` 
More advanced useages:
* invoke from your own python projects
* modify and add the systemd script (ddddst.service) to your system's /etc/systemd

### Project Life
* March 27, 2021: initial release

# Appendixes

### Install and useage on Ubuntu 20.04
* March 27 2021: python on Ubuntu is version 3.8 but version 3.9 is needed here
* [install python 3.9 using premade ppa](https://linuxize.com/post/how-to-install-python-3-9-on-ubuntu-20-04/)
* [install pip for python 3.9 using get-pip.py](https://stackoverflow.com/questions/65644782/how-to-install-pip-for-python-3-9-on-ubuntu-20-04)
* run `python3.9` instead of `python`
* to stop fullscreen window minimizing, set `export SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS=0` in .profile [as described in this SO article](https://superuser.com/questions/1144959/how-do-i-stop-fullscreen-games-from-minimizing-when-i-click-on-another-window-on). You will need to re-login your ubuntu session.
