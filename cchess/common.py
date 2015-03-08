# -*- coding: utf-8 -*-

RED, BLACK = 0, 1

KING, ADVISOR, BISHOP, KNIGHT, ROOK, CANNON, PAWN, NONE = range(8)


def get_kind(fen_ch):
    if fen_ch in ['k', 'K']:
        return KING
    elif fen_ch in ['a', 'A']:
        return ADVISOR
    elif fen_ch in ['b', 'B']:
        return BISHOP
    elif fen_ch in ['n', 'N']:
        return KNIGHT
    elif fen_ch in ['r', 'R']:
        return ROOK
    elif fen_ch in ['c', 'C']:
        return CANNON
    elif fen_ch in ['p', 'P']:
        return PAWN
    else:
        return NONE

def get_char(kind, color):
    if kind is KING:
        return ['K', 'k'][color]
    elif kind is ADVISOR:
        return ['A', 'a'][color]
    elif kind is BISHOP:
        return ['B', 'b'][color]
    elif kind is KNIGHT:
        return ['N', 'n'][color]
    elif kind is ROOK:
        return ['R', 'r'][color]
    elif kind is CANNON:
        return ['C', 'c'][color]
    elif kind is PAWN:
        return ['P', 'p'][color]
    else:
        return ''
        
# 比赛结果
UNKNOWN, RED_WIN, BLACK_WIN, PEACE  =  range(4)
result_str = (u"未知", u"红胜", u"黑胜",  u"平局" ) 

#存储类型
BOOK_UNKNOWN, BOOK_ALL, BOOK_BEGIN, BOOK_MIDDLE, BOOK_END = range(5)
book_type_str = (u"未知", u"全局", u"开局",  u"中局",  u"残局") 

#KING, ADVISOR, BISHOP, KNIGHT, ROOK, CANNON, PAWN
chessman_show_names = \
( 
        (u"帅",u"仕",u"相",u"马",u"车",u"炮",u"兵"),
        (u"将",u"士",u"象",u"马",u"车",u"炮",u"卒")
 )
                    
def get_show_name(kind, side) :
        return chessman_show_names[side][kind]
        
def move_to_str(p_from, p_to):
    
    x, y = p_from 
    x_, y_ = p_to
    
    move_str = ''
    move_str += chr(ord('a') + x)
    move_str += str(y)
    move_str += chr(ord('a') + x_)
    move_str += str(y_)
    
    return move_str

def str_to_move(move_str):
    
    m00 = ord(move_str[0]) - ord('a')
    m01 = int(move_str[1])
    m10 = ord(move_str[2]) - ord('a')
    m11 = int(move_str[3])
    
    return ((m00,m01),(m10, m11))

#-----------------------------------------------------#
class MoveLogItem(object):
    def __init__(self, p_from = None, p_to = None, killed_man = None, fen_before_move = '',  fen_after_move = '',  last_non_killed_fen = '',  last_non_killed_moves = []):
        self.p_from = p_from
        self.p_to = p_to
        self.move_str = move_to_str(p_from, p_to)  if p_from else '' 
        self.killed_man = killed_man
        self.fen_before_move = fen_before_move
        self.fen_after_move = fen_after_move
        self.last_non_killed_fen =  last_non_killed_fen       
        self.last_non_killed_moves = last_non_killed_moves[:]
        
    def fen_for_engine(self) :
        if  self.killed_man or not self.p_from:
            return self.fen_after_move
        else :    
            return self.last_non_killed_fen + " moves " + " ".join(self.last_non_killed_moves)
            
def mirror_moves(moves) :
        changes = {"a":"i", "b":"h", "c":"g", "d":"f", "e":"e", "f":"d", "g":"c", "h":"b", "i":"a" }
        new_moves  = ''
        
        for  ch in moves :
                if  ch in changes :
                        new_moves += changes[ch]
                else :
                        new_moves += ch
        return new_moves



'''
c3d1 f0e0 c4c0 e0e1 f2e2 e1e2 c0e0 f1e1 d3e3 e2f2 e3f3 f2f1 f3f2 f1f2 e0e1 b9c9 (i5i9 e1e9 f2f1 e9i9 f1e1 i9e9 e1f1 e9e0)  d9e9 i5i9 e9e8 c8d8 e8d8 (e8f8 g7f7 \
f8f7 i9f9 f7e7 f9e9)  i9d9 d8e8 d9d1 e1e5 (e1d1 g7g0 d1d0 g0f0 e8f8 f2f1) f5f3 e5e3 d1e1 e3e1 g7g0 e1e0 g0f0 e8f8 f2f1
'''      
 
def has_branchs(move_str) :
        return True if "(" in move_str else False

def get_branch(move_str) :

        first = move_str.find("(")
        last = -1
        deep = 0
        
        for i in range(first+1, len(move_str)):
                if (move_str[i] == ")") :
                        if (deep == 0) :
                                last = i
                                break
                        else :
                                deep -= 1
                elif (move_str[i] == "(") :
                        deep += 1           
        #end for                
        return (first, last)
                        
def branch_split(moves_str) :
       
        move_list = [moves_str]
        
        while True: 
                new_list = []
                for move_item in move_list :
                        if not has_branchs(move_item) :
                                new_list.append(move_item)
                                continue
                        #real logic here
                        
                        first, last =  get_branch(move_item)
                        
                        if last < 0:
                                raise Exception("Match Error")
                        
                        head_moves = move_item[:first].split()
                        branch_moves = move_item[first+1 : last].split()
                        last_moves = move_item[last+1:].split() if (last < len(move_item) -1) else []
                        
                        new_head_moves = head_moves + last_moves
                        new_branch_moves = head_moves[:-1] + branch_moves
                        
                        new_list.append(" ".join(new_head_moves))
                        new_list.append(' '.join(new_branch_moves))
                        
                if len(new_list) == len(move_list):
                        break
                        
                move_list = new_list[:]
                
        return move_list

#-----------------------------------------------------#
if __name__ == '__main__':        
        move_str = 'f3f2 f1f2 e0e1 b9c9 (i5i9 e1e9 f2f1 e9i9 f1e1 i9e9 e1f1 e9e0)  d9e9 i5i9 e8d8 (e8f8 g7f7 f8f7 i9f9 f7e7 f9e9)  i9d9 e1e5 f5f3 '      
        moves = branch_split(move_str)
        for it in moves :
                print it