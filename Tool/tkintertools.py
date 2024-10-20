# -*- coding: utf-8 -*-
# -*- file: tkintertools.py -*-
# -*- ver: 3.11 -*-

from tkinter import *
from os import path as os_path
from tkinter.messagebox import (
    showinfo
)
from typing import (
    NoReturn
)

class ShowText(Tk):


    def __init__(self,
                 target: str, 
                 *, 
                 title: str = ""
                 ) -> NoReturn:
        super(ShowText, self).__init__()

        self.title(title)
        self.__text: str = None
        self.__Text: Text = Text()
        if os_path.isfile(target):
            with open(target, 'r', encoding="utf-8") as file:
                self.__text: str = file.read()

        else:
            self.__text: str = target


    def show(self) -> NoReturn:
        pass