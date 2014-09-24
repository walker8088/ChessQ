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

import sys

from common import *
from chessman import *

#-----------------------------------------------------#

class Chessboard(object):
    def __init__(self):
        
        self.clear()

    def clear(self):
        
        self._board = {}
        self.move_side = RED
        
    def at_pos(self, x, y):
        
        pos = (x, y)
        
        if pos in self._board.keys():
            return self._board[pos]
        else :
            return None
            
    def turn_side(self) :
        
        if self.move_side == None :
            return None
            
        self.move_side = 1 - self.move_side
        
        return self.move_side
        
    def init_board(self, fen_str = None) :
        if not fen_str:
            fen_str = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1'
                
        self.clear()
        self.fen_parse(fen_str)
        
    def on_create_chessman(self, kind, color, pos):
        return Chessman(self, kind, color, pos)
        
    def create_chessman(self, kind, color, pos):     
        
        new_man = self.on_create_chessman(kind, color, pos)
        
        if new_man:
            self._board[pos] = new_man
        
    def remove_chessman(self, pos):     
        if pos in self._board.keys():
            self._board.pop(pos)
        
    def chinese_move_to_std_move(self, move_str):
        
        move_indexs = [u"前", u"中", u"后", u"一", u"二", u"三", u"四", u"五"]
        
        multi_man = False
        multi_lines = False
        
        if move_str[0] in move_indexs:
            
            man_index = move_indexs.index(mov_str[0])
            
            if man_index > 1:
                multi_lines = True
                
            multi_man = True
            man_name = move_str[1]
            
        else :
            
            man_name = move_str[0]
        
        if man_name not in chessman_show_names[self.move_side]:
            print "error",  move_str     
        
        man_kind = chessman_show_names[self.move_side].index(man_name)
        if not multi_man:
            #单子移动指示
            man_x = h_level_index[self.move_side].index(man_name)
            mans = __get_mans_at_vline(man_kind, self.move_side) 
            
            #无子可走
            if len(mans) == 0:
                return None
            
            #同一行选出来多个
            if (len(mans) > 1) and (man_kind not in[ADVISOR, BISHOP]):
                #只有士象是可以多个子尝试移动而不用标明前后的
                return None
            
            for man in mans:
                move = man.chinese_move_to_std_move(move_str[2:]) 
                if move :
                    return move
            
            return None
            
        else:
            #多子选一移动指示
            mans = __get_mans_of_kind(man_kind, self.move_side) 
            
        
    def __get_mans_of_kind(self, kind, color):
        
        mans = []
        for key in self._board.keys():    
            man = self._board[key]
            if man.kind == kind and man.color == color:
                mans.append(man)
        
        return mans 
    
    def __get_mans_at_vline(self, kind, color, x):
        
        mans = __get_mans_of_kind(kind, color)
        
        new_mans = []
        for man in mans:    
            if man.x == x:
                new_mans.append(man)
        
        return new_mans 
        
    def std_move_to_chinese_move(self, p_from, p_to):
        
        man = self._board[p_from]
        
        return man.std_move_to_chinese_move(p_to)
    
    def get_fen(self):
        fen_str = ''
        count = 0
        for j in range(10):
            for i in range(9):
                if (i, j) in self._board.keys():
                    if count is not 0:
                        fen_str += str(count)
                        count = 0
                    chessman = self._board[(i, j)]
                    ch = get_char(chessman.kind, chessman.color)
                    
                    if ch is not '':
                        fen_str += ch
                else:
                    count += 1
                    
            if count > 0:
                fen_str += str(count)
                count = 0
            if j < 9:
                fen_str += '/'
                
        if self.move_side is BLACK:
            fen_str += ' b'
        else:
            fen_str += ' w'
            
        fen_str += ' - - 0 1'

        return fen_str

    def fen_parse(self, fen_str):
        
        self.clear()
            
        if fen_str == '':
                return

        #pc_code = [[16, 17, 19, 21, 23, 25, 27], [32, 33, 35, 37, 39, 41, 43]]
        
        x = y = 0

        for i in range(0, len(fen_str)):
            ch = fen_str[i]
            if ch == ' ':
                break

            if ch == '/':
                x = 0
                y += 1

                if y > 9:
                    break
            elif ch >= '1' and ch <= '9':
                x += int(ch)
                if x > 8:
                    x = 8
            elif ch >= 'A' and ch <= 'Z':
                if x <= 8:
                    kind = get_kind(ch)

                    if kind != NONE:
                        self.create_chessman(kind, RED, (x, y))
                        
                    x += 1
            elif ch >= 'a' and ch <= 'z':
                if x <= 8:
                    kind = get_kind(ch)

                    if kind != NONE:
                        self.create_chessman(kind, BLACK, (x, y))
                        
                    x += 1

        if fen_str[i+1] == 'b':
             self.move_side = BLACK
        else:
             self.move_side = RED            

    def can_make_move(self, p_from, p_to) :
        
        #print p_from,  p_to
        
        if (p_from[0] == p_to[0]) and (p_from[1] == p_to[1]):
            print "no move"
            return False
            
        if p_from not in self._board.keys():
            print "not in"
            return False 
        
        chessman = self._board[p_from]
        if chessman.color != self.move_side:
            print "not color", chessman.color, self.move_side
            return False
            
        if not chessman.can_move_to(p_to[0],  p_to[1]):
            print "can not move"
            return False
        
        """
        chessman_ = None
        if p_to in self._board.keys():
            chessman_ = self._board[p_to]
        self._do_move(p_from, p_to, chessman_)         
        result = not self.check(self.move_side)
        self._undo_move(p_from, p_to, chessman_)
        
        return result
        """
        
        return True
        
    def make_step_move(self, p_from, p_to):
        
        #print "step move", p_from,  p_to
        if not self.can_make_move(p_from, p_to):
            return False
            
        self._do_move(p_from, p_to)
        
        return True
                
    
    def _do_move(self, p_from, p_to):

        killed_man = None
        if p_to in self._board.keys():
            killed_man = self._board[p_to]
            
        chessman = self._board.pop(p_from)
        
        chessman.x, chessman.y = p_to
        self._board[p_to] = chessman
        
        return killed_man
        
    def _undo_move(self, p_from, p_to, chessman_):
        chessman = self._board[p_to]
        
        chessman.x, chessman.y = p_from
        self._board[p_from] = chessman

        if chessman_ is not None:
            self._board[p_to] = chessman_
        else:
            del self._board[p_to]
    
    def between_v_line(self, x, y1, y2):
        
        min_y = min(y1, y2)
        max_y = max(y1, y2)
        
        #if (max_y - min_y) <= 1:
        #    return 0
        
        count = 0
        for m_y in range(min_y+1, max_y):
            if (x, m_y) in self._board.keys():
                count += 1
                
        return count    
    
    def between_h_line(self, y, x1, x2):
        
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        
        count = 0
        for m_x in range(min_x+1, max_x):
            if (m_x, y) in self._board.keys():
                count  += 1
        
        return count
