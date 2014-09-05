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

from QChessBoard import *
from QChessWidgets import *

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
        self.finalbook = FinalBook(u"challengers/基本杀法.EPD")
        
        self.timer = QTimer()
        self.timer.start(50)
        self.timer.timeout.connect(self.onIdleRun)
        
        self.resize(800, 700)
         
        self.center()
        #self.showMaximized()
        
        self.readSettings()
        
        
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
        #event.accept()
    
    def onFlipBoardChanged(self, state):
        
        self.board.setFlipBoard(state)
        
    def onRedBoxChanged(self, state):
        
        if not self.table.players[0] :
            return
        
        if state == Qt.Checked:
            self.table.players[0].bind_engine(self.engine)
        else :
            self.table.players[0].bind_engine(None)
            
    def onBlackBoxChanged(self, state):
        
        if not self.table.players[1] :
            return
            
        if state == Qt.Checked :
            self.table.players[1].bind_engine(self.engine)
        else :
            self.table.players[1].bind_engine(None)
        
    def onInfoBoxChanged(self, state):
        pass
        
    def open(self):
        pass

    def save(self):
        pass
        
    def saveAs(self):
        fileName = QFileDialog.getSaveFileName(self, "Save As",
                self.curFile)
        if not fileName:
            return False

        return self.saveFile(fileName)

    def about(self):
        QMessageBox.about(self, u"关于ChessQ",
                ""
                "")
                
    def onNewGame(self):
        
        self.setWindowTitle(APP_NAME)
        
        player1 = UiChessPlayer(self.table)
        if self.eRedBox.isChecked(): 
            player1.bind_engine(self.engine)
        
        player2 = UiChessPlayer(self.table)
        if self.eBlackBox.isChecked(): 
            player2.bind_engine(self.engine)
        
        self.bookView.clear()
                
        self.table.new_game((player1, player2))
        self.table.start_game()
        
    def onFinalChallenge(self) :
        
        
        curr_book = self.finalbook.curr_book()
        
        player1 = UiChessPlayer(self.table)
        if self.eRedBox.isChecked(): 
            player1.bind_engine(self.engine)
            
        player2 = UiChessPlayer(self.table)
        if self.eBlackBox.isChecked(): 
            player2.bind_engine(self.engine)
        
        self.setWindowTitle(APP_NAME + curr_book[0])
        self.bookView.clear()
        
        self.table.new_game((player1, player2), curr_book[1])
        self.table.start_game()
        
    def notify_move_from_table(self, move_step) :
        
        #self.table.undo_move()
        self.bookView.append_move(move_step)
       
    def notify_unmove_from_table(self, move_step) :
        pass
        
    def onUndoMove(self) :
        self.table.undo_move()
    
    def onEndGame(self) :
        self.table.stop_game()
        
    def onLoadEngine(self):
        pass
        
    def on_game_over(self, over_side):
        
        if over_side == BLACK:
            #QMessageBox.warning(self,  APP_NAME, u"挑战成功!")
            self.finalbook.next_book()
            print u"挑战成功", self.finalbook.index
        else:
            #QMessageBox.warning(self,  APP_NAME, u"挑战失败!")
            self.finalbook.next_book()
            
            print u"挑战失败", self.finalbook.index
            
        self.onFinalChallenge()
        
    def createActions(self):
        self.newGameAct = QAction(u"新对局", self, 
                statusTip=u"新对局", triggered=self.onNewGame)
        
        self.finalChallengeAct = QAction(u"残局挑战", self, 
                statusTip=u"残局挑战", triggered=self.onFinalChallenge)
        
        self.undoMoveAct = QAction(u"悔棋", self, 
                statusTip=u"悔棋", triggered=self.onUndoMove)
        
        self.endGameAct = QAction(u"结束对局", self, 
                statusTip=u"结束对局", triggered=self.onEndGame)
        
        self.loadEngineAct = QAction(u"加载引擎", self, 
                statusTip=u"加载象棋引擎", triggered=self.onLoadEngine)
        
        self.openAct = QAction(QIcon(':/images/open.png'),
                "&Open...", self, shortcut=QKeySequence.Open,
                statusTip="Open an existing file", triggered=self.open)

        self.saveAct = QAction(QIcon(':/images/save.png'),
                "&Save", self, shortcut=QKeySequence.Save,
                statusTip="Save the document to disk", triggered=self.save)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                statusTip="Exit the application",
                triggered=qApp.closeAllWindows)

        self.aboutAct = QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        #self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        #self.fileMenu.addAction(self.closeAct)
        self.fileMenu.addAction(self.exitAct)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)

    def createToolBars(self):
        self.gameToolbar = self.addToolBar("Game")
        self.gameToolbar.addAction(self.newGameAct)
        self.gameToolbar.addAction(self.finalChallengeAct) 
        self.gameToolbar.addAction(self.undoMoveAct)
        self.gameToolbar.addAction(self.endGameAct)
        
        self.boardToolbar = self.addToolBar("Board")
        self.flipBoardBox = QCheckBox(u"反转棋盘")
        self.flipBoardBox.stateChanged.connect(self.onFlipBoardChanged)
        self.boardToolbar.addWidget(self.flipBoardBox)
        
        self.engineToolbar = self.addToolBar("Engine")
        self.engineToolbar.addAction(self.loadEngineAct)
        
        self.eRedBox = QCheckBox(u"引擎执红")
        self.eRedBox.setChecked(False);
        self.eRedBox.stateChanged.connect(self.onRedBoxChanged)
        
        self.eBlackBox = QCheckBox(u"引擎执黑")
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
        self.table = ChessTable(self, self.board)
        
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
