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

from .QtCChessBoard import *
from .QtCChessWidgets import *

#from .QChessboardEditDlg import *

#-----------------------------------------------------#

BOOK, EXERCISE, KILLING = list(range(3))

APP_NAME = "ChessQ 中国象棋"
APP_CONFIG_FILE = "ChessQ.cfg"

#-----------------------------------------------------#
class GameKeeper():
    def __init__(self, file):

        self.file = os.path.splitext(file)[0]
        self.games = []
        self.games_done = []
        self.file_eglib = self.file + '.eglib'
        self.file_eplib = self.file + '.eplib'
        self.index = -1
        
    def load(self):

        with open(self.file_eglib, 'rb') as f:
            lines = f.readlines()

        for line in lines:
            it = line.strip().decode('utf-8')
            if it.startswith('#') or  it== '':
                continue
            its = it.split('|')
            if len(its) == 3:
                self.games.append((its[0], its[1], its[2]))
            else:
                self.games.append((its[0], its[1], None))
            
        self.games_done = bytearray(b'0' * len(self.games))

        if os.path.isfile(self.file + '.eplib'):
            with open(self.file_eplib, 'rb') as f:
                done_array = bytearray(open(self.file_eplib, 'rb').read())
            for i, it in enumerate(done_array):
                if i >= len(self.games):
                    break
                if it == ord('1'):
                    self.games_done[i] = it
        self.next_new() 
        self.save_done()
    
    def all(self):
        return zip(self.games, self.games_done)
        
    def curr_game(self):
        if self.index >= 0:
            return self.games[self.index]
        else:
            return None
            
    def curr_game_done(self):
        self.games_done[self.index] = ord('1')
        self.save_done()

    def save_done(self):
        open(self.file_eplib, 'wb').write(bytes(self.games_done))
    
    def next_new(self):
        for i in range(self.index+1, len(self.games)):
            if self.games_done[i] == ord('0'):
                self.index = i
                return self.index
        self.index = 0
        return self.index 
    
    def prev_new(self):
        for i in range(self.index-1, -1, -1):
            if self.games_done[i] == ord('0'):
                self.index = i
                return self.index
        self.index = 0
        return self.index 
    
    def next_game(self):
        self.index = self.index + 1
        if self.index >= len(self.games):
            self.index = len(self.games) - 1
        return self.index
    
    def prev_game(self):
        self.index = self.index - 1
        if self.index <= 0:
            self.index = 0
        return self.index

#-----------------------------------------------------#
class TimerMessageBox(QMessageBox):
    def __init__(self, text, timeout=2):
        super().__init__()
        self.setWindowTitle("ChessQ")
        self.time_to_wait = timeout
        self.setText(text)
        self.setStandardButtons(QMessageBox.NoButton)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.changeContent)
        self.timer.start()

    def changeContent(self):
        self.time_to_wait -= 1
        if self.time_to_wait <= 0:
            self.close()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()

#-----------------------------------------------------#
class EngineThread(QThread):
    best_move_signal = pyqtSignal(tuple, tuple)
    move_probe_signal = pyqtSignal(dict)
    checkmate_signal = pyqtSignal()
    
    def __init__(self, engine):
        QThread.__init__(self)
        self.engine = engine
        self.stoped = True
        
    def run(self):
        self.stoped = False 
        while not self.stoped:
            self.engine.handle_msg_once()
            if not self.engine.move_queue.empty():
                output = self.engine.move_queue.get()
                #print(output)
                if output[0] == 'best_move':
                    p_from, p_to = output[1]["move"]
                    self.best_move_signal.emit(p_from, p_to)
           
                elif output[0] == 'dead':
                    print(output)
                    self.checkmate_signal.emit()
                elif output[0] == 'info_move':
                    self.move_probe_signal.emit(output[1])
                    #print(output)
            else:
                time.sleep(0.1)            
                    
