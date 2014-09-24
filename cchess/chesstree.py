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

#-----------------------------------------------------#

class LabelNode(object):
    def __init__(self, name, parent = None, step_no = 0):
        
        self.name = name
        
        self.parent = parent
        self.step_no = step_no
        
        self.children = []
    
    def add_child(self, node):
        
        node.parent = self
        node.step_no = self.step_no + self.child_count() + 1
        self.children.append(node)
        
        return node    
    
    def child_count(self):
        return len(self.children)
    
#-----------------------------------------------------#

class StepNode(object):
    def __init__(self, parent, fen_before_move, fen_after_move, move, move_str, comment = None):
        self.parent = parent
        
        self.fen_before_move = fen_before_move
        self.fen_after_move = fen_after_move
        
        self.move = move
        self.move_str = move_str
        self.comment = comment
        
        self.step_no = 0
        
        self.children = []

    def add_child(self, node):
        
        node.parent = self
        node.step_no = self.step_no + self.child_count() + 1
        self.children.append(node)
        
        return node    
    
    def child_count(self):
        return len(self.children)
        
class StepsTree:

    def __init__(self):
        self.head_node = LabelNode(u"=== 开始 ===")
    
    def set_head(self, head_str):
        self.head_node = LabelNode(head_str)
    
    def step_append(self, fen_before_move, fen_after_move, move, move_str, comment = None) :
        node = StepNode(self.head_node, fen_before_move, fen_after_move, move, move_str, comment)
        
        self.head_node.add_child(node)
        
        return node
    
    def add_branch(self, parent, step_no,  name = ''):
        l_node = LabelNode(name)
        
        parent.add_child(l_node)
        
    def step_insert(self, parent, fen_before_move, fen_after_move, move, move_str, comment = None) :
        
        node = StepNode(parent, fen_before_move, fen_after_move, move, move_str, comment)
        
        parent.add_child(node)
        
        return node
        
