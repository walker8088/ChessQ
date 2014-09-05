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

class TreeItem(object):
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0


class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self):
        super(TreeModel, self).__init__(parent = None)

        self.rootItem = TreeItem((u"序号", u"步骤", u"注释"))
        
        #self.setupModelData(data.split('\n'), self.rootItem)
    def append_move(self, move_str):
        
        childItem = TreeItem((move_str, ""), self.rootItem)
        
        self.rootItem.appendChild(childItem)
        row = childItem.row()
        print row
        index = self.createIndex(row, 1, childItem)
        
        self.dataChanged.emit(index, index)
            
    def columnCount(self, parent):
        return 3
        
    def data(self, index, role):
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole:
            return None

        item = index.internalPointer()
        
        col = index.column()
        
        if col == 0:
            return str(0)
        else:    
            return item.data(col-1)

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

#-----------------------------------------------------#

class QChessBookWidget(QDockWidget):
    def __init__(self, parent):
        super(QChessBookWidget, self).__init__(u"棋谱",  parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        #self.model = TreeModel()
        
        #self.view = QTreeView(self)
        #self.view.setModel(self.model)
        
        self.view = QTreeWidget()
        
        self.view.setColumnCount(3)
        self.view.setHeaderLabels([u"序号", u"走子", u"备注"])
        self.view.setColumnWidth(0,40)
        self.view.setColumnWidth(1,80)
        self.view.setColumnWidth(2,280)
 
        self.setWidget(self.view)
    
    def sizeHint(self):
        return QSize(350, 500)    
    
    def minimumSizeHint(self):
        return QSize(350, 500)   

    def append_move(self, move_step):   
        item = QTreeWidgetItem(self.view)
        
        step_no = move_step[0]
        
        if step_no % 2 == 1:    
            item.setText(0, str((step_no + 1) / 2))
        
        item.setText(1, move_step[4])
        #item.setData(move_step)
        
    def clear(self):    
        self.view.clear()
        
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