#-----------------------------------------------------#
class MainWindow(QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.app = app
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon('ChessQ.ico'))
       
        self.board = ChessBoard()
       
        self.createActions()
        #self.createMenus()
        self.createToolBars()
        
        self.boardView = QChessBoard(self.board)
        self.setCentralWidget(self.boardView)
        self.boardView.try_move_signal.connect(self.onTryMove)

        self.historyView = QMoveHistoryWidget(self)
        #self.engineView = QChessEngineWidget(self)

        self.endBookView = QEndBookWidget(self)
        #self.endBookView.setVisible(True)
        #self.endBookView.book_view.clicked.connect(self.onSelectGameIndex)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.historyView)
        self.addDockWidget(Qt.RightDockWidgetArea, self.endBookView)
        #self.addDockWidget(Qt.RightDockWidgetArea, self.engineView)

        self.resize(800, 700)
        self.center()
        
        self.readSettings()
        
        self.app.loadConfig()
        self.app.loadEngine()
        
        self.last_checked = False
        
        try:
            self.loadEndGameBook(self.book_file)
        except:
            pass
            
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def closeEvent(self, event):
        self.writeSettings()
    
    def onLoadEndGameBook(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog 
        fileName, _ = QFileDialog.getOpenFileName(self,"打开残局文件", "","残局文件(*.eglib);;All Files (*)", options=options)
        self.loadEndGameBook(fileName)
        
    def loadEndGameBook(self, file_name):    
        self.keeper = GameKeeper(file_name)
        self.keeper.load()
        
        games = self.keeper.all()
        
        self.endBookView.showGameBook(games)
        
        self.book_file = file_name
        self.writeSettings()
        
        self.bind_engines = [None, None, self.app.engine]
        
        self.engineThread = EngineThread(self.app.engine)  
        self.engineThread.best_move_signal.connect(self.onTryMove)
        self.engineThread.checkmate_signal.connect(self.onCheckmate)
        self.engineThread.move_probe_signal.connect(self.onMoveProbe)
        self.engineThread.start()
        
        self.onRestart()
    
    def onPrevGame(self):
        index = self.keeper.prev_game()
        self.onRestart()
    
    def onNextGame(self):
        index = self.keeper.next_game()
        self.onRestart()
    
    def onPrevNewGame(self):
        index = self.keeper.prev_new()
        self.onRestart()
    
    def onNextNewGame(self):
        index = self.keeper.next_new()
        self.onRestart()
        
    def startGameIndex(self, index):
        self.keeper.index = index
        self.onRestart()
        
    def onRestart(self):
        title, fen, best_moves = self.keeper.curr_game()
        
        self.boardView.text = title
        self.boardView.init_board(fen)
        self.endBookView.select(self.keeper.index)
        self.historyView.clear()
        
        self.best_moves = {}
        if best_moves:
            tmp_board = self.board.copy()
            for move in best_moves.split(","):
                self.best_moves[tmp_board.to_fen()] = move
                tmp_board.move_iccs(move)
                tmp_board.next_turn()
            
        self.last_moved = None
        self.move_history = []
        
        engine = self.bind_engines[self.board.move_side.value]
        if engine:
            engine.go_from(self.board.to_fen())
        
        self.boardView.update()
        
    def onEditBoard(self):

        dlg = QChessboardEditDialog(self)
        new_fen = dlg.editBoard(self.board.get_fen())
        
    def onEngineBestMove(self, move_from, move_to):
        pass
    
    def onCheckmate(self):
        msgbox = TimerMessageBox("电脑认输, 挑战成功!, 再下一城!")
        msgbox.exec_()
        self.keeper.curr_game_done()
        games = self.keeper.all()
        self.endBookView.showGameBook(games)
        self.keeper.next_new()
        self.onRestart()

    def onMoveProbe(self, info):
        print('onMoveProbe', info)
        
    def onTryMove(self, move_from, move_to):
        
        if not self.board.is_valid_move(move_from, move_to):
            self.boardView.clear_pickup()
            return False

        checked = self.board.is_checked_move(move_from, move_to)
        if checked:
            if self.last_checked:
                msg = "    必须应将!    "
            else:
                msg = "    不能送将!    "
             
            msgbox = TimerMessageBox(msg, timeout = 1)
            msgbox.exec_()
                
            return False

        self.boardView.showMove(move_from, move_to)
        
        move = self.board.move(move_from, move_to)
        #move.checked = True if check_count > 0 else False
        
        fen = move.board.to_fen()
        move_iccs = move.to_iccs()        
        
        good = False
        if (fen in self.best_moves) and (move_iccs == self.best_moves[fen]) and (self.board.move_side == ChessSide.RED): 
            good = True
        
        #engine = self.bind_engines[self.board.move_side.value]
        #if engine:
        #    engine.stop_thinking()
        
        #这一行必须有,否则引擎不能工作
        move.for_ucci(move.board.move_side.opposite(), self.move_history)
        self.move_history.append(move)
        self.historyView.newMove(move, len(self.move_history), good)
        
        if self.board.is_win():
            if self.board.move_side == ChessSide.BLACK:
                msgbox = TimerMessageBox("挑战失败, 重新再来!")
                msgbox.exec_()
                self.onRestart() 
            else:
                msgbox = TimerMessageBox("挑战成功!, 再下一城!")
                msgbox.exec_()
                self.keeper.curr_game_done()
                games = self.keeper.all()
                self.endBookView.showGameBook(games)
                self.keeper.next_new()
                self.onRestart()
            return True
        
        self.last_checked = self.board.is_checking()
        if self.last_checked:
            self.statusBar().showMessage("将军!")
        else:
            self.statusBar().showMessage('')
        
        self.board.next_turn()
        
        engine = self.bind_engines[self.board.move_side.value]
        if engine:
            fen_done = self.board.to_fen()
            if fen_done in self.best_moves:
                #time.sleep(0.5)
                engine.preset_best_move(self.best_moves[fen_done])
            else:
                #print(move)
                engine.go_from(move.to_ucci_fen())

        return True
    
    def waitMoveDone(self):
        pass
    
    def onCheckHistory(self):
        self.historyView.showGoodMoves(True)
        
    def onUndoMove(self):
        pass
    
    def onFlipBoardChanged(self, state):
        self.boardView.setFlipBoard(state)

    def onMirrorBoardChanged(self, state):
        self.boardView.setMirrorBoard(state)
    
    def onRedBoxChanged(self, state):
        self.bind_engines[ChessSide.RED] = self.app.engine if state == Qt.Checked else None
        
        self.engine_drive(ChessSide.RED)

    def onBlackBoxChanged(self, state):
        self.bind_engines[ChessSide.BLACK] = self.app.engine if state == Qt.Checked else None
            
        self.engine_drive(ChessSide.BLACK)

    def engine_drive(self, side):
        
        if self.board.move_side != side:
            return
            
        move = self.move_history[-1] if len(self.move_history) > 0 else None
        if move is not None:
            engine = self.bind_engines[side]
            if engine is not None:
                engine.go_from(move.to_ucci_fen())
                
    def onEngineInfoBoxChanged(self, state):
        self.engineView.show_profile(state == Qt.Checked)

    def about(self):
        QMessageBox.about(
            self, "关于ChessQ",
            "ChessQ 是一个象棋软件, 欢迎任何改进\n本软件采用GPL 3协议授权\n作者walker li (walker8088@gmail.com)\n"
        )

    def createActions(self):
        #self.loadBookAct = QAction(
        #    "对局打谱", self, statusTip="新对局", triggered=self.onLoadBook)

        #self.execriseGameAct = QAction(
        #    "对局练习", self, statusTip="新对局", triggered=self.onExecriseGame)

        self.loadEndGameBookAct = QAction(
            "打开残局谱", self, statusTip="杀局练习", triggered=self.onLoadEndGameBook)
        
        self.nextGameAct = QAction(
            "后一局", self, statusTip="后一局", triggered=self.onNextGame)
        
        self.prevGameAct = QAction(
            "前一局", self, statusTip="前一局", triggered=self.onPrevGame)
        
        self.nextNewGameAct = QAction(
            "后一新局", self, statusTip="后一新局", triggered=self.onNextNewGame)
        
        self.prevNewGameAct = QAction(
            "前一新局", self, statusTip="前一新局", triggered=self.onPrevNewGame)

        #self.startGameAct = QAction(u"起始局面", self,
        #        statusTip=u"开始局面", triggered=self.onStartGame)

        #self.editBoardAct = QAction(
        #    "局面修改", self, statusTip="编辑局面", triggered=self.onEditBoard)

        self.checkHistoryAct = QAction(
            "历史提示", self, statusTip="历史提示", triggered=self.onCheckHistory)
        self.undoMoveAct = QAction(
            "悔棋", self, statusTip="悔棋", triggered=self.onUndoMove)
        
        self.restartAct = QAction(
            "重新开始", self, statusTip="重新开始", triggered=self.onRestart)
 
        #self.stopGameAct = QAction(u"结束", self,
        #        statusTip=u"结束对局", triggered=self.onStopGame)

        self.exitAct = QAction(
            "结束退出",
            self,
            shortcut="Ctrl+Q",
            statusTip="Exit the application",
            triggered=qApp.closeAllWindows)

        self.aboutAct = QAction(
            "&About",
            self,
            statusTip="Show the application's About box",
            triggered=self.about)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addSeparator()
        #self.fileMenu.addAction(self.closeAct)
        self.fileMenu.addAction(self.exitAct)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)

    def createToolBars(self):

        #self.boardToolbar = self.addToolBar("Board")
        #self.boardToolbar.addAction(self.loadBookAct)
        #self.boardToolbar.addAction(self.execriseGameAct)
        #self.boardToolbar.addAction(self.checkingGameAct)
        #self.boardToolbar.addAction(self.editBoardAct)

        self.flipBoardBox = QCheckBox("上下反转")
        self.flipBoardBox.stateChanged.connect(self.onFlipBoardChanged)
        
        self.mirrorBoardBox = QCheckBox("水平镜像")
        self.mirrorBoardBox.stateChanged.connect(self.onMirrorBoardChanged)

        self.gameToolbar = self.addToolBar("Game")
        self.gameToolbar.addAction(self.loadEndGameBookAct)
        self.gameToolbar.addAction(self.prevGameAct)
        self.gameToolbar.addAction(self.nextGameAct)
        self.gameToolbar.addAction(self.prevNewGameAct)
        self.gameToolbar.addAction(self.nextNewGameAct)
        
        self.gameToolbar.addAction(self.checkHistoryAct)
        self.gameToolbar.addAction(self.undoMoveAct)
        self.gameToolbar.addAction(self.restartAct)
        
        self.showToolbar = self.addToolBar("Show")
        self.showToolbar.addWidget(self.flipBoardBox)
        self.showToolbar.addWidget(self.mirrorBoardBox)

        self.engineToolbar = self.addToolBar("Engine")
        #self.engineToolbar.addAction(self.loadEngineAct)
        
        self.eRedBox = QCheckBox("引擎执红")
        self.eRedBox.setChecked(False)
        self.eRedBox.stateChanged.connect(self.onRedBoxChanged)

        self.eBlackBox = QCheckBox("引擎执黑")
        self.eBlackBox.setChecked(True)
        self.eBlackBox.stateChanged.connect(self.onBlackBoxChanged)

        self.engineInfoBox = QCheckBox("引擎分析")
        #self.engineInfoBox.setChecked(True);
        self.engineInfoBox.stateChanged.connect(self.onEngineInfoBoxChanged)

        self.engineToolbar.addWidget(self.eRedBox)
        self.engineToolbar.addWidget(self.eBlackBox)
        self.engineToolbar.addWidget(self.engineInfoBox)

        self.sysToolbar = self.addToolBar("System")
        self.sysToolbar.addAction(self.exitAct)
    
        self.statusBar().showMessage("Ready")

    
    def readSettings(self):

        settings = QSettings('WalkerLee', 'ChessQ')

        pos = settings.value('pos', QPoint(200, 50))
        size = settings.value('size', QSize(600, 600))
        self.book_file = settings.value('last_book_file', os.path.join('gamebooks','适情雅趣360.eglib'))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):

        settings = QSettings('WalkerLee', 'ChessQ')

        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())
        settings.setValue('last_book_file', self.book_file) 
    
#-----------------------------------------------------#
    
  