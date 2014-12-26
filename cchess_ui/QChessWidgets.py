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
        self.step_view.setColumnWidth(0,30)
        self.step_view.setColumnWidth(1,80)
        self.step_view.setColumnWidth(2,30)
        self.step_view.setColumnWidth(3,120)
        
        self.step_view.itemClicked.connect(self.onSelectStep)
        
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
    
    def onSelectStep(self, item, column):
        
        step_node = item.data(0, Qt.UserRole)
        
        if isinstance(step_node,StepNode):
                self.parent.board.init_board(step_node.fen_str_after_step)
        else :
                self.parent.board.init_board(step_node.fen_str)
        
        if step_node.comment != None:
                self.comment_view.setText(step_node.comment)
        else :
                self.comment_view.setText("")
         
    def __append_move(self, move_step):   
        item = QTreeWidgetItem(self.step_view)
        
        step_no = move_step[0]
        
        if step_no % 2 == 1:    
            item.setText(0, str((step_no + 1) / 2))
        
        item.setText(1, move_step[4])
        #item.setData(move_step, Qt.UserRole)
        
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
    
    def undo_move(self):
        #pass
        count = self.step_view.topLevelItemCount()
        
        if count == 0:
            return 
        
        #item = self.step_view.topLevelItem(count - 1)
        #print item
        
        self.step_view.takeTopLevelItem(count -1) 
    
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
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.step_view = QListWidget(self)
        
        self.setWidget(self.step_view)
    
    def  handle_engine_msg(self, engine) :
        
        if engine.move_info_queue.qsize() == 0:
                return 
                
        msg = engine.move_info_queue.get_nowait()
        
        if msg  == None :
                return       
        
        if msg[0] == BOARD_RESET :
                self.step_view.clear()
                
        elif msg[0] == INFO_MOVE :
                move_info = msg[1]       
                board = Chessboard()
                board.init_board(move_info["fen_str"])
                total_move_str = move_info['score']  
                for (move_from, move_to) in move_info["moves"] :
                        if board.can_make_move(move_from, move_to):
                                total_move_str += " " + board.std_move_to_chinese_move(move_from, move_to)
                                board.make_step_move(move_from, move_to)
                                board.turn_side()
                                #fen_after_move = board.get_fen()
                                #step_node = StepNode(move_str, fen_before_move,  fen_after_move, (move_from, move_to), comments)              
                        else :
                                total_move_str  =  "error on move"
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
