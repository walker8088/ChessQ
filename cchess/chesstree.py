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

from common import *

#-----------------------------------------------------#

class LabelNode(object):
    def __init__(self, name, fen_str = None,  comment = None):
        
        self.parent = None
        self.name = name
        self.fen_str = fen_str
        self.comment = comment
        self.children = []
    
    def add_child(self, node):
        node.parent = self
        self.children.append(node)
        return node    
    
    def child_count(self):
        return len(self.children)
    
#-----------------------------------------------------#

class StepNode(LabelNode):
    def __init__(self, name, fen_str, fen_str_after_step, move, comment = None):
        super(StepNode, self).__init__(name, fen_str, comment)
        
        self.fen_str_after_step = fen_str_after_step
        self.move = move

#-----------------------------------------------------#
def dump_info(book)  :   
       
        print
        print  u"格式：", book["source"]
        print  u"版本：", book["version"]
        print  u"类型：", book_type_str[book["book_type"]]
        print  u"标题：", book["title"]
        print  u"比赛：", book["match"]
        print  u"红方：", book["players"][0]
        print  u"黑方：", book["players"][1]
        print  u"结果：", result_str[book["result"]]
        print  u"解说：", book["narrator"]
        print  u"作者：", book["author"]
        print  "fen",       book["fen_str"]
        print  "moves",  book["moves"]
        print
    
#-----------------------------------------------------#

def dump_steps(step_node) :        
        count = 0
        break_line = False
        while step_node != None:
                if  (count % 2) == 1:
                        print "%3d." % ((count+1)  / 2),
                elif  break_line :
                        print "%3d.  ......   " % ((count+1)  / 2),
                        break_line = False
                
                print step_node.name, " ", 
               
                if  (count % 2) == 0:
                        print 
                        
                if step_node.comment != None :
                        if  (count % 2) == 1:
                                break_line = True
                                print 
                        print 
                        print  step_node.comment
                
                if step_node.child_count() > 0:
                        step_node = step_node.children[0]
                else :
                        step_node = None
                
                count += 1