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

import time
import yaml

from pubsub import pub

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QVariant', 2)

from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui  import *

from cchess import *

from QChessboard import *
from QChessWidgets import *

from QChessboardEditDlg import *

#-----------------------------------------------------#    

BOOK, EXERCISE, KILLING = range(3)

APP_NAME = u"ChessQ 中国象棋"
APP_CONFIG_FILE = "ChessQ.cfg"
#-----------------------------------------------------#       

class MainWindow(QMainWindow):
    
    def __init__(self, app):
        super(MainWindow, self).__init__()
        
        self.setAttribute(Qt.WA_DeleteOnClose)
        
        self.app = app
        self.setWindowTitle(APP_NAME)
        
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createMainWidgets()
        
        with open(APP_CONFIG_FILE) as f:
            try :
                self.config = yaml.load(f)
            except Exception as e:
                QMessageBox.warning(self, APP_NAME, APP_CONFIG_FILE + u" 配置文件错误：" + str(e))
                self.config = None
                return 

        self.table = ChessTable(self, self.board)
        
        #self.players = [ UiChessPlayer(self.table), 
        #                 UiChessPlayer(self.table)
        #                 ]
        #self.table.set_players(self.players)
        
        self.engine = [None, None]
        self.engine_taken = [False , True]
        self.last_engine_best_move = None
        
        self.loadEngine()
            
        self.timer = QTimer()
        self.timer.start(50)
        self.timer.timeout.connect(self.onIdleRun)
        
        self.resize(800, 700)
         
        self.center()
        #self.showMaximized()
        
        self.readSettings()
        
        self.mode = EXERCISE 
        
        self.final_book = FinalBook()
        #self.final_book.load_from_qcd(".\chessbooks\\final_book.qcd")
        self.final_book.load_from_qcb(".\chessbooks\\shi_qing_ya_qu.qcb")
        self.finalbookView.show_book(self.final_book)
        
        pub.subscribe(self.on_game_inited, "game_inited")
        pub.subscribe(self.on_game_started, "game_started")
        pub.subscribe(self.on_game_reshow, "game_reshow")
        pub.subscribe(self.on_game_step_moved, "game_step_moved")
        pub.subscribe(self.on_game_step_moved_undo, "game_step_moved_undo")
        pub.subscribe(self.on_engine_best_move, "engine_best_move")
        pub.subscribe(self.on_side_dead, "side_dead")
        
        self.onExecriseGame()
   
    def loadEngine(self):
        
        primary_engine = self.config["ucci_engine"]["primary"] 
        engine = UcciEngine(primary_engine["name"])
        if engine.load(primary_engine["path"]) :
            self.engine[0] = engine 
            self.is_engine_profile = True
        else:
            QMessageBox.warning(self, APP_NAME, u"主引擎加载失败：" + primary_engine["path"])
            self.engine[0] = None
        
        scondary_engine = self.config["ucci_engine"]["scondary"] 
        
        if scondary_engine["load"] :            
            engine = UcciEngine(scondary_engine["name"])
            if engine.load(scondary_engine["path"]) :
                self.engine[1] = engine 
            else:
                QMessageBox.warning(self, APP_NAME, u"副引擎加载失败：" + scondary_engine["path"])
                self.engine[1] = None
        
        self.engine_taken[RED] = True if self.eRedBox.isChecked() else False 
        self.engine_taken[BLACK] = True if self.eBlackBox.isChecked() else False 
        self.engineView.show_profile(True)
         
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)    
    
    def onIdleRun(self):
        
        #if self.table.running:
        #    self.table.handle_player_msg()
        
        if self.engine[0] :
                self.engine[0].handle_msg_once()
                #self.engineView.handle_engine_msg(self.engine[0])
        
    def closeEvent(self, event):
        self.timer.stop()
        
        if self.engine[0] :
            self.engine[0].quit()
            self.engine[0] = None
        
        if self.engine[1] :
            self.engine[1].quit()
            self.engine[1] = None
            
        self.writeSettings()
      
    def onLoadBook(self):
        
        file_name = QtGui.QFileDialog.getOpenFileName(self, u"打开棋谱文件", '')
        
        if file_name :
                self.book = load_book(file_name)      
                if self.book  :
                        self.bookView.show_book(self.book)
                self.mode = BOOK
                
    def onExecriseGame(self):
        
        self.engineView.setVisible(True)
        self.finalbookView.setVisible(False)

        self.mode = EXERCISE
        
        self.table.new_game(DEFAULT_INIT_FEN)
        self.table.start_game()
        
    def onCheckingGame(self) :
    
        #self.engineView.setVisible(False)
        self.finalbookView.setVisible(True)
        
        self.start_final_book( self.final_book.index )
        
    def onEditBoard(self):
        
        dlg = QChessboardEditDialog(self)
        
        new_fen = dlg.editBoard(self.board.get_fen())
        
        self.table.new_game(new_fen)
        self.table.start_game()
        
    def start_final_book(self, book_index) :
        
        self.final_book.index = book_index
        self.curr_book = self.final_book.curr_book()
        self.setWindowTitle(APP_NAME + "  --  " + self.curr_book.name)
        self.bookView.clear()
        self.finalbookView.book_view.selectRow(book_index)
        
        self.mode = KILLING

        self.table.new_game( self.curr_book.fen)
        self.table.start_game()
        
    def onUndoMove(self) :
        self.table.undo_move() 
        
    def on_game_inited(self, move_log) :
        self.bookView.step_view.clear()
        self.bookView.append_move(move_log)
        self.engineView.step_view.clear()
        self.last_engine_best_move = None 
        
    def on_game_started(self, move_side) :
        self.engineView.step_view.clear()
        self.reshow_mode = False
        
    def on_game_reshow(self, move_log) :
        self.engineView.step_view.clear()
        self.board.init_board(move_log.fen_after_move)
        if move_log.step_no != (len(self.table.history) -1) :
            self.reshow_mode = True
        else :
            self.reshow_mode = False
            
    def on_game_step_moved(self, move_log) :
        
        self.bookView.append_move(move_log)
        self.engineView.step_view.clear()
        
        self.last_engine_best_move = None 
        
        #if self.engine[0] and self.is_engine_profile :
            #fen_for_engine =
            #self.engine[0].go_from(move_log.fen_for_engine())
    
    def on_game_step_moved_undo(self, steps, move_log, next_move_side) :
        self.bookView.undo_move(steps)
        
    def on_engine_best_move(self, from_engine, from_pos, to_pos) :
        
        if self.reshow_mode :
            return 
            
        chess_man = self.table.board.at_pos(*from_pos)
        if not chess_man or  chess_man.color != self.table.board.move_side:
            return 
        
        self.last_engine_best_move = ( from_pos, to_pos)
        
        if  self.engine_taken[self.board.move_side] :
            self.table.on_side_move_request(from_pos, to_pos)    
    
    def on_side_dead(self,  dead_side) :
        
        self.table.stop_game()
        
        if self.mode == KILLING :        
            if dead_side == BLACK:
                result = u"棋局结束，黑方被将死。挑战成功，继续挑战！"
                self.curr_book.done = True
                self.final_book.index += 1    
            else:
                result = u"棋局结束，红方被将死。再接再励！"
            
            QMessageBox.warning(self,  APP_NAME, result)
            
            self.start_final_book( self.final_book.index)
             
        elif self.mode == EXERCISE :
           result = u"棋局结束，黑方被将死。" if dead_side == BLACK else  u"棋局结束，红方被将死。"
           QMessageBox.warning(self,  APP_NAME, result)
             
    def onFlipBoardChanged(self, state):
        
        self.board.setFlipBoard(state)
    
    def onRedBoxChanged(self, state):
        
        self.engine_taken[RED] = True if state == Qt.Checked else False
        self.__handle_last_best_move(RED)
        
    def onBlackBoxChanged(self, state):
        
        self.engine_taken[BLACK] = True if state == Qt.Checked else False 
        self.__handle_last_best_move(BLACK)
    
    def __handle_last_best_move(self, move_side) :
    
        if not self.last_engine_best_move :
            return 
       
        from_pos, to_pos = self.last_engine_best_move
       
        if  self.engine_taken[move_side] :
            self.table.on_side_move_request(from_pos, to_pos)  
        
        self.last_engine_best_move =  None
        
       
    def onEngineInfoBoxChanged(self, state):
         self.engineView.show_profile(state == Qt.Checked)
         
    def about(self):
        QMessageBox.about(self, u"关于ChessQ",
                u"ChessQ 是一个象棋软, 目标是做一个跨平台版本的象棋巫师，欢迎任何改进\n本软件采用GPL 3协议授权\n作者walker li (walker8088@gmail.com)\n"
                )
        
    def createActions(self):
        self.loadBookAct = QAction(u"棋谱管理", self, 
                statusTip=u"新对局", triggered=self.onLoadBook)
        
        self.execriseGameAct = QAction(u"对局练习", self, 
                statusTip=u"新对局", triggered=self.onExecriseGame)
        
        self.checkingGameAct = QAction(u"杀局练习", self, 
                statusTip=u"杀局练习", triggered=self.onCheckingGame)
        
        #self.startGameAct = QAction(u"起始局面", self, 
        #        statusTip=u"开始局面", triggered=self.onStartGame)
        
        self.editBoardAct = QAction(u"局面修改", self, 
                statusTip=u"编辑局面", triggered=self.onEditBoard)
        
        self.undoMoveAct = QAction(u"悔棋", self, 
                statusTip=u"悔棋", triggered=self.onUndoMove)
        
        #self.stopGameAct = QAction(u"结束", self, 
        #        statusTip=u"结束对局", triggered=self.onStopGame)
        
        self.exitAct = QAction(u"结束退出", self, shortcut="Ctrl+Q",
                statusTip="Exit the application",
                triggered=qApp.closeAllWindows)

        self.aboutAct = QAction("&About", self,
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
        
        self.boardToolbar = self.addToolBar("Board")
        self.boardToolbar.addAction(self.loadBookAct)
        self.boardToolbar.addAction(self.execriseGameAct)
        self.boardToolbar.addAction(self.checkingGameAct)
        self.boardToolbar.addAction(self.editBoardAct) 
               
        self.flipBoardBox = QCheckBox(u"反转棋盘")
        self.flipBoardBox.stateChanged.connect(self.onFlipBoardChanged)
        
        self.gameToolbar = self.addToolBar("Game")
        self.gameToolbar.addWidget(self.flipBoardBox)
       
        #self.gameToolbar.addAction(self.startGameAct)
        self.gameToolbar.addAction(self.undoMoveAct)
        #self.gameToolbar.addAction(self.stopGameAct)
        
        self.engineToolbar = self.addToolBar("Engine")
        #self.engineToolbar.addAction(self.loadEngineAct)
        
        self.eRedBox = QCheckBox(u"引擎执红")
        self.eRedBox.setChecked(False);
        self.eRedBox.stateChanged.connect(self.onRedBoxChanged)
        
        self.eBlackBox = QCheckBox(u"引擎执黑")
        self.eBlackBox.setChecked(True);
        self.eBlackBox.stateChanged.connect(self.onBlackBoxChanged)
        
        self.engineInfoBox = QCheckBox(u"引擎分析")
        self.engineInfoBox.setChecked(True);
        self.engineInfoBox.stateChanged.connect(self.onEngineInfoBoxChanged)
         
        self.engineToolbar.addWidget(self.eRedBox)
        self.engineToolbar.addWidget(self.eBlackBox)
        self.engineToolbar.addWidget(self.engineInfoBox)
        
        self.engineToolbar.addAction(self.exitAct)

    def createMainWidgets(self):
        
        self.board = QChessboard()
        
        self.setCentralWidget(self.board)
      
        self.bookView = QChessBookWidget(self)
        self.engineView = QChessEngineWidget(self)
        
        self.finalbookView = QFinalBookWidget(self)
        self.finalbookView.setVisible(False)
        
        self.addDockWidget(Qt.LeftDockWidgetArea, self.bookView)
        self.addDockWidget(Qt.RightDockWidgetArea, self.finalbookView)
        self.addDockWidget(Qt.RightDockWidgetArea, self.engineView)
        
        self.bookView.raise_()
        
    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def readSettings(self):
        
        settings = QSettings('ChessQ', 'pos_rem')
        
        pos = settings.value('pos', QPoint(200, 50))
        size = settings.value('size', QSize(600, 600))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        
        settings = QSettings('ChessQ', 'pos_rem')
        
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())
    
#-----------------------------------------------------#

class QChessApplication(QApplication):
        
        def __init__(self) :
                super(QApplication,self).__init__([])
                
                self.mainWin = MainWindow(self)
                self.mainWin.show()
                      
#-----------------------------------------------------#
