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

import sys, time

from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui  import *

from cchess import  *
from QChess_rc import *
from QChessman import *

#-----------------------------------------------------#
                  
BOARD_SIZE = (BOARD_WIDTH, BOARD_HEIGHT) = (530, 586)
BORDER, SPACE = 15, 56
                  
#-----------------------------------------------------#

class QChessboardEditWidget(Chessboard, QWidget):
    
    def __init__(self):
    
        QWidget.__init__(self)
        
        Chessboard.__init__(self)
        
        self.last_selected = None
        self._new_pos = None
        
        self._board_img = QPixmap( ':images/board.png')
        self._select_img = QPixmap(':images/select.png')
        
        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)
        
        self.createContextMenu()  
  
  
    def createContextMenu(self):  
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)  
        self.customContextMenuRequested.connect(self.showContextMenu)  
  
    def showContextMenu(self, pos):  
        
        x, y = self.board_to_logic(pos.x(),  pos.y())   
        
        print x, y
        
        if (x, y) in self._board.keys():
            self.last_selected = (x, y)
        else :
            self._new_pos = (x, y)
        
        
        fen_str = self.get_fen()
        
        self.contextMenu = QtGui.QMenu(self)  
        
        actionDel = self.contextMenu.addAction(u'删除')  
        if not self.last_selected :
            actionDel.setEnabled(False)
            
        readMenu = self.contextMenu.addMenu(u'添加红方棋子')
        
        actionAdd_RK = readMenu.addAction(u"帅")
        if fen_str.count("K") > 0:
            actionAdd_RK.setEnabled(False)
            
        actionAdd_RA = readMenu.addAction(u"仕")
        if fen_str.count("A") > 1:
            actionAdd_RA.setEnabled(False)
        
        actionAdd_RB = readMenu.addAction(u"相")
        if fen_str.count("B") > 1:
            actionAdd_RB.setEnabled(False)
        
        actionAdd_RN = readMenu.addAction(u"马")
        if fen_str.count("N") > 1:
            actionAdd_RN.setEnabled(False)
        
        actionAdd_RR = readMenu.addAction(u"车")
        if fen_str.count("R") > 1:
            actionAdd_RR.setEnabled(False)
        
        actionAdd_RC = readMenu.addAction(u"炮")
        if fen_str.count("C") > 1:
            actionAdd_RC.setEnabled(False)
        
        actionAdd_RP = readMenu.addAction(u"兵")
        if fen_str.count("P") > 4:
            actionAdd_RP.setEnabled(False)
        
        blackMenu = self.contextMenu.addMenu(u'添加黑方棋子')  
        
        actionAdd_BK = blackMenu.addAction(u"将")
        if fen_str.count("k") > 0:
            actionAdd_BK.setEnabled(False)
        
        actionAdd_BA = blackMenu.addAction(u"士")
        if fen_str.count("a") > 1:
            actionAdd_BA.setEnabled(False)
        
        actionAdd_BB = blackMenu.addAction(u"象")
        if fen_str.count("b") > 1:
            actionAdd_BB.setEnabled(False)
        
        actionAdd_BN = blackMenu.addAction(u"马")
        if fen_str.count("n") > 1:
            actionAdd_BN.setEnabled(False)
        
        actionAdd_BR = blackMenu.addAction(u"车")
        if fen_str.count("r") > 1:
            actionAdd_BR.setEnabled(False)
        
        actionAdd_BC = blackMenu.addAction(u"炮")
        if fen_str.count("c") > 1:
            actionAdd_BC.setEnabled(False)
        
        actionAdd_BP = blackMenu.addAction(u"卒")
        if fen_str.count("p") > 4:
            actionAdd_BP.setEnabled(False)
        
        actionDel.triggered.connect(self.onActionDel)  
        
        actionAdd_RK.triggered.connect(self.onActionAdd_RK) 
        actionAdd_RA.triggered.connect(self.onActionAdd_RA) 
        actionAdd_RB.triggered.connect(self.onActionAdd_RB) 
        actionAdd_RN.triggered.connect(self.onActionAdd_RN) 
        actionAdd_RR.triggered.connect(self.onActionAdd_RR) 
        actionAdd_RC.triggered.connect(self.onActionAdd_RC) 
        actionAdd_RP.triggered.connect(self.onActionAdd_RP) 
        
        actionAdd_BK.triggered.connect(self.onActionAdd_BK) 
        actionAdd_BA.triggered.connect(self.onActionAdd_BA) 
        actionAdd_BB.triggered.connect(self.onActionAdd_BB) 
        actionAdd_BN.triggered.connect(self.onActionAdd_BN) 
        actionAdd_BR.triggered.connect(self.onActionAdd_BR) 
        actionAdd_BC.triggered.connect(self.onActionAdd_BC) 
        actionAdd_BP.triggered.connect(self.onActionAdd_BP) 
          
        self.contextMenu.move(QCursor.pos())  
        self.contextMenu.show()
    
    def onActionDel(self):
        
        if self.last_selected :
            self.remove_chessman(self.last_selected)
            self.last_selected = None    
            self.update()
                
    def onActionAdd_RK(self):
        self.onActionAddChessman(KING , RED)
    
    def onActionAdd_BK(self):
        self.onActionAddChessman(KING , BLACK)
    
    def onActionAdd_RA(self):
        self.onActionAddChessman(ADVISOR , RED)
    
    def onActionAdd_BA(self):
        self.onActionAddChessman(ADVISOR , BLACK)
    
    def onActionAdd_RB(self):
        self.onActionAddChessman(BISHOP , RED)
    
    def onActionAdd_BB(self):
        self.onActionAddChessman(BISHOP , BLACK)
    
    def onActionAdd_RN(self):
        self.onActionAddChessman(KNIGHT , RED)
    
    def onActionAdd_BN(self):
        self.onActionAddChessman(KNIGHT , BLACK)
    
    def onActionAdd_RR(self):
        self.onActionAddChessman(ROOK , RED)
    
    def onActionAdd_BR(self):
        self.onActionAddChessman(ROOK , BLACK)
    
    def onActionAdd_RC(self):
        self.onActionAddChessman(CANNON , RED)
    
    def onActionAdd_BC(self):
        self.onActionAddChessman(CANNON , BLACK)
    
    def onActionAdd_RP(self):
        self.onActionAddChessman(PAWN , RED)
    
    def onActionAdd_BP(self):
        self.onActionAddChessman(PAWN , BLACK)
        
    def onActionAddChessman(self, type, color):
        
        if not self._new_pos:
            return False
            
        man = self.create_chessman(type,  color,  self._new_pos)
        
        self._new_pos = None
        self.update()
        
    def init_board(self, fen_str = None):
        
        Chessboard.init_board(self,  fen_str)
        
        self.last_selected = ()
        self.update()
    
    def clear(self):
        Chessboard.clear(self)
        
        self.last_selected = ()
        self.update()
        
    def on_create_chessman(self, kind, color, pos):     
        
        man = QChessman(self, kind, color, pos)
        
        if man.can_place_to(pos[0], pos[1]) :
           return man
        
        return None
        
    def logic_to_board(self,  x,  y):
        
        board_x = BORDER + x * SPACE
        board_y = BORDER + y * SPACE
        
        return board_x,  board_y     
    
    def board_to_logic(self, bx,  by):
        
        x = (bx - BORDER) / SPACE
        y = (by - BORDER) / SPACE
        
        return x,  y
        
    def paintEvent(self, ev):
        painter = QPainter(self)
        
        painter.drawPixmap(0, 0, self._board_img)
        
        for key in self._board.keys():
                
            chessman = self._board[key]
                
            board_x, board_y = self.logic_to_board(chessman.x,  chessman.y)
                
            if chessman.color == RED:
                    offset = 0
            else:
                    offset = 53
            
            painter.drawPixmap(QPoint(board_x, board_y), chessman.image, QRect(offset, 0, 52, 52))
            
            if key == self.last_selected:
                painter.drawPixmap(QPoint(board_x, board_y), self._select_img, QRect(offset, 0, 52, 52))
                
            
    def minimumSizeHint(self):
        return QSize(BOARD_WIDTH, BOARD_HEIGHT) 

    #def sizeHint(self):
    #    return QSize(BOARD_WIDTH, BOARD_HEIGHT) 
        
    def mousePressEvent(self, mouseEvent):
        if (mouseEvent.button() != Qt.LeftButton):
            return
            
        pos = mouseEvent.pos()
        
        ax, ay = pos.x(), pos.y()
        
        x, y = self.board_to_logic(ax,  ay)
        
        if (x, y) in self._board.keys():
            self.last_selected = (x, y)
                    
        else :
            #空击,如果已经有选过，则可能是走子
            if self.last_selected :
                
                old_man = self._board[self.last_selected]
                
                if old_man.can_place_to(x,  y):
                    self._do_move(self.last_selected, (x, y))    
                
                self.last_selected = None
                
        self.update()
                
    def mouseMoveEvent(self, mouseEvent):
        pass
        
    def mouseReleaseEvent(self, mouseEvent):
        pass
        
    
