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
from .QChessBoardEditDlg import *

#-----------------------------------------------------#

BOOK, EXERCISE, KILLING = list(range(3))

APP_NAME = "ChessQ 中国象棋"
APP_CONFIG_FILE = "ChessQ.cfg"

#-----------------------------------------------------#
'''
class EngineThread(QThread):
    def __init__(self, parent, engine, engine_id):
        super().__init__(self)
        
        self.engine = engine
        self.engine_id = engine_id
        
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
                    self.parent.on_best_move(self.engine_id, p_from, p_to)
                #被将死不能从引擎发出, 因为引擎探测深度太深
                #elif output[0] == 'dead':
                #    print(output)
                #    self.checkmate_signal.emit(self.engined_id)
                elif output[0] == 'info_move':
                    self.parent.on_move_probe(self.engine_id, output[1])
                    #print(output)
            else:
                time.sleep(0.1)            
'''
                    
#-----------------------------------------------------#
class EngineManager(QObject):
    best_move_signal = pyqtSignal(int, tuple, tuple)
    move_probe_signal = pyqtSignal(int, dict)
    
    def __init__(self, parent):
        super(QObject, self).__init__()
        
        self.parent = parent
        self.engines = []
        self.engine_fens = []
        
        self.stoped = True
        
    def load_engine_from_config(self, config):
        engine = UcciEngine(config["ucci_engine"]["name"])
        if engine.load(config["ucci_engine"]["path"]):
            self.engines.append(engine)
        else:
            QMessageBox.warning(None, APP_NAME, f'引擎加载失败：{config["ucci_engine"]["path"]}')
    
    def go_from(self, engine_id, fen):
        if (engine_id < 0) or (engine_id >= len(self.engines)):
            return False
        self.engines[engine_id].go_from(fen)
        
    def start(self):
        self.thread = ThreadRunner(self)
        self.thread.start()
        
    def stop(self):    
        self.stoped = True
        
    def run(self):
        self.stoped = False 
        while not self.stoped:
            self.run_once()
            time.sleep(0.1)
            
    def run_once(self):
        for engine_id, engine in enumerate(self.engines): 
            engine.handle_msg_once()
            while not engine.move_queue.empty():
                output = engine.move_queue.get()
                action = output['action']
                if action == 'best_move':
                    p_from, p_to = output["move"]
                    self.best_move_signal.emit(engine_id, p_from, p_to)
                #被将死不能从引擎发出, 因为引擎探测深度太深
                #elif output[0] == 'dead':
                #    print(output)
                #    self.checkmate_signal.emit(self.engined_id)
                elif action == 'info_move':
                    self.move_probe_signal.emit(engine_id, output)
                    #print(output)
#-----------------------------------------------------#
class GameManager(QObject):
    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
    
    def init_ui(self):
        pass
        
    def free_ui(self):
        pass
    
    def on_new(self):
        pass
    
    def onRestart(self):
        
        self.parent.boardView.text = ''
          
        self.parent.last_move = None
        self.parent.move_history = []
        
        self.parent.historyView.clear()
        self.parent.engineView.clear()
        
        self.parent.boardView.update()
        
    def on_move(self, move):
        self.parent.board.next_turn()
        self.parent.engineView.clear()
        self.parent.idle_engine_working()
        
    def on_win(self, side):
        pass
        
