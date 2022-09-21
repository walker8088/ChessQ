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

from .utils import *
from .QtCChess_rc import *

BOARD_SIZE = (BOARD_WIDTH, BOARD_HEIGHT) = (530, 586)
BORDER, SPACE = 15, 56
SHOW_RATIO = 1.0

#-----------------------------------------------------#
class QChessBoardBase(QWidget):
    def __init__(self, board):

        super().__init__()
        
        self._board = board
        
        self.flip_board = False
        self.mirror_board = False
        
        self.last_pickup = None
    
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
    
    def init_board(self, fen_str=''):
        self._board.from_fen(fen_str)
        self.clear_pickup()
        
    def clear_pickup(self):
        self.last_pickup = None
        self.update()
    
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
   
    def resizeEvent(self, ev):

        self.start_x = (ev.size().width() - BOARD_WIDTH) // 2
        if self.start_x < 0:
            self.start_x = 0

        self.start_y = (ev.size().height() - BOARD_HEIGHT + 30) // 2
        if self.start_y < 0:
            self.start_y = 0
        
    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.drawPixmap(self.start_x, self.start_y, self._board_img)
                
        for piece in self._board.get_pieces():
            board_x, board_y = self.logic_to_board(piece.x, piece.y)

            if piece.color == RED:
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
        
         
    def minimumSizeHint(self):
        return QSize(BOARD_WIDTH, BOARD_HEIGHT+40)

    def sizeHint(self):
        return QSize(BOARD_WIDTH, BOARD_HEIGHT+40)

    def mousePressEvent(self, mouseEvent):
        
        if self.view_only:
            return
        
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
        
        if piece and piece.color == self._board.move_player.color:
                #pickup and clear last move
                self.last_pickup = key
                self.last_pickup_moves = list(self._board.create_piece_moves(key))
                
        else:
                # move check
                if self.last_pickup and key != self.last_pickup:
                    #app.try_move(self.last_pickup, key)
                    self.try_move(self.last_pickup, key)
                    #pass
                    
        self.update()

    def mouseMoveEvent(self, mouseEvent):
        pass

    def mouseReleaseEvent(self, mouseEvent):
        pass


'''    
class QChessBoard(QWidget):
    try_move_signal = pyqtSignal(tuple, tuple)
 
    def __init__(self, board):

        super().__init__()
        
        self._board = board
        self.text = ''
        self.view_only = False
        
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
    
    def set_view_only(self, yes):
        self.view_only = yes
        
    def show_move(self, p_from, p_to):
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

            if piece.color == RED:
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

            if piece.color == RED:
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
        
        if self.view_only:
            return
        
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
        
        if piece and piece.color == self._board.move_player.color:
                #pickup and clear last move
                self.last_pickup = key
                self.last_pickup_moves = list(self._board.create_piece_moves(key))
                
        else:
                # move check
                if self.last_pickup and key != self.last_pickup:
                    #app.try_move(self.last_pickup, key)
                    self.try_move(self.last_pickup, key)
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
    
    def try_move(self, move_from, move_to):
    
        if not self._board.is_valid_move(move_from, move_to):
            self.clear_pickup()
            return False

        checked = self._board.is_checked_move(move_from, move_to)
        if checked:
            #if self.last_checked:
            #    msg = "    必须应将!    "
            #else:
            msg = "    不能送将!    "
             
            msgbox = TimerMessageBox(msg, timeout = 1)
            msgbox.exec_()
                
            return False
            
        self.try_move_signal.emit(move_from, move_to)
        return True
'''    

class QChessBoard(QChessBoardBase):
    try_move_signal = pyqtSignal(tuple, tuple)
 
    def __init__(self, board):

        super().__init__(board)
        
        self._board = board
        self.text = ''
        self.view_only = False
        
        self.last_pickup = None
        self.last_pickup_moves = []
        self.move_steps_show = []
        
        self.done = []

        self.move_steps_show = []

        self.start_x = 0
        self.start_y = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.moveShowEvent)
    
    def set_view_only(self, yes):
        self.view_only = yes
        
    def show_move(self, p_from, p_to):
        self.last_pickup = None
        self.last_pickup_moves = []
        self.make_log_step_move(p_from, p_to)
        #self._board.move(p_from, p_to)         
        self.last_move = (p_from, p_to)
        
    #def init_board(self, fen_str=None):
    #    self._board.from_fen(fen_str)
    #    self.clear_pickup()
        
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
        super().paintEvent(ev)
        
        painter = QPainter(self)
        
        if self.text != '':
            painter.setPen(QColor(34, 168, 3))
            painter.setFont(QFont('Decorative', 16))
            er = ev.rect()
            rect = QRect(er.left(), er.top(), er.width(), 30) 
            painter.drawText(rect, Qt.AlignCenter, self.text)
        
        for move_it in self.last_pickup_moves:
            board_x, board_y = self.logic_to_board(*move_it[1])
            painter.drawPixmap(
                    QPoint(board_x, board_y), self.point_img,
                    QRect(0, 0, 52, 52))
        
        if len(self.move_steps_show) > 0:
            piece, step_point = self.move_steps_show.pop(0)

            if piece.color == RED:
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
        
        if self.view_only:
            return
        
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
        
        if piece and piece.color == self._board.move_player.color:
                #pickup and clear last move
                self.last_pickup = key
                self.last_pickup_moves = list(self._board.create_piece_moves(key))
                
        else:
                # move check
                if self.last_pickup and key != self.last_pickup:
                    #app.try_move(self.last_pickup, key)
                    self.try_move(self.last_pickup, key)
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
    
    def try_move(self, move_from, move_to):
    
        if not self._board.is_valid_move(move_from, move_to):
            self.clear_pickup()
            return False

        checked = self._board.is_checked_move(move_from, move_to)
        if checked:
            #if self.last_checked:
            #    msg = "    必须应将!    "
            #else:
            msg = "    不能送将!    "
             
            msgbox = TimerMessageBox(msg, timeout = 1)
            msgbox.exec_()
                
            return False
            
        self.try_move_signal.emit(move_from, move_to)
        return True


