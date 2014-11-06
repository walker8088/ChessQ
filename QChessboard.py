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

BOARD_SIZE = (BOARD_WIDTH, BOARD_HEIGHT) = (530, 586)
BORDER, SPACE = 15, 56

#-----------------------------------------------------#

class QChessboard(Chessboard, QWidget):

    """
        棋盘对象
    """

    def __init__(self):
    
        QWidget.__init__(self)
        
        Chessboard.__init__(self)
        
        self.flip_board = False
        
        self.hook_move = [None,  None]
        #self.last_move = None
        self.move_side = None
        self.last_selected = None
        
        self.done = []
        
        self.move_steps_show = []
        
        self._board_img = QPixmap( ':images/board.png')
        self.select_img = QPixmap(':images/select.png')
        self.done_img = QPixmap(':images/done.png')
        self.over_img = QPixmap(':images/over.png')
        
        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)
        
        self.start_x = 0
        self.start_y = 0
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.moveShowEvent)
        
    def init_board(self, fen_str = None):
        Chessboard.init_board(self,  fen_str)

        self.last_selected = None
        
        self.update()
        
    def on_create_chessman(self, kind, color, pos):     
        
        return QChessman(self, kind, color, pos)
        
        
    def make_step_move(self, p_from, p_to):

        self.last_selected = p_from
        
        self.move_steps_show = self.make_show_steps(p_from, p_to, 6)
        
        self.timer.start(50)
        
        #等待的运动绘制完成
        while len(self.move_steps_show) > 0:
            qApp.processEvents() 
        
        Chessboard.make_step_move(self, p_from, p_to)
        
        self.update()
        
        #self.last_move = p_to
        self.last_selected = None
    
    def logic_to_board(self,  x,  y):
        
        if self.flip_board :
            x = 8 - x
            y = 9 - y 
            
        board_x = BORDER + x * SPACE + self.start_x
        board_y = BORDER + y * SPACE + self.start_y
        
        return board_x,  board_y     
    
    def board_to_logic(self, bx,  by):
        
        x = (bx - BORDER - self.start_x) / SPACE
        y = (by - BORDER - self.start_y) / SPACE
        
        if self.flip_board :
            x = 8 - x
            y = 9 - y 
        
        return x,  y
        
    def setFlipBoard(self, fliped): 
        
        if fliped != self.flip_board :
            self.flip_board = fliped
            self.update() 
    
    def closeEvent(self, event):

        self.timer.stop()
      
        
    def moveShowEvent(self):
        
        if len(self.move_steps_show) == 0:
            self.timer.stop()
            #self.hook_move_done()
        else:
            #ugly patch here 
            try:
                self.update()
            except:
                self.timer.stop()
                
    def resizeEvent(self, ev):
        
        self.start_x = (ev.size().width() - BOARD_WIDTH) / 2
        if self.start_x < 0:
            self.start_x = 0
            
        self.start_y = (ev.size().height() - BOARD_HEIGHT) / 2
        if self.start_y < 0:
            self.start_y = 0
        
    def paintEvent(self, ev):
        painter = QPainter(self)
        
        painter.drawPixmap(self.start_x, self.start_y, self._board_img)
        
        move_man = None
        if len(self.move_steps_show) > 0:
            move_man,  step_point = self.move_steps_show.pop(0)
            
            if move_man.color == RED:
                    offset = 0
            else:
                    offset = 53
                    
            painter.drawPixmap(QPoint(step_point[0], step_point[1]), move_man.image, QRect(offset, 0, 52, 52))
            painter.drawPixmap(QPoint(step_point[0], step_point[1]), self.select_img, QRect(offset, 0, 52, 52))
                
        for key in self._board.keys():
                
            chessman = self._board[key]
            if chessman == move_man:
                continue    
                
            board_x, board_y = self.logic_to_board(chessman.x,  chessman.y)
                
            if chessman.color == RED:
                    offset = 0
            else:
                    offset = 53
            
            painter.drawPixmap(QPoint(board_x, board_y), chessman.image, QRect(offset, 0, 52, 52))
            
            if key == self.last_selected:
                painter.drawPixmap(QPoint(board_x, board_y), chessman.image, QRect(offset, 0, 52, 52))
                painter.drawPixmap(QPoint(board_x, board_y), self.select_img, QRect(offset, 0, 52, 52))
              
            #if key == self.last_move:
            #    painter.drawPixmap(QPoint(board_x, board_y), self.select_img, QRect(offset, 0, 52, 52))
            
    def minimumSizeHint(self):
        return QSize(BOARD_WIDTH, BOARD_HEIGHT) 

    def sizeHint(self):
        return QSize(BOARD_WIDTH, BOARD_HEIGHT) 
        
    def mousePressEvent(self, mouseEvent):
        if (mouseEvent.button() != Qt.LeftButton):
            return
            
        pos = mouseEvent.pos()
        
        ax, ay = pos.x(), pos.y()
        
        x, y = self.board_to_logic(ax,  ay)
        
        if (x, y) in self._board.keys():
            #选中某个棋子，可以多次选当前可走方的棋子
            new_man = self._board[(x, y)]                        
            if new_man.color == self.move_side:
                #选中的是可走方的棋子
                self.last_selected = (x, y)
                #self.last_move = new_man        
            else:
                #以前没选中，现在选中的是对方的棋子，不动作
                if not self.last_selected :
                    return
                
                #可能是吃子，交由player自己管理
                if  self.hook_move[self.move_side] :
                    self.hook_move[self.move_side](self.last_selected, (x,y))
                    
        else :
            #空击,如果已经有选过，则可能是走子
            if self.last_selected and  self.hook_move[self.move_side] :
                self.hook_move[self.move_side](self.last_selected, (x,y))
                        
        self.update()
                
    def mouseMoveEvent(self, mouseEvent):
        pass
        
    def mouseReleaseEvent(self, mouseEvent):
        pass
        
    def make_show_steps(self,  p_from, p_to, step_diff):
        
        move_man = self._board[p_from]
        
        board_p_from =  self.logic_to_board(p_from[0],  p_from[1]) 
        board_p_to = self.logic_to_board(p_to[0],  p_to[1]) 
        
        step = ((board_p_to[0] - board_p_from[0]) / step_diff, (board_p_to[1] - board_p_from[1]) / step_diff)
        
        steps = []
        
        for i in range(step_diff):
            
            x = board_p_from[0] + step[0] * i
            y = board_p_from[1] + step[1] * i
            
            steps.append((move_man,  (x, y)))
        
        steps.append((move_man,  board_p_to))
        
        return steps 
        
    def set_hook_move(self, side, move_func):
        self.hook_move[side] = move_func
    
