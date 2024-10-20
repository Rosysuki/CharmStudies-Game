"""CharmLexicon Get Illness ,So I Create This."""
from static.include import pygame,choice,shuffle,asyncio

def together(key:list|tuple ,items:list|tuple) -> dict:
    return dict(zip(key ,items))

def saveData(target:list|tuple|dict ,**fmt:str) -> str:
    if not fmt["encode"]:
        with open(fmt["fmt"] ,fmt["mode"]) as file:
            pass


