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

from pubsub import pub

from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui  import *

#-----------------------------------------------------#

class QChessBookWidget(QDockWidget):
    def __init__(self, parent):
        super(QChessBookWidget, self).__init__(u"棋谱",  parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        self.parent = parent
        
        self.step_view = QTreeWidget()
        self.step_view.setColumnCount(1)
        self.step_view.setHeaderLabels([u"序号", u"行棋", u"注释",  u"变招"])
        self.step_view.setColumnWidth(0,60)
        self.step_view.setColumnWidth(1,80)
        self.step_view.setColumnWidth(2,30)
        self.step_view.setColumnWidth(3,120)
        
        self.step_view.itemSelectionChanged.connect(self.onSelectStep)
        
        self.comment_view = QTextEdit()
        self.comment_view.readOnly = True
        
        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Vertical)
        
        splitter.addWidget(self.step_view)
        splitter.addWidget(self.comment_view )
        splitter.setStretchFactor(0,70)
        splitter.setStretchFactor(1,30)
        
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
        move_log = item.data(0, Qt.UserRole)
        
        pub.sendMessage("game_reshow",  move_log = move_log)
                
    def append_move(self, move_log):   
        item = QTreeWidgetItem(self.step_view)
        
        step_no = move_log.step_no
        if step_no % 2 == 1:    
            hint =  "{0}.".format((step_no + 1) / 2) 
            item.setText(0, hint)
        
        item.setText(1, move_log.move_str_zh)
        item.setData(0, Qt.UserRole, move_log)
        
    def append_move_step(self, step_node, index):   
        item = QTreeWidgetItem(self.step_view)
        
        if index % 2 == 1:    
            item.setText(0, str((index + 1) / 2))
        
        item.setText(1, step_node.name)
        item.setData(0, Qt.UserRole, step_node)
        
        if step_node.comment != None:
                item.setText(2, "*")
                #self.comment_view.setText(step_node.comment)
                
    def clear(self):    
        self.step_view.clear()
    
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
        while step_node != None :
            self.append_move_step(step_node, index)
            
            if step_node.child_count() == 1 :
                step_node = step_node.children[0]
            else :
                step_node = None
            
            index += 1
            
#-----------------------------------------------------#
        
class QChessEngineWidget(QDockWidget):
    def __init__(self, parent):
        super(QChessEngineWidget, self).__init__(u"引擎分析",  parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea)

        self.step_view = QListWidget(self)
        
        self.setWidget(self.step_view)
    
    def show_profile(self, yes) :
        if yes :
            pub.subscribe(self.on_game_started, "game_started")
            pub.subscribe(self.on_game_step_moved, "game_step_moved")
            pub.subscribe(self.on_engine_move_info, "engine_move_info")
        else :
            self.step_view.clear()
            pub.unsubscribe(self.on_game_started, "game_started")
            pub.unsubscribe(self.on_game_step_moved, "game_step_moved")
            pub.unsubscribe(self.on_engine_move_info, "engine_move_info")
            
    def on_game_started(self, move_side) :
        self.step_view.clear()
    
    def on_game_step_moved(self, move_log) :
        self.step_view.clear()
            
    def  on_engine_move_info(self, move_info) :
        
        board = Chessboard()
        board.init_board(move_info["fen_str"])
        total_move_str = move_info["depth"] + " " + move_info['score']  
        for (move_from, move_to) in move_info["moves"] :
                if board.can_make_move(move_from, move_to):
                        total_move_str += " " + board.std_move_to_chinese_move(move_from, move_to)
                        board.make_step_move(move_from, move_to)
                        board.turn_side()
                        #fen_after_move = board.get_fen()
                        #step_node = StepNode(move_str, fen_before_move,  fen_after_move, (move_from, move_to), comments)              
                else :
                        print "info move error", move_from, move_to
                        total_move_str  +=  "engine error on move"
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

class QFinalBookWidget(QDockWidget):
    def __init__(self, parent):
        super(QFinalBookWidget, self).__init__(u"棋谱列表",  parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        self.parent = parent
        
        self.book_view = QTableView()
        
        self.book_model = QStandardItemModel(self.book_view)
        #self.book_model.setHorizontalHeaderItem(0, QStandardItem(' '));
        self.book_model.setHeaderData(0,QtCore.Qt.Horizontal, u"级别")  
        self.book_model.setHeaderData(1,QtCore.Qt.Horizontal, u"名称")  
        #self.book_model.setHorizontalHeaderItem(1, QStandardItem(u"名称"));
        
        self.book_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.book_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.book_view.verticalHeader().hide()
        self.book_view.horizontalHeader().setResizeMode(0, QHeaderView.Fixed)
        self.book_view.horizontalHeader().setResizeMode(1, QHeaderView.Fixed)
        
        self.book_view.setColumnWidth(0,30)
        self.book_view.setColumnWidth(1,30)
        #self.book_view.setColumnWidth(2,100)
        
        self.book_view.setModel(self.book_model)
        
        self.book_view.clicked.connect(self.onSelectIndex)
        
        self.setWidget(self.book_view)
        
    def sizeHint(self):
        return QSize(350, 500)    
    
    def minimumSizeHint(self):
        return QSize(350, 500)   
    
    def onSelectIndex(self, index) :
        self.parent.start_final_book(index.row())
         
    def clear(self):    
        self.book_model.clear()
    
    def show_book(self, book):    
        self.clear()
        
        index = 0 
        
        for book_it in book.books :
            #self.book_model.setItem(index, 0, QStandardItem(''));
            self.book_model.setItem(index, 0, QStandardItem(str(book_it.level)));
            self.book_model.setItem(index, 1, QStandardItem(book_it.name));
            index += 1
            
            '''
            view_it = QTreeWidgetItem(self.book_view)
            if  book_it.done :
                b = QBrush(QColor(100,180,100));
                view_it.setBackground(0, b)
                view_it.setBackground(1, b)
                view_it.setBackground(2, b)
               
            view_it.setText(1, str(book_it.level))
            view_it.setText(2, book_it.name)
            view_it.setData(0, Qt.UserRole, book_it)
            '''
   