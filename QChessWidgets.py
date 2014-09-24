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

#-----------------------------------------------------#

class QChessBookWidget(QDockWidget):
    def __init__(self, parent):
        super(QChessBookWidget, self).__init__(u"棋谱",  parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        self.parent = parent
        
        self.view = QTreeWidget()
        
        self.view.setColumnCount(1)
        self.view.setHeaderLabels([u"序号", u"行棋"])
        self.view.setColumnWidth(0,40)
        self.view.setColumnWidth(1,80)
        #self.view.setColumnWidth(2,280)
        self.view.itemClicked.connect(self.onSelectStep)
        
        self.setWidget(self.view)
    
    def sizeHint(self):
        return QSize(350, 500)    
    
    def minimumSizeHint(self):
        return QSize(350, 500)   
    
    def onSelectStep(self, item, column):
        step = item.data(0, Qt.UserRole)
        self.parent.board.init_board(step.fen_after_move)
        
    def append_move(self, move_step):   
        item = QTreeWidgetItem(self.view)
        
        step_no = move_step[0]
        
        if step_no % 2 == 1:    
            item.setText(0, str((step_no + 1) / 2))
        
        item.setText(1, move_step[4])
        #item.setData(move_step, Qt.UserRole)
        
    def append_move_step(self, step):   
        item = QTreeWidgetItem(self.view)
        
        if step.step_no % 2 == 1:    
            item.setText(0, str((step.step_no + 1) / 2))
        
        item.setText(1, step.move_str)
        item.setData(0, Qt.UserRole, step)
        
    def clear(self):    
        self.view.clear()
    
    def undo_move(self):
        #pass
        count = self.view.topLevelItemCount()
        
        print count  
        
        if count == 0:
            return 
        
        #item = self.view.topLevelItem(count - 1)
        #print item
        
        self.view.takeTopLevelItem(count -1) 
    
    def show_book(self, book):    
        self.clear()
        for item in book.steps.head_node.children:
            self.append_move_step(item)
            
#-----------------------------------------------------#
        
class QChessEngineWidget(QDockWidget):
    def __init__(self, parent):
        super(QChessEngineWidget, self).__init__(u"引擎分析",  parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.view = QListWidget(self)
        
        self.setWidget(self.view)
        
    def append_info(self, info):   
        self.view.addItem(info)
        
    def clear(self):    
        self.view.clear()
    
    def sizeHint(self):
        return QSize(350, 500)    
    
    def minimumSizeHint(self):
        return QSize(350, 500)   