#-----------------------------------------------------#
class EndBookManager(GameManager):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.loadEndBookAct = QAction(
            "加载杀局库", self.parent, statusTip="加载杀局库", triggered=self.onLoadEndBook)
        
        self.nextGameAct = QAction(
            "后一局", self.parent, statusTip="后一局", triggered=self.onNextGame)
        
        self.prevGameAct = QAction(
            "前一局", self.parent, statusTip="前一局", triggered=self.onPrevGame)
        
        self.nextNewGameAct = QAction(
            "后一新局", self.parent, statusTip="后一新局", triggered=self.onNextNewGame)
        
        self.prevNewGameAct = QAction(
            "前一新局", self.parent, statusTip="前一新局", triggered=self.onPrevNewGame)
        
        self.gameToolbar = self.parent.addToolBar("Game")
        self.gameToolbar.hide()
        self.gameToolbar.addAction(self.loadEndBookAct)
        self.gameToolbar.addAction(self.prevGameAct)
        self.gameToolbar.addAction(self.nextGameAct)
        self.gameToolbar.addAction(self.prevNewGameAct)
        self.gameToolbar.addAction(self.nextNewGameAct)
        
        #self.gameToolbar.addAction(self.checkHistoryAct)
        self.parent.endBookView.book_select_signal.connect(self.startGameIndex)
        
        try:
            self.loadEndBook(self.parent.book_file)
        except:
            pass
        
    def init_ui(self):
        self.gameToolbar.show()
        self.parent.endBookView.show()
        self.parent.boardView.init_board('')
        
    def free_ui(self):
        self.gameToolbar.hide()
        self.parent.endBookView.hide()
        
    def on_new(self):
        self.onRestart()
    
    def on_win(self, win_side):
        if win_side == ChessSide.BLACK:
            msgbox = TimerMessageBox("挑战失败, 重新再来!")
            msgbox.exec_()
            self.onRestart() 
        else:
            self.parent.eRedBox.setChecked(False)
            msgbox = TimerMessageBox("挑战成功!, 再下一城!")
            msgbox.exec_()
            self.keeper.curr_game_done()
            
            games = self.keeper.all()
            self.parent.endBookView.showGameBook(games)
            
            self.keeper.next_new()
            self.onRestart()
           
    def onLoadEndBook(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog 
        fileName, _ = QFileDialog.getOpenFileName(self.parent, "打开残局文件", "","残局文件(*.eglib);;All Files (*)", options=options)
        if fileName:
            self.loadEndBook(fileName)
        
    def loadEndBook(self, file_name):
    
        self.keeper = GameKeeper(file_name)
        self.keeper.load()
        
        games = self.keeper.all()
        
        index = self.keeper.next_new()
        
        self.parent.endBookView.showGameBook(games)
        self.parent.book_file = file_name
        self.parent.writeSettings()
       
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
        super().onRestart()

        title, fen, best_moves = self.keeper.curr_game()
        
        self.parent.boardView.text = title
        self.parent.boardView.init_board(fen)
        self.parent.endBookView.select(self.keeper.index)
        
        '''
        self.best_moves = {}
        if best_moves:
            tmp_board = self.board.copy()
            for move in best_moves.split(","):
                self.best_moves[tmp_board.to_fen()] = move
                tmp_board.move_iccs(move)
                tmp_board.next_turn()
        '''    
        self.parent.last_move = None
        self.parent.move_history = []
        self.parent.idle_engine_working()
        self.parent.boardView.update()
        
#-----------------------------------------------------#
class FreeGameManager(GameManager):
    def __init__(self, parent):
        super().__init__(parent)
        
    def on_new(self):
        self.onRestart()
        
    def onRestart(self):
        super().onRestart()
        self.parent.boardView.init_board(FULL_INIT_FEN)
        
        self.parent.idle_engine_working()
        
        
    def on_win(self, side):
        pass
    
#-----------------------------------------------------#
class MainWindow(QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.app = app
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon('ChessQ.ico'))
       
        self.board = ChessBoard()
        self.game_manager = None
        
        self.createActions()
        self.createMenus()
        self.createToolBars()
        
        self.boardView = QChessBoard(self.board)
        self.setCentralWidget(self.boardView)
        self.boardView.try_move_signal.connect(self.onTryMove)
        
        self.historyView = QMoveHistoryWidget(self)
        self.historyView.move_select_signal.connect(self.onSelectHistoryMove)
        self.engineView = QChessEngineWidget(self)

        self.endBookView = QEndBookWidget(self)
        #self.endBookView.setVisible(True)
        #self.endBookView.book_view.clicked.connect(self.onSelectGameIndex)

        self.addDockWidget(Qt.RightDockWidgetArea, self.historyView)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.endBookView)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.engineView)

        self.resize(800, 700)
        self.center()
        
        self.readSettings()
        
        self.app.loadConfig()
        
        self.engine_manager = EngineManager(self)
        self.engine_manager.load_engine_from_config(self.app.config)
        
        self.engine_manager.best_move_signal.connect(self.onEngineBestMove)
        self.engine_manager.move_probe_signal.connect(self.onEngineMoveProbe)
        
        self.engine_working = False
        self.last_move = None
        
        self.bind_engines = [None, None, 0]
        
        self.engine_manager.start()
        
        self.game_managers = {
            'free_game': FreeGameManager(self),
            'end_book': EndBookManager(self),
        }
        
        self.onDoEndBook()
        
        #self.move_history = []
        
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def closeEvent(self, event):
        self.writeSettings()
    
    def onDoFreeGame(self):

        if self.game_manager:
            if self.game_manager == self.game_managers['free_game']: 
                return
            else:    
                self.game_manager.free_ui()
        
        self.game_manager = self.game_managers['free_game']
        self.game_manager.init_ui()
        self.game_manager.on_new()
         
    def onDoOpenBook(self):
        pass
    
    def onDoEndBook(self):

        if self.game_manager:
            if self.game_manager == self.game_managers['end_book']: 
                return
            else:    
                self.game_manager.free_ui()

        self.game_manager = self.game_managers['end_book']
        self.game_manager.init_ui()
        self.game_manager.on_new()
        
    def onRestartGame(self):
        self.game_manager.onRestart()
        
    def onEditBoard(self):
        dlg = QChessboardEditDialog(self)
        new_fen = dlg.editBoard(self.board.to_fen())
            
    def idle_engine_working(self):
        working = False
        if self.engine_working:
            working = True
        elif self.bind_engines[ChessSide.RED] is not None:
            working = True
        elif self.bind_engines[ChessSide.BLACK] is not None:
            working = True    
        if working:    
            if self.last_move:
                self.engine_manager.go_from(0, self.last_move.to_ucci_fen())
            else:
                self.engine_manager.go_from(0, self.board.to_fen())
                
    def onSelectHistoryMove(self, move, is_last):
        self.boardView.set_view_only(not is_last)
        self.boardView.init_board(move.board.to_fen())
        self.boardView.show_move(move.p_from, move.p_to)
        self.boardView.init_board(move.board_done.to_fen())
        
    def onEngineMoveProbe(self, engine_id, info):
        if not self.engine_working:
            return
            
        fen = self.board.to_fen()
        self.engineView.on_engine_move_info(fen, info)
    
    def onEngineBestMove(self, engine_id, move_from, move_to):
        #print("onEngineBestMove", engine_id, move_from, move_to)
        
        if not self.board.is_valid_move(move_from, move_to):
            print(f'error move: {move_from} {move_to}')
            return False

        piece = self.board.get_piece(move_from)
        if self.bind_engines[piece.side.value] == engine_id: 
            self.onTryMove(move_from, move_to)
        
    def onTryMove(self, move_from, move_to):
    
        self.boardView.show_move(move_from, move_to)
        move = self.board.move(move_from, move_to)
        
        fen = move.board.to_fen()
        move_iccs = move.to_iccs()        
        
        good = False
        #if (fen in self.best_moves) and (move_iccs == self.best_moves[fen]) and (self.board.move_side == ChessSide.RED): 
        #    good = True
        
        #这一行必须有,否则引擎不能工作
        move.for_ucci(move.board.move_side.opposite(), self.move_history)
        
        self.move_history.append(move)
        self.historyView.newMove(move, len(self.move_history), good)
        self.last_move = move

        if self.board.is_checking():
            self.statusBar().showMessage("将军!")
        else:
            self.statusBar().showMessage('')
        
        if self.board.is_win():
            self.game_manager.on_win(self.board.move_side)
        else:
            self.game_manager.on_move(move)
            
        return True
    
    def onCheckHistory(self):
        self.historyView.showGoodMoves(True)
        
    def onUndoMove(self):
        pass
    
    def onFlipBoardChanged(self, state):
        self.boardView.setFlipBoard(state)

    def onMirrorBoardChanged(self, state):
        self.boardView.setMirrorBoard(state)
    
    def onRedBoxChanged(self, state):
        self.__check_state(state == Qt.Checked, ChessSide.RED)
        
    def onBlackBoxChanged(self, state):
        self.__check_state(state == Qt.Checked, ChessSide.BLACK)
        
    def __check_state(self, yes, move_side):    
        self.bind_engines[move_side] = 0 if yes else None
        self.idle_engine_working()
        #engine_id = self.bind_engines[move_side]
        #if (engine_id is None) or (self.board.move_side.value != move_side):
        #    return 
        
    def onEngineInfoBoxChanged(self, state):
        self.engine_working = (state == Qt.Checked)
        if self.engine_working is True:
            self.engineView.clear()
        self.idle_engine_working()
        
    def about(self):
        QMessageBox.about(
            self, "关于ChessQ",
            "ChessQ 是一个象棋软件, 欢迎任何改进\n本软件采用GPL 3协议授权\n作者walker li (walker8088@gmail.com)\n"
        )

    def createActions(self):
        
        self.doFreeGameAct = QAction(
            "自由练习", self, statusTip="练习", triggered=self.onDoFreeGame)

        self.doOpenBookAct = QAction(
            "对局打谱", self, statusTip="打谱", triggered=self.onDoOpenBook)
        
        self.doEndBookAct = QAction(
            "杀局练习", self, statusTip="杀局练习", triggered=self.onDoEndBook)
        
        
        self.restartAct = QAction(
            "重新开始", self, statusTip="重新开始", triggered=self.onRestartGame)
        
        self.editBoardAct = QAction(
            "局面修改", self, statusTip="编辑局面", triggered=self.onEditBoard)
        
        '''
        self.checkHistoryAct = QAction(
            "历史提示", self, statusTip="历史提示", triggered=self.onCheckHistory)
        '''
        
        self.undoMoveAct = QAction(
            "悔棋", self, statusTip="悔棋", triggered=self.onUndoMove)
        
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

        self.gameToolbar = self.addToolBar("Board")
        self.gameToolbar.addAction(self.doFreeGameAct)
        self.gameToolbar.addAction(self.doOpenBookAct)
        self.gameToolbar.addAction(self.doEndBookAct)
        
        #self.boardToolbar = self.addToolBar("Board")
        
        self.flipBoardBox = QCheckBox("上下反转")
        self.flipBoardBox.stateChanged.connect(self.onFlipBoardChanged)
        
        self.mirrorBoardBox = QCheckBox("水平镜像")
        self.mirrorBoardBox.stateChanged.connect(self.onMirrorBoardChanged)
        
        self.showToolbar = self.addToolBar("Show")
        self.showToolbar.addAction(self.restartAct)
        self.showToolbar.addAction(self.undoMoveAct)
        self.showToolbar.addAction(self.editBoardAct)
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
    
  