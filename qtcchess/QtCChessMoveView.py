#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Copyright (C) 2014  walker li <walker8088@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import time
import yaml

from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from cchess import *

from .utils import *

from .QtCChessBoard import *
from .QtCChessWidgets import *

#-----------------------------------------------------#
class ChessMoveHistoryWindow(QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.board = ChessBoard()
       
        self.boardView = QChessBoard(self.board)
        self.setCentralWidget(self.boardView)
        self.historyView = QMoveHistoryWidget(self)
    
        self.addDockWidget(Qt.RightDockWidgetArea, self.historyView)
    
        self.resize(800, 700)
        self.center()
        
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    
#-----------------------------------------------------#
    
  