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

from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from cchess import *

from .QtCChess_rc import *

BOARD_SIZE = (BOARD_WIDTH, BOARD_HEIGHT) = (530, 586)
BORDER, SPACE = 15, 56

#-----------------------------------------------------#

class QChessBoard(QWidget):
    try_move_signal = pyqtSignal(tuple, tuple)
 
    def __init__(self, board):

        super().__init__()
        
        self._board = board
        self.text = ''
        
        self.flip_board = False
        self.mirror_board = False
        
        self.last_pickup = None
        self.last_pickup_moves = []
        self.move_steps_show = []
        
        self.done = []

        self.move_steps_show = []

        self._board_img = QPixmap(':images/board.png')
        self.select_img = QPixmap(':images/select.png')
        self.point_img = QPixmap(':images/point.png')
        self.done_img = QPixmap(':images/done.png')
        self.over_img = QPixmap(':images/over.png')
        
        self.pieces_img = {}
        for name in ['k', 'a', 'b', 'r', 'n', 'c', 'p']:
            self.pieces_img[name] = QPixmap(':images/{}.png'.format(name))
            
        self.setAutoFillBackground(True)
        
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(40, 40, 40))
        self.setPalette(p)
        
        self.start_x = 0
        self.start_y = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.moveShowEvent)
    
    def showMove(self, p_from, p_to):
        self.last_pickup = None
        self.last_pickup_moves = []
        self.make_log_step_move(p_from, p_to)
        #self._board.move(p_from, p_to)         
        self.last_move = (p_from, p_to)
        
    def init_board(self, fen_str=None):
        self._board.from_fen(fen_str)
        self.clear_pickup()
        
    def clear_pickup(self):
        self.last_pickup = None
        self.last_pickup_moves = []
        self.update()
    
    def make_log_step_move(self, p_from, p_to):

        self.last_pickup = p_from

        self.move_steps_show = self.make_show_steps(p_from, p_to, 6)

        self.timer.start(50)

        #等待的运动绘制完成
        while len(self.move_steps_show) > 0:
            qApp.processEvents()

        self.update()
        
        self.last_pickup = None


    def logic_to_board(self, x, y):

        if self.flip_board:
            x = 8 - x
            y = 9 - y
            
        if self.mirror_board: 
            x = 8 - x
            
        board_x = BORDER + x * SPACE + self.start_x
        board_y = BORDER + (9 - y) * SPACE + self.start_y

        return (board_x, board_y)

    def board_to_logic(self, bx, by):

        x = (bx - BORDER - self.start_x) // SPACE
        y = 9 - ((by - BORDER - self.start_y) // SPACE)

        if self.flip_board:
            x = 8 - x
            y = 9 - y
        
        if self.mirror_board: 
            x = 8 - x
        
        return (x, y)

    def setFlipBoard(self, fliped):

        if fliped != self.flip_board:
            self.flip_board = fliped
            self.update()
   
    def setMirrorBoard(self, mirrored):

        if mirrored != self.mirror_board:
            self.mirror_board = mirrored
            self.update()
   
    def closeEvent(self, event):
        self.timer.stop()

    def moveShowEvent(self):
        if len(self.move_steps_show) == 0:
            self.timer.stop()
        else:
            self.update()
            
    def resizeEvent(self, ev):

        self.start_x = (ev.size().width() - BOARD_WIDTH) // 2
        if self.start_x < 0:
            self.start_x = 0

        self.start_y = (ev.size().height() - BOARD_HEIGHT + 30) // 2
        if self.start_y < 0:
            self.start_y = 0
        
    def paintEvent(self, ev):
        painter = QPainter(self)
        if self.text != '':
            painter.setPen(QColor(34, 168, 3))
            painter.setFont(QFont('Decorative', 16))
            er = ev.rect()
            rect = QRect(er.left(), er.top(), er.width(), 30) 
            painter.drawText(rect, Qt.AlignCenter, self.text)
        
        painter.drawPixmap(self.start_x, self.start_y, self._board_img)
                
        for piece in self._board.get_pieces():
            board_x, board_y = self.logic_to_board(piece.x, piece.y)

            if piece.side == ChessSide.RED:
                offset = 0
            else:
                offset = 53

            painter.drawPixmap(
                QPoint(board_x, board_y), self.pieces_img[piece.fench.lower()],
                QRect(offset, 0, 52, 52))
            
            if (piece.x, piece.y) == self.last_pickup:
                painter.drawPixmap(
                    QPoint(board_x, board_y), self.select_img,
                    QRect(0, 0, 52, 52))
        
        for move_it in self.last_pickup_moves:
            board_x, board_y = self.logic_to_board(*move_it[1])
            painter.drawPixmap(
                    QPoint(board_x, board_y), self.point_img,
                    QRect(0, 0, 52, 52))
        
        if len(self.move_steps_show) > 0:
            piece, step_point = self.move_steps_show.pop(0)

            if piece.side == ChessSide.RED:
                offset = 0
            else:
                offset = 53

            painter.drawPixmap(
                QPoint(step_point[0], step_point[1]), self.pieces_img[piece.fench.lower()],
                QRect(offset, 0, 52, 52))
            #painter.drawPixmap(
            #    QPoint(step_point[0], step_point[1]), self.select_img,
            #    QRect(offset, 0, 52, 52))
        
         

    def minimumSizeHint(self):
        return QSize(BOARD_WIDTH, BOARD_HEIGHT+40)

    def sizeHint(self):
        return QSize(BOARD_WIDTH, BOARD_HEIGHT+40)

    def mousePressEvent(self, mouseEvent):
        if (mouseEvent.button() != Qt.LeftButton):
            return
            
        if len(self.move_steps_show) > 0:
            return

        pos = mouseEvent.pos()
        key = x, y = self.board_to_logic(pos.x(), pos.y())
         
        #数据合法校验
        if key[0] < 0 or key[0] > 8:
            return
        if key[1] < 0 or key[1] > 9:
            return
        
        piece = self._board.get_piece(key)
        
        if piece and piece.side == self._board.move_side:
                #pickup and clear last move
                self.last_pickup = key
                self.last_pickup_moves = list(self._board.create_piece_moves(key))
                
        else:
                # move check
                if self.last_pickup and key != self.last_pickup:
                    #app.try_move(self.last_pickup, key)
                    self.try_move_signal.emit(self.last_pickup, key)
                    #pass
                    
        self.update()

    def mouseMoveEvent(self, mouseEvent):
        pass

    def mouseReleaseEvent(self, mouseEvent):
        pass

    def make_show_steps(self, p_from, p_to, step_diff):

        move_man = self._board.get_piece(p_from)

        board_p_from = self.logic_to_board(p_from[0], p_from[1])
        board_p_to = self.logic_to_board(p_to[0], p_to[1])

        step = ((board_p_to[0] - board_p_from[0]) // step_diff,
                (board_p_to[1] - board_p_from[1]) // step_diff)

        steps = []

        for i in range(step_diff):

            x = board_p_from[0] + step[0] * i
            y = board_p_from[1] + step[1] * i

            steps.append((move_man, (x, y)))

        steps.append((move_man, board_p_to))

        return steps

