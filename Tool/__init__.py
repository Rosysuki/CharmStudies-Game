# -*- coding: utf-8 -*-
# -*- file: __init__.py -*-

try:
    from .pygametools import *
except ImportError as IE:
    IE("pygametools.py无法正常导入！")

try:
    from .wraptools import *
except ImportError as IE:
    IE("wraptools.py无法正常导入！")

try:
    from .tkintertools import *
except ImportError as IE:
    IE("tkintertools.py无法正常导入！")

if __name__ == "__main__":
    pass