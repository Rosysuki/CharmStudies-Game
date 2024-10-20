# -*- coding: utf-8 -*-
# -*- file: pygametools.py -*-
# -*- ver: pygame 2.5.0 python 3.11.4 -*-

__all__: list = [
        "Button",
        "Buttons", 
        "Screen"
    ]

import pygame
from pygame.locals import *
from os import path as os_path
from functools import wraps, lru_cache
from types import NoneType
from pprint import pp

from abc import (
    ABC, 
    abstractmethod
)

from typing import (
    NoReturn, 
    Any, 
    Callable, 
    Self, 
    Union, 
    Final, 
    final
)


@lambda func : func()
def blessing() -> Callable:
    if not pygame.get_init() and (res := pygame.init())[1]:
        raise pygame.error(
            f"pygame init failed！\nSuccess: {res[0]}\tFail: {res[1]}"
        )
    return final


class Screen(ABC):


    @abstractmethod
    def update(self, pos: tuple[int, int], Any: Any) -> bool|NoReturn:
        ...


    @abstractmethod
    def show(self, screen: pygame.SurfaceType, Any: Any) -> NoReturn:
        ...


    @lru_cache
    def image(file: Union[str, pygame.SurfaceType],
              *, 
              alpha: bool = False, 
              colorkey: bool = False, 
              color: tuple = (255, 255, 255), 
              resize: bool = False, 
              angle: float = 1.0, 
              ratio: float = 0.8, 
              pixel: int = 255
              ) -> pygame.surface.Surface:
        
        if not isinstance(file, pygame.Surface):
            image: pygame.SurfaceType  = pygame.image.load(file).convert_alpha() if alpha else pygame.image.load(file).convert()
        image = pygame.transform.rotozoom(image, angle, ratio) if resize else image
        image.set_colorkey(color) if colorkey else None
        image.set_alpha(pixel)
        return image

    
    @lru_cache
    def text(text: str, 
             *, 
             sysfont: bool = True, 
             font: str = "幼圆", 
             color: tuple = (255, 255, 255), 
             size: int = 36, 
             bold: bool = False ,
             italic: bool = False, 
             bg: Union[tuple, None] = None
             ) -> pygame.surface.Surface:
        
        font: pygame.font.FontType = pygame.font.SysFont(font, size, bold, italic) if sysfont else pygame.font.Font(font, size)
        return font.render(text, True, color, bg)
    

class TextInfo(dict):
    
    def __init__(self, 
                 text: str, 
                 xy: tuple[int, int], 
                 *, 
                 sysfont: bool = True, 
                 font: str = "幼圆", 
                 color: tuple = (255, 255, 255), 
                 size: int = 36, 
                 bold: bool = False ,
                 italic: bool = False, 
                 bg: Union[tuple, None] = None, 
                 **kwargs: tuple
                 ) -> NoReturn:
        
        self |= kwargs
        self["text"] = text
        self["xy"] = xy


class ImageInfo(dict):
    pass


