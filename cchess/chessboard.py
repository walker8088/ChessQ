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
        self.piece = [0]*48
        self.move_side = None
        
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
        
    def init_board(self, fen_str) :
        if not fen_str:
            fen_str = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1'
                
        self.clear()
        self.fen_parse(fen_str)
        
    def on_create_chessman(self, kind, color, pos, pc):
        return Chessman(self, kind, color, pos, pc)
        
    def create_chessman(self, kind, color, pos, pc):     
        
        new_man = self.on_create_chessman(kind, color, pos, pc)
        
        self._board[pos] = new_man
        self.piece[pc] = pos
    
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

        pc_code = [[16, 17, 19, 21, 23, 25, 27], [32, 33, 35, 37, 39, 41, 43]]
        
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
                        self.create_chessman(kind, RED, (x, y), pc_code[RED][kind])
                        pc_code[RED][kind] += 1

                    x += 1
            elif ch >= 'a' and ch <= 'z':
                if x <= 8:
                    kind = get_kind(ch)

                    if kind != NONE:
                        self.create_chessman(kind, BLACK, (x, y), pc_code[BLACK][kind])
                        pc_code[BLACK][kind] += 1

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
        self.__do_move(p_from, p_to, chessman_)         
        result = not self.check(self.move_side)
        self.__undo_move(p_from, p_to, chessman_)
        
        return result
        """
        
        return True
        
    def make_step_move(self, p_from, p_to):
        
        if not self.can_make_move(p_from, p_to):
            return False
            
        self.__do_move(p_from, p_to)
        
        return True
                
    
    def __do_move(self, p_from, p_to):

        killed_man = None
        if p_to in self._board.keys():
            killed_man = self._board[p_to]
            self.piece[killed_man.pc] = 0

        chessman = self._board.pop(p_from)
        self.piece[chessman.pc] = p_to
        
        chessman.x, chessman.y = p_to
        self._board[p_to] = chessman
        
        return killed_man
        
    def __undo_move(self, p_from, p_to, chessman_):
        chessman = self._board[p_to]
        
        chessman.x, chessman.y = p_from
        self._board[p_from] = chessman

        self.piece[chessman.pc] = p_from
        if chessman_ is not None:
            self._board[p_to] = chessman_
            self.piece[chessman_.pc] = p_to
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
    
    """    
    def save_move(self, p, n, moves, move_side):
        flag = False
        if n in self._board.keys():
            if self._board[n].color is move_side:
                flag = True
                
        chessman = self._board[p]
        ok = self.can_move(chessman, n[0], n[1])
        if not ok:
            flag = True
            
        if not flag:
            move_ = move(p, n)
            moves.append(move_)

    def gen_moves(self, move_side):
        moves = []
        side_tag = 16 + 16 * move_side

        # king
        p = self.piece[side_tag]
        if not p:
            return moves
        for k in range(0, 4):
            tmp = king_dir[k]
            n = (p[0]+tmp[0], p[1]+tmp[1])
            if self._board[p].move_check(n[0], n[1]):
                self.save_move(p, n, moves, move_side)

        # advisor
        for i in range(1,3):
            p = self.piece[side_tag + i]
            if not p:
                continue
            for k in range(0, 4):
                tmp = advisor_dir[k]
                n = (p[0]+tmp[0], p[1]+tmp[1])
                if self._board[p].move_check(n[0], n[1]):
                    self.save_move(p, n, moves, move_side)

        # bishop
        for i in range(3, 5):
            p = self.piece[side_tag + i]
            if not p:
                continue
            for k in range(0, 4):
                tmp = bishop_dir[k]
                n = (p[0]+tmp[0], p[1]+tmp[1])
                if self._board[p].move_check(n[0], n[1]):
                    tmp = bishop_check[k]
                    m = (p[0]+tmp[0], p[1]+tmp[1])
                    if m not in self._board.keys():
                        self.save_move(p, n, moves, move_side)

        # knight
        for i in range(5, 7):
            p = self.piece[side_tag + i]
            if not p:
                continue
            for k in range(0, 8):
                tmp = knight_dir[k]
                n = (p[0]+tmp[0], p[1]+tmp[1])
                if self._board[p].move_check(n[0], n[1]):
                    tmp = knight_check[k]
                    m = (p[0]+tmp[0], p[1]+tmp[1])
                    if m not in self._board.keys():
                        self.save_move(p, n, moves, move_side)

        # rook
        for i in range(7, 9):
            p = self.piece[side_tag + i]
            if not p:
                continue
            for k in range(0, 4):
                for j in range(1, 10):
                    tmp = rook_dir[k]
                    n = (p[0]+j*tmp[0],p[1]+j*tmp[1])
                    if not self._board[p].move_check(n[0], n[1]):
                        break
                    if n not in self._board.keys():
                        move_ = move(p, n)
                        moves.append(move_)
                    else:
                        if self._board[n].color is not move_side:
                            move_ = move(p, n)
                            moves.append(move_)
                        break

        # cannon
        for i in range(9, 11):
            p = self.piece[side_tag + i]
            if not p:
                continue
            for k in range(0, 4):
                over_flag = 0
                for j in range(1, 10):
                    tmp = cannon_dir[k]
                    n = (p[0]+j*tmp[0],p[1]+j*tmp[1])
                    if not self._board[p].move_check(n[0], n[1]):
                        break
                    if n not in self._board.keys():
                        if not over_flag:
                            move_ = move(p, n)
                            moves.append(move_)
                    else:
                        if not over_flag:
                            over_flag = 1
                        else:
                            self.save_move(p, n, moves, move_side)
                            break

        # pawn
        for i in range(11, 16):
            p = self.piece[side_tag + i]
            if not p:
                continue

            flag = 0
            if p[1] > 4:
                flag = 1

            for k in range(0, 3):
                tmp = pawn_dir[flag][k]
                n = (p[0]+tmp[0], p[1]+tmp[1])
                if self._board[p].move_check(n[0], n[1]):
                    self.save_move(p, n, moves, move_side)
                    
        return moves

    def check(self, move_side):
        side_tag = 32 - move_side * 16
        
        # king
        w_king = self.piece[16]
        b_king = self.piece[32]

        if not w_king or not b_king:
            return False
        
        kill = True
        if w_king[0] == b_king[0]:
            min_y = min(w_king[1], b_king[1])
            max_y = max(w_king[1], b_king[1])
            for m_y in range(min_y+1, max_y):
                if (w_king[0] ,m_y) in self._board.keys():
                    kill = False
                    break
            if kill:
                return kill
        
        # knight
        q = self.piece[48 - side_tag]
        
        for i in range(5, 7):
            p = self.piece[side_tag + i]
            if not p:
                continue
            for k in range(0, 8):
                tmp = knight_dir[k]
                n = (p[0]+tmp[0], p[1]+tmp[1])
                if n != q:
                    continue
                if self._board[p].move_check(n):
                    tmp = knight_check[k]
                    m = (p[0]+tmp[0], p[1]+tmp[1])
                    if m not in self._board.keys():
                        return True

        # rook
        for i in range(7, 9):
            kill = True
            
            p = self.piece[side_tag + i]
            if not p:
                continue
            if p[0] == q[0]:
                min_y = min(p[1], q[1])
                max_y = max(p[1], q[1])

                for m_y in range(min_y+1, max_y):
                    if (p[0], m_y) in self._board.keys():
                        kill = False
                        break
                    
                if kill:
                    return kill
            elif p[1] == q[1]:
                min_x = min(p[0], q[0])
                max_x = max(p[0], q[0])

                for m_x in range(min_x+1, max_x):
                    if (m_x, p[1]) in self._board.keys():
                        kill = False
                        break
                    
                if kill:
                    return kill

        # cannon
        for i in range(9, 11):
            over_flag = 0
            p = self.piece[side_tag + i]
            if not p:
                continue
            if p[0] == q[0]:
                min_y = min(p[1], q[1])
                max_y = max(p[1], q[1])

                for m_y in range(min_y+1, max_y):
                    if (p[0], m_y) in self._board.keys():
                        if not over_flag:
                            over_flag = 1
                        else:
                            over_flag = 2
                            break
                if over_flag == 1:
                    return True
            elif p[1] == q[1]:
                min_x = min(p[0], q[0])
                max_x = max(p[0], q[0])
                for m_x in range(min_x+1, max_x):
                    if (m_x, p[1]) in self._board.keys():
                        if not over_flag:
                            over_flag = 1
                        else:
                            over_flag = 2
                if over_flag == 1:
                    return True
        
        # pwan
        for i in range(11, 16):
            p = self.piece[side_tag + i]
            if not p:
                continue
            
            flag = 0
            if p[1] > 4:
                flag = 1
                
            for k in range(0, 3):
                tmp = pawn_dir[flag][k]
                n = (p[0]+tmp[0], p[1]+tmp[1])
                if n != q:
                    continue
                if self._board[p].move_check(n[0], n[1]):
                    print "here6"       
                    return True
       
        return False    
    """    
