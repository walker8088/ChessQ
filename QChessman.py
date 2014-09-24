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

from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui  import *

from cchess import  *
from QChess_rc import *

#-----------------------------------------------------#

chessman_image = ['king.png',
                  'advisor.png',
                  'bishop.png',
                  'knight.png',
                  'rook.png',
                  'cannon.png',
                  'pawn.png']

#-----------------------------------------------------#

class QChessman(Chessman):
    def __init__(self, parent, kind, color, pos):
        super(QChessman,self).__init__(parent, kind, color, pos)        
        self.image = QPixmap()
        self.image.load(':images/' + chessman_image[kind]) #.convert_alpha()

