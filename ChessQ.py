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

APP_NAME = u"ChessQ 中国象棋"

#-----------------------------------------------------#       

class MainWindow(QMainWindow):
    
    def __init__(self, app):
        super(MainWindow, self).__init__()
        
        self.setAttribute(Qt.WA_DeleteOnClose)
        
        self.app = app
        self.setWindowTitle(APP_NAME)
        
        self.createActions()
        #self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createMainWidgets()
        
        self.engine_path = "engines/eleeye/eleeye"
        #self.engine_path = "engines/bitstronger/bitstronger"
        #self.engine_path = "engines/harmless/harmless"
        
        self.engine = UcciEngine(self.engine_path)
        if not self.engine.load():
            QMessageBox.warning(self, APP_NAME, u"引擎加载失败.")
            self.engine = None
            
        #self.finalbook = FinalBook(u"epds/橘中秘_残局.EPD")
        #self.finalbook = FinalBook(u"challengers/基本杀法.EPD")
        
        self.table = ChessTable(self, self.board)
        
        self.players = [ UiChessPlayer(self.table), 
                         UiChessPlayer(self.table)
                         ]
    
        self.table.set_players(self.players)
        
        if self.eRedBox.isChecked(): 
            self.players[RED].bind_engine(self.engine)
        
        if self.eBlackBox.isChecked(): 
            self.players[BLACK].bind_engine(self.engine)
        
        self.timer = QTimer()
        self.timer.start(50)
        self.timer.timeout.connect(self.onIdleRun)
        
        self.resize(800, 700)
         
        self.center()
        #self.showMaximized()
        
        self.readSettings()
        
        self.onInitBoard()
        
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)    
    
    def onIdleRun(self):
        if self.table.running:
            self.table.handle_player_msg()
        
    def closeEvent(self, event):
        self.timer.stop()
        
        if self.engine :
            self.engine.quit()
            self.engine = None
            
        if self.table.running :
            self.table.stop_game()
        
        self.writeSettings()
      
    def onLoadBook(self):
        self.book = ChessBook()
        self.book.load_from_cbf_file("2.cbf")
        self.bookView.show_book(self.book)
        
    def onInitBoard(self):
        self.board.init_board()
        
    def onEditBoard(self):
        
        dlg = QChessboardEditDialog(self)
        new_fen = dlg.editBoard(self.board.get_fen())
        
        self.board.init_board(new_fen)
        
    def onSelectBoard(self):
        pass
        
    def onStartGame(self):
        self.table.start_game()
    
    def onUndoMove(self) :
        self.table.undo_move()
        self.bookView.undo_move()
    
    def onStopGame(self) :
        self.table.stop_game()
        
    def onLoadEngine(self):
        
        if self.eRedBox.isChecked(): 
            self.players[RED].bind_engine(self.engine)
        
        if self.eBlackBox.isChecked(): 
            self.players[BLACK].bind_engine(self.engine)
                
    def onFinalChallenge(self) :
    
        curr_book = self.finalbook.curr_book()
        
        self.setWindowTitle(APP_NAME + curr_book[0])
        self.bookView.clear()
        
        self.table.new_game((player1, player2), curr_book[1])
        self.table.start_game()
        
    def notify_move_from_table(self, move_step) :
        self.bookView.append_move(move_step)
       
    def notify_unmove_from_table(self, move_step) :
        pass
        
    
    def onFlipBoardChanged(self, state):
        
        self.board.setFlipBoard(state)
        
    def onRedBoxChanged(self, state):
        
        if state == Qt.Checked:
            self.table.players[RED].bind_engine(self.engine)
        else :
            self.table.players[RED].bind_engine(None)
            
    def onBlackBoxChanged(self, state):
            
        if state == Qt.Checked :
            self.table.players[BLACK].bind_engine(self.engine)
        else :
            self.table.players[BLACK].bind_engine(None)
        
    def onInfoBoxChanged(self, state):
        pass
        

    def about(self):
        QMessageBox.about(self, u"关于ChessQ",
                ""
                "")
        
    def on_game_over(self, over_side):
        
        self.table.stop_game()
        
        if over_side == BLACK:
            result = u"棋局结束，黑方被将死！"
            #self.finalbook.next_book()
            #print u"挑战成功", self.finalbook.index
        else:
            result = u"棋局结束，红方被将死！"
        
        QMessageBox.warning(self,  APP_NAME, result)
            
            #QMessageBox.warning(self,  APP_NAME, u"挑战失败!")
            #self.finalbook.next_book()
            
            #print u"挑战失败", self.finalbook.index
            
        #self.onFinalChallenge()
        
    def createActions(self):
        self.loadBookAct = QAction(u"加载棋谱", self, 
                statusTip=u"新对局", triggered=self.onLoadBook)
        
        self.initBoardAct = QAction(u"初始盘面", self, 
                statusTip=u"新对局", triggered=self.onInitBoard)
        
        self.editBoardAct = QAction(u"编辑盘面", self, 
                statusTip=u"局面编辑", triggered=self.onEditBoard)
        
        self.selectBoardAct = QAction(u"残局选择", self, 
                statusTip=u"残局选择", triggered=self.onSelectBoard)
        
        self.startGameAct = QAction(u"开始", self, 
                statusTip=u"开始对局", triggered=self.onStartGame)
        
        self.undoMoveAct = QAction(u"悔棋", self, 
                statusTip=u"悔棋", triggered=self.onUndoMove)
        
        self.stopGameAct = QAction(u"结束", self, 
                statusTip=u"结束对局", triggered=self.onStopGame)
        
        self.loadEngineAct = QAction(u"加载引擎", self, 
                statusTip=u"加载象棋引擎", triggered=self.onLoadEngine)
        
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
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
        self.boardToolbar.addAction(self.initBoardAct)
        self.boardToolbar.addAction(self.editBoardAct) 
        self.boardToolbar.addAction(self.selectBoardAct)
        
        self.flipBoardBox = QCheckBox(u"反转棋盘")
        self.flipBoardBox.stateChanged.connect(self.onFlipBoardChanged)
        
        self.boardToolbar.addWidget(self.flipBoardBox)
        
        self.gameToolbar = self.addToolBar("Game")
        self.gameToolbar.addAction(self.startGameAct)
        self.gameToolbar.addAction(self.undoMoveAct)
        self.gameToolbar.addAction(self.stopGameAct)
        
        self.engineToolbar = self.addToolBar("Engine")
        self.engineToolbar.addAction(self.loadEngineAct)
        
        self.eRedBox = QCheckBox(u"引擎执红")
        self.eRedBox.setChecked(False);
        self.eRedBox.stateChanged.connect(self.onRedBoxChanged)
        
        self.eBlackBox = QCheckBox(u"引擎执黑")
        self.eBlackBox.setChecked(True);
        self.eBlackBox.stateChanged.connect(self.onBlackBoxChanged)
        
        self.eInfoBox = QCheckBox(u"引擎分析")
        self.eInfoBox.setChecked(True);
        self.eInfoBox.stateChanged.connect(self.onInfoBoxChanged)
         
        self.engineToolbar.addWidget(self.eRedBox)
        self.engineToolbar.addWidget(self.eBlackBox)
        self.engineToolbar.addWidget(self.eInfoBox)
        
        #self.engineToolbar.addAction() 
        #self.engineToolbar.addAction()

        #self.toolbar.addAction(self.exitAct)

    def createMainWidgets(self):
        
        self.board = QChessboard()
        
        self.setCentralWidget(self.board)
      
        self.bookView = QChessBookWidget(self)
        self.engineView = QChessEngineWidget(self)
        
        self.addDockWidget(Qt.RightDockWidgetArea, self.bookView)
        self.addDockWidget(Qt.RightDockWidgetArea, self.engineView)
        self.tabifyDockWidget(self.bookView, self.engineView);
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

class CChessApplication(QApplication):
        
        def __init__(self) :
                super(QApplication,self).__init__([])
                
                self.mainWin = MainWindow(self)
                self.mainWin.show()
                
        
#-----------------------------------------------------#
if __name__ == '__main__':
    app = CChessApplication()
    sys.exit(app.exec_())
