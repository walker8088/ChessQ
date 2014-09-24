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

from xml.etree import ElementTree as et

from chesstree import *
from chessboard import *

#-----------------------------------------------------#

class ChessBook(dict):
    def __init__(self):
        self.infos = {}
        self.result = None
        self.init_fen = None
        self.steps = StepsTree()
        
    def load_from_cbf_file(self, file_name):
        
        def decode_move(move_str):
            p_from = (int(move_str[0]), int(move_str[1])) 
            p_to = (int(move_str[3]), int(move_str[4])) 
            
            return (p_from, p_to)
            
        tree = et.parse(file_name)
        root = tree.getroot()
        
        head = root.find("Head")
        for node in head.getchildren() :
            if node.tag == "FEN":
                self.init_fen = node.text
            print node.tag
        
        board = Chessboard()
        board.init_board(self.init_fen)
        
        move_list = root.find("MoveList").getchildren()
        
        head_node = move_list[0]
        if head_node.text :
            self.steps.set_head(head_node.text)
            print head_node.text
            
        for node in move_list[1:] :
            
            p_from, p_to = decode_move(node.attrib["value"])
            
            if not board.can_make_move(p_from, p_to):
                raise Exception("Move Error")
            
            fen_before_move = board.get_fen() 
            chinese_move_str = board.std_move_to_chinese_move(p_from, p_to) 
            board.make_step_move(p_from, p_to) 
            fen_after_move = board.get_fen()
            
            self.steps.step_append(fen_before_move, fen_after_move, (p_from, p_to), chinese_move_str, node.text)
            board.turn_side()
            
            #print p_from, p_to, chinese_move_str
            
    def write_to_pgn_file(self, file_name):
        pass
        
    def load_from_pgn_file(self,  file_name):     
        with open(file_name) as file:
            flines = file.readlines()
        
        lines = []
        for line in flines :
            it = line.strip().decode("GBK") #TODO, fix it in linux
            
            if len(it) == 0:
                continue
                
            lines.append(it)
            
        lines = self.__get_headers(lines)
        lines, docs = self.__get_comments(lines)
        self.infos["Doc"] = docs
        self.__get_steps(lines)
       
    def __get_headers(self,  lines):    
        
        index = 0
        for line in lines:
            
            if line[0] != "[" :
                return lines[index:]
                
            if line[-1] != "]":
                raise Exception("Format Error on line %" %(index + 1))
                
            items = line[1:-1].split("\"")
            
            if len(items) < 3: 
                raise Exception("Format Error on line %" %(index + 1))
            
            self.infos[str(items[0]).strip()] = items[1].strip()
            
            index += 1
    
    def __get_comments(self, lines):    
        
        if lines[0][0] != "{" :
            return (lines, None)
        
        docs = lines[0][1:]
        
        #处理一注释行的情况
        if docs[-1] == "}":
            return (lines[1:], docs[:-1].strip())
        
        #处理多行注释的情况    
        index = 1

        for line in lines[1:]:
            if line[-1] == "}":
                docs = docs + "\n" + line[:-1]
                return (lines[index+1:], docs.strip())
            
            docs = docs + "\n" + line
            index += 1        
            
        #代码能运行到这里，就是出了异常了
        raise Exception("Comments not closed")    
        
    def __get_token(self,  token_mode,  lines):
        pass
        
    def __get_steps(self, lines,  next_step = 1):    
        
        for line in lines :
            if line in["*", "1-0","0-1", "1/2-1/2"]:
                return 
                
            print line
            items = line.split(".")
            
            if(len(items) < 2):
                continue
                raise Exception("format error")
                
            steps = items[1].strip().split(" ")
            print steps
            
    

################################################
if __name__ == '__main__':
    book = ChessBook()
    #book.load_from_pgn_file("test/test.PGN")
    book.load_from_cbf_file("test/test.cbf")
    