class Button(Screen, dict):
    

    def __init__(self,
                 name: str, 
                 pos: tuple[int, int],
                 size: tuple[int, int],
                 file: str = None,
                 font: str = None
                 ) -> NoReturn:
        
        super(Button, self).__init__()
        self["pos"] = pos
        self["size"] = size
        self["name"] = name
        self["image"] = None
        self.__styles: dict[str: Callable] = {
                "image": self.image,
                "text": self.text
            }
        
        if file is not None:
            if not isinstance(file, str):
                raise TypeError("param: file is string-type!")
            self["file"] = file

        if font is not None:
            if not isinstance(font, str):
                raise TypeError("param: font is string-type!")
            self["font"] = font


    def is_clicked(self, pos: tuple[int, int]) -> bool:
        return self["pos"][0] <= pos[0] <= self["pos"][0] + self["size"][0] and \
               self["pos"][1] <= pos[1] <= self["pos"][1] + self["size"][1]


    def image(self,
              screen: pygame.SurfaceType,
              xy: tuple[int, int] = None, 
              *,
              file: str = None, 
              alpha: bool = False, 
              colorkey: bool = False, 
              color: tuple = (255, 255, 255), 
              resize: bool = False, 
              angle: float = 1.0, 
              ratio: float = 0.8, 
              pixel: int = 255, 
              auto: bool = True,
              adapt: bool = True
              ) -> tuple[int, int, Self]:

        file: str = file if file is not None else self["file"]
        xy: tuple = xy if xy is not None else self["pos"]

        if self["image"] is None:
            image0: pygame.SurfaceType = super(Button, self).image(
                    file, 
                    alpha=alpha,
                    colorkey=colorkey, 
                    color=color, 
                    resize=resize,
                    angle=angle, 
                    ratio=ratio, 
                    pixel=pixel
            )
            self["image"] = image0
        else:
            image0 = self["image"]

        screen.blit(image0, xy)
        pygame.display.flip() if auto else None
        self["size"] = (image0.get_width(), image0.get_height()) if adapt else self["pos"]
        return (image0.get_width(), image0.get_height(), self)


    def text(self,
             text0: str,
             xy: tuple[int, int] = None,
             *,
             font: str = None,
             size: int = 36,
             color: tuple = (255, 255, 255),
             auto: bool = True, 
             sysfont: bool = True, 
             bold: bool = False, 
             italic: bool = False, 
             bg: Any = None
             ) -> tuple[pygame.font.FontType, Self]:

        try:
            font: str = font if font is not None else self["font"]
        except KeyError as KE:
            raise KE("you should have param/key: font!")

        xy: tuple = xy if xy is not None else self["pos"]

        _font: pygame.font.FontType = super().text(
            text0, 
            xy, 
            sysfont=sysfont, 
            font=font, 
            color=color, 
            size=size, 
            bold=bold, 
            italic=italic, 
            bg=bg
        )

        return (_font, self)


    def click(self,
              pos: tuple[int, int],
              reaction: Callable[[Any], Any] = lambda : print("click!"),
              *args: tuple,
              **kwargs: dict
              ) -> bool:

        if (signal := self.is_clicked(pos)):
            reaction(*args, **kwargs)
        return signal


    def init(self, command: str) -> dict|None:
        return self.pop(command) if command in self else None
    

    def show(self, option: str, *args: tuple, **kwargs: dict) -> NoReturn:
        return self.__styles[option](
            *args, 
            **kwargs
        )


    def update(self, pos: tuple[int, int], 
               reaction: Callable, 
               *args: tuple, 
               **kwargs: dict
               ) -> bool:
        
        return self.click(
            pos, 
            reaction=reaction, 
            *args, 
            **kwargs
        )


class Buttons(object):


    def __init__(self, *buttons: tuple[Button]) -> NoReturn:

        if not all(map(lambda e: isinstance(e, Button), buttons)):
            raise TypeError("Buttons only recv Button-obj!")

        self.__buttons: tuple[Button] = buttons
        self.__memory: dict[str: dict[str: Any]] = {}


    def click(self, pos: tuple[int, int]) -> Any:
        
        for index ,btn in enumerate(self.__buttons, start=1):
            if btn.is_clicked(pos):
                memory: dict[str: Any] = self.__memory[btn["name"]]
                res: Any = memory["reaction"](*memory["args"], **memory["kwargs"])
                return True if isinstance(res, NoneType) else res
        else:
            return False


    def register(self, 
                 name: str,
                 function: Callable, 
                 *args: tuple, 
                 **kwargs: dict
                 ) -> NoReturn:

        self.__memory[name] = self.__memory.get(name, {
                "reaction": function, 
                "args": args, 
                "kwargs": kwargs
            }
        )


    def register_wraps(self, 
                       name: str,
                       *args: tuple, 
                       **kwargs: dict
                       ) -> NoReturn:

        @wraps(function)
        def wrapper(function: Callable[[Any], Any]) -> Callable:
            self.register(name, function, *args, **kwargs)
            return function
        
        return wrapper
        

    def unregister(self, name: str) -> dict[str: dict[str: Any]]|bool:
        return self.__memory.pop(name) if name in self.__memory else False


class Cursor(Screen):


    def __init__(self,
                 file: str,
                 *,
                 hide: bool = False, 
                 colorkey: bool = False, 
                 color: tuple = (255, 255, 255), 
                 resize: bool = False, 
                 angle: float = 1.0, 
                 ratio: float = 0.8, 
                 pixel: int = 255, 
                 pos: tuple[int] = (0, 0), 
                 offset: tuple[float] = (0.0, 0.0)
                 ) -> NoReturn:
        
        if not os_path.exists(file):
            raise FileNotFoundError(f"path: {file} not exists!")
        #self.__file: str = file

        pygame.mouse.set_visible(hide)

        image: pygame.SurfaceType = super(Cursor, self).image(
            file, 
            colorkey=colorkey, 
            color=color, 
            resize=resize, 
            angle=angle, 
            ratio=ratio, 
            pixel=pixel
        )

        self.__offset: tuple = offset
        self.__image: pygame.image = image
        self.__pos: tuple = (pos[0]+offset[0], pos[1]+offset[1])


    def show(self, screen: pygame.SurfaceType) -> NoReturn:
        screen.blit(self.__image, self.__pos)


    def update(self, pos: tuple[int, int]) -> NoReturn:
        self.__pos: tuple = (pos[0]+self.__offset[0], pos[1]+self.__offset[1])


if __name__.__eq__("__main__"):
    ...
