# -*- coding: utf-8 -*-
# -*- file: wraptools.py -*-
# -*- ver: 3.11.4 -*-

__doc__: str = """
Multi Wrapper Here.
"""

__all__: list = [
        "Overload" ,
        "atenter" ,
        "annotations" ,
        "read_only"
    ]

from typing import (
    NoReturn ,
    Any ,
    Callable
)

from functools import wraps
from sys import stderr
from time import time


def annotations(function: Callable) -> Callable:
    if not callable(function):
        raise Exception("AnnotationError!")

    @wraps(function)
    def wrapper(*args: tuple ,**kwargs: dict) -> Any:
        func_types: list = [value for key ,value in function.__annotations__.items() if key != "return"]
        for index ,each in enumerate([*args ,*kwargs.values()] ,start=1):
            if (std_type := each.__class__) != (real_type := func_types[index-1]):
                raise TypeError(f"Func {function.__name__} -> Arg{index}:\n\tShould Be {std_type} ,Not {real_type}!")
        else:
            function(*args ,**kwargs)
    return wrapper


class Overload(object):


    __func_dict: dict = {}


    @classmethod
    def __get_func_type(cls ,function: Callable) -> str:
        return ''.join([str(value) for key ,value in function.__annotations__.items() if key != "return"])


    @classmethod
    #@annotations
    def register(cls ,function: Callable) -> Callable:
        if not callable(function):
            raise ValueError("X")

        if (func_type := cls.__get_func_type(function)) not in cls.__func_dict:
            cls.__func_dict[func_type] = function

        @wraps(function)
        def wrapper(*args: tuple ,**kwargs: dict) -> Any:
            func_name: str = ''.join([str(each.__class__) for each in [*args ,*kwargs.values()]])
            return cls.__func_dict[func_name](*args ,**kwargs)
        return wrapper


    @classmethod
    #@annotations
    def unregister(cls ,function: Callable) -> Callable|None:
        if not callable(function):
            raise ValueError("X")

        return cls.__func_dict.pop(func_type) if (func_type := cls.__get_func_type(function)) in cls.__func_dict else None


def atenter(function: Callable) -> Callable:
    @wraps(function)
    def wrapper(*args: tuple ,**kwargs: dict) -> Any:
        return function(*args ,**kwargs)
    return wrapper()


read_only: Callable = lambda args ,kwargs : lambda function : function(*args ,**kwargs)


def timer(_round: int = 3) -> Callable:
    def decorator(function: Callable[[Any], Any]) -> Callable:
        @wraps(function)
        def wrapper(*args: tuple ,**kwargs: dict) -> float:
            begin_time: float = time()
            function(*args ,**kwargs)
            return round(time()-begin_time ,_round)
        return wrapper
    return decorator


if __name__.__eq__("__main__"):
    pass


