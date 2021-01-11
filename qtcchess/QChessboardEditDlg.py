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

from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from cchess import *

from .QtCChessBoard import *

#-----------------------------------------------------#

class QChessboardEditDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)

        #self.setFixedSize(200, 120)

        vbox = QVBoxLayout()

        self.boardEdit = QChessBoardEditWidget()
        vbox.addWidget(self.boardEdit)

        self.fenEdit = QLineEdit()
        vbox.addWidget(self.fenEdit)

        initBtn = QPushButton("初始棋盘", self)
        clearBtn = QPushButton("清空棋盘", self)

        initBtn.clicked.connect(self.onInitBoard)
        clearBtn.clicked.connect(self.onClearBoard)

        okBtn = QPushButton("完成", self)
        cancelBtn = QPushButton("取消", self)
        #self.quit.setGeometry(62, 40, 75, 30)

        hbox = QHBoxLayout()

        hbox.addWidget(initBtn)
        hbox.addWidget(clearBtn)
        hbox.addWidget(okBtn)
        #hbox.addWidget(cancelBtn)

        vbox.addLayout(hbox)

        self.setLayout(vbox)
        
        self.fenEdit.textEdited.connect(self.onTextEdited)
        okBtn.clicked.connect(self.accept)
        #cancelBtn.clicked.connect(self.onClose)

    def onInitBoard(self):
        self.boardEdit.init_board(FULL_INIT_FEN)
        self.fenEdit.setText(self.boardEdit.to_fen())
    
    def onTextEdited(self, text):
        self.boardEdit.init_board(text)
        
    def update_fen(self):
        self.fenEdit.setText(self.boardEdit.to_fen())

    def onClearBoard(self):
        self.boardEdit.init_board('')
        self.fenEdit.setText(self.boardEdit.to_fen())

    def editBoard(self, fen_str):

        self.fenEdit.setText(fen_str)
        self.boardEdit.init_board(fen_str)

        if self.exec_()  == QDialog.Accepted :
            return self.boardEdit.to_fen()
        else :
            return None