class QChessBoardEditWidget(QChessBoardBase):
    def __init__(self):
        
        QChessBoardBase.__init__(self, ChessBoard())

        self.last_selected = None
        self._new_pos = None

        self.createContextMenu()

    def createContextMenu(self):

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, pos):

        x, y = self.board_to_logic(pos.x(), pos.y())

        if (x, y) in list(self._board.keys()):
            self.last_selected = (x, y)
        else:
            self._new_pos = (x, y)

        fen_str = self.get_fen()

        self.contextMenu = QtGui.QMenu(self)

        actionDel = self.contextMenu.addAction('删除')
        if not self.last_selected:
            actionDel.setEnabled(False)

        readMenu = self.contextMenu.addMenu('添加红方棋子')

        actionAdd_RK = readMenu.addAction("帅")
        if fen_str.count("K") > 0:
            actionAdd_RK.setEnabled(False)

        actionAdd_RA = readMenu.addAction("仕")
        if fen_str.count("A") > 1:
            actionAdd_RA.setEnabled(False)

        actionAdd_RB = readMenu.addAction("相")
        if fen_str.count("B") > 1:
            actionAdd_RB.setEnabled(False)

        actionAdd_RN = readMenu.addAction("马")
        if fen_str.count("N") > 1:
            actionAdd_RN.setEnabled(False)

        actionAdd_RR = readMenu.addAction("车")
        if fen_str.count("R") > 1:
            actionAdd_RR.setEnabled(False)

        actionAdd_RC = readMenu.addAction("炮")
        if fen_str.count("C") > 1:
            actionAdd_RC.setEnabled(False)

        actionAdd_RP = readMenu.addAction("兵")
        if fen_str.count("P") > 4:
            actionAdd_RP.setEnabled(False)

        blackMenu = self.contextMenu.addMenu('添加黑方棋子')

        actionAdd_BK = blackMenu.addAction("将")
        if fen_str.count("k") > 0:
            actionAdd_BK.setEnabled(False)

        actionAdd_BA = blackMenu.addAction("士")
        if fen_str.count("a") > 1:
            actionAdd_BA.setEnabled(False)

        actionAdd_BB = blackMenu.addAction("象")
        if fen_str.count("b") > 1:
            actionAdd_BB.setEnabled(False)

        actionAdd_BN = blackMenu.addAction("马")
        if fen_str.count("n") > 1:
            actionAdd_BN.setEnabled(False)

        actionAdd_BR = blackMenu.addAction("车")
        if fen_str.count("r") > 1:
            actionAdd_BR.setEnabled(False)

        actionAdd_BC = blackMenu.addAction("炮")
        if fen_str.count("c") > 1:
            actionAdd_BC.setEnabled(False)

        actionAdd_BP = blackMenu.addAction("卒")
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

        if self.last_selected:
            self.remove_chessman(self.last_selected)
            self.last_selected = None
            self.update()

    def onActionAdd_RK(self):
        self.onActionAddChessman(KING, RED)

    def onActionAdd_BK(self):
        self.onActionAddChessman(KING, BLACK)

    def onActionAdd_RA(self):
        self.onActionAddChessman(ADVISOR, RED)

    def onActionAdd_BA(self):
        self.onActionAddChessman(ADVISOR, BLACK)

    def onActionAdd_RB(self):
        self.onActionAddChessman(BISHOP, RED)

    def onActionAdd_BB(self):
        self.onActionAddChessman(BISHOP, BLACK)

    def onActionAdd_RN(self):
        self.onActionAddChessman(KNIGHT, RED)

    def onActionAdd_BN(self):
        self.onActionAddChessman(KNIGHT, BLACK)

    def onActionAdd_RR(self):
        self.onActionAddChessman(ROOK, RED)

    def onActionAdd_BR(self):
        self.onActionAddChessman(ROOK, BLACK)

    def onActionAdd_RC(self):
        self.onActionAddChessman(CANNON, RED)

    def onActionAdd_BC(self):
        self.onActionAddChessman(CANNON, BLACK)

    def onActionAdd_RP(self):
        self.onActionAddChessman(PAWN, RED)

    def onActionAdd_BP(self):
        self.onActionAddChessman(PAWN, BLACK)

    def onActionAddChessman(self, type, color):

        if not self._new_pos:
            return False

        man = self.create_chessman(type, color, self._new_pos)

        self._new_pos = None
        self.update()

    def to_fen(self):
        return self._board.to_fen()
    
    '''
    def clear(self):
        self.board.clear(self)

        self.last_selected = ()
        self.update()
    '''
    
    def on_create_chessman(self, kind, color, pos):

        man = QChessman(self, kind, color, pos)

        if man.can_place_to(pos[0], pos[1]):
            return man

        return None

    def paintEvent(self, ev):
        super().paintEvent(ev)
        
        painter = QPainter(self)
        '''
        for key in list(self._board.keys()):

            chessman = self._board[key]

            board_x, board_y = self.logic_to_board(chessman.x, chessman.y)

            if chessman.color == RED:
                offset = 0
            else:
                offset = 53

            painter.drawPixmap(
                QPoint(board_x, board_y), chessman.image,
                QRect(offset, 0, 52, 52))

            if key == self.last_selected:
                painter.drawPixmap(
                    QPoint(board_x, board_y), self._select_img,
                    QRect(offset, 0, 52, 52))
        '''    
        
    def mousePressEvent(self, mouseEvent):
        if (mouseEvent.button() != Qt.LeftButton):
            return

        pos = mouseEvent.pos()

        x, y = self.board_to_logic(pos.x(), pos.y())
        print(x,y)
        '''
        if (x, y) in list(self._board.keys()):
            self.last_selected = (x, y)

        else:
            #空击,如果已经有选过，则可能是走子
            if self.last_selected:

                old_man = self.board[self.last_selected]

                if old_man.can_place_to(x, y):
                    self._do_move(self.last_selected, (x, y))

                self.last_selected = None

                self.parent.update_fen()
        '''
        self.update()
        
    def mouseMoveEvent(self, mouseEvent):
        pass

    def mouseReleaseEvent(self, mouseEvent):
        pass
