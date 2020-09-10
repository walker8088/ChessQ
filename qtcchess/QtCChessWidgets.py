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

from cchess import *

from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#-----------------------------------------------------#

class QMoveHistoryWidget(QDockWidget):
    def __init__(self, parent):
        super().__init__("棋谱", parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.parent = parent

        self.step_view = QTreeWidget()
        self.step_view.setColumnCount(1)
        self.step_view.setHeaderLabels(["序号", "行棋", "注释"])
        self.step_view.setColumnWidth(0, 60)
        self.step_view.setColumnWidth(1, 80)
        self.step_view.setColumnWidth(2, 30)
        #self.step_view.setColumnWidth(3, 120)

        self.step_view.itemSelectionChanged.connect(self.onSelectStep)

        self.comment_view = QTextEdit()
        self.comment_view.readOnly = True

        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Vertical)

        splitter.addWidget(self.step_view)
        splitter.addWidget(self.comment_view)
        splitter.setStretchFactor(0, 70)
        splitter.setStretchFactor(1, 30)

        self.setWidget(splitter)

    def sizeHint(self):
        return QSize(350, 500)

    def minimumSizeHint(self):
        return QSize(350, 500)

    def onSelectStep(self):
        
        items = self.step_view.selectedItems()

        if len(items) != 1:
            return

        item = items[0]
        move = item.data(0, Qt.UserRole)

    def newMove(self, move, num, good):
        item = QTreeWidgetItem(self.step_view)

        if num % 2 == 1:
            hint = "{0}.".format((num + 1) // 2)
            item.setText(0, hint)

        item.setText(1, move.to_chinese())
        item.setData(0, Qt.UserRole, move)
        item.setData(1, Qt.UserRole, good)

    def get_all_items(self):
        """Returns all QTreeWidgetItems in the given QTreeWidget."""
        all_items = []
        for i in range(self.step_view.topLevelItemCount()):
            top_item = self.step_view.topLevelItem(i)
            all_items.append(top_item)
        return all_items

    def clear(self):
        self.step_view.clear()
    
    def showGoodMoves(self, yes):
        items = self.get_all_items()
        for it in items:
            good = it.data(1, Qt.UserRole)
            if good:
                it.setText(2, 'Yes')
            else:
                it.setText(2, '')
            
    def undo_move(self, steps):
        while steps > 1:
            count = self.step_view.topLevelItemCount()

            if count < 1:
                return

            self.step_view.takeTopLevelItem(count - 1)

            steps -= 1

    def show_book(self, book):

        self.clear()

        step_node = book["steps"]

        index = 0
        while step_node != None:
            self.append_move_step(step_node, index)

            if step_node.child_count() == 1:
                step_node = step_node.children[0]
            else:
                step_node = None

            index += 1


#-----------------------------------------------------#
'''
class QChessEngineWidget(QDockWidget):
    def __init__(self, parent):
        super().__init__("引擎分析", parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea
                             | Qt.BottomDockWidgetArea)

        self.step_view = QListWidget(self)

        self.setWidget(self.step_view)

    def show_profile(self, yes):
        if yes:
            pub.subscribe(self.on_game_started, "game_started")
            pub.subscribe(self.on_game_step_moved, "game_step_moved")
            pub.subscribe(self.on_engine_move_info, "engine_move_info")
        else:
            self.step_view.clear()
            pub.unsubscribe(self.on_game_started, "game_started")
            pub.unsubscribe(self.on_game_step_moved, "game_step_moved")
            pub.unsubscribe(self.on_engine_move_info, "engine_move_info")

    def on_game_started(self, move_side):
        self.step_view.clear()

    def on_game_step_moved(self, move_log):
        self.step_view.clear()

    def on_engine_move_info(self, move_info):

        board = Chessboard()
        board.init_board(move_info["fen_str"])
        total_move_str = move_info["depth"] + " " + move_info['score']
        for (move_from, move_to) in move_info["moves"]:
            if board.can_make_move(move_from, move_to):
                total_move_str += " " + board.std_move_to_chinese_move(
                    move_from, move_to)
                board.make_step_move(move_from, move_to)
                board.turn_side()
                #fen_after_move = board.get_fen()
                #step_node = StepNode(move_str, fen_before_move,  fen_after_move, (move_from, move_to), comments)
            else:
                #print("info move error", move_from, move_to)
                total_move_str += "engine error on move"
                break
        self.step_view.addItem(total_move_str)

    def append_info(self, info):
        self.step_view.addItem(info)

    def clear(self):
        self.step_view.clear()

    def sizeHint(self):
        return QSize(450, 500)

    def minimumSizeHint(self):
        return QSize(450, 500)

'''
#------------------------------------------------------------------#
class QEndBookWidget(QDockWidget):
    def __init__(self, parent):
        super().__init__("棋局列表", parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.parent = parent

        self.bookView = QListView()

        self.bookModel = QStandardItemModel(self.bookView)
        #self.bookModel.setHorizontalHeaderItem(0, QStandardItem(' '));
        
        self.bookView.setModel(self.bookModel)
        self.bookView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.bookView.setAlternatingRowColors(True) 

        self.bookView.clicked.connect(self.onSelectIndex)

        self.setWidget(self.bookView)

    def sizeHint(self):
        return QSize(150, 500)

    def minimumSizeHint(self):
        return QSize(150, 500)

    def onSelectIndex(self, index):
        self.parent.startGameIndex(index.row())
        
    def select(self, index):
        i = self.bookModel.index(index,0);
        self.bookView.setCurrentIndex(i)
 
    def showGameBook(self, books):
        self.bookModel.clear()
        
        for i, it in enumerate(books):
            self.bookModel.setItem(i, 0, QStandardItem(it[0][0]))
            if it[1] == ord('1'):
                self.bookModel.setData(self.bookModel.index(i, 0), QBrush(QColor("#00bbcc")), Qt.ForegroundRole);
            
#------------------------------------------------------------------#
