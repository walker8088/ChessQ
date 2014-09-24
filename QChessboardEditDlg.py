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

from cchess import *

from QChessman import *
from QChessboardEditor import *

#-----------------------------------------------------#

class QChessboardEditDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
    
        #self.setFixedSize(200, 120)
        
        vbox = QVBoxLayout()
        
        self.boardEdit = QChessboardEditWidget()
        vbox.addWidget(self.boardEdit)
        
        self.fenEdit = QtGui.QLineEdit()
        vbox.addWidget(self.fenEdit)
        
        initBtn = QPushButton(u"初始棋盘", self)
        clearBtn = QPushButton(u"清空棋盘", self)
        
        initBtn.clicked.connect(self.onInitBoard)
        clearBtn.clicked.connect(self.onClearBoard)
        
        okBtn = QtGui.QPushButton(u"完成", self)
        cancelBtn = QtGui.QPushButton(u"取消", self)
        #self.quit.setGeometry(62, 40, 75, 30)
        
        hbox = QHBoxLayout()
        
        hbox.addWidget(initBtn)
        hbox.addWidget(clearBtn)
        hbox.addWidget(okBtn)
        hbox.addWidget(cancelBtn)
        
        vbox.addLayout(hbox)
        
        self.setLayout(vbox);
         
        self.connect(okBtn, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("close()"))
        
        self.connect(cancelBtn, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("close()"))
    
    def onInitBoard(self):
        self.boardEdit.init_board()
        self.fenEdit.setText(self.boardEdit.get_fen())
        
    def onClearBoard(self):
        self.boardEdit.clear()
        self.fenEdit.setText(self.boardEdit.get_fen())
        
    def editBoard(self, fen_str):
        
        self.fenEdit.setText(fen_str)
        self.boardEdit.init_board(fen_str)
        
        self.exec_() #== QDialog.Accepted :

        return self.boardEdit.get_fen()
        #else :
        #    return fen_str
