import pygame
import sys
import threading
import json
import pickle
import atexit
from os import path as os_path
from pygame.locals import *
from glob import glob, iglob
from tkinter import messagebox
from math import nan
from copy import deepcopy
from functools import (
    partial ,
    wraps, 
    lru_cache
)
from random import (
    randint ,
    choice ,
    shuffle
)
from typing import (
    NoReturn, 
    Self, 
    Any, 
    NewType, 
    Callable, 
    Union
)
from time import (
    time,
    sleep, 
    asctime, 
    localtime
)

from pyautogui import position

"""UserInfo: dict[str: Any] = {

}"""