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

import os
import struct, copy

from common import *
from chessboard import *

#-----------------------------------------------------#

def decode_pos(man_pos) :
        return (int(man_pos / 10), 9 - (man_pos % 10)) 
            
#-----------------------------------------------------#
        
class XQFKey(object) :
	def __init__(self):
		pass
                
#-----------------------------------------------------#

class XQFBookBuff(object) :
	def __init__(self, buffer):
                self.buffer = buffer
                self.index = 0
                self.length = len(buffer)
                
        def __read(self, size):
                if self.index + size > self.length:
                        return None
        
                start = self.index
                stop = self.index + size
                self.index += size
                return self.buffer[start:stop] 
                
        def read_str(self, size, coding = "GB18030"):
                buff =  self.__read(size)       
                
                if buff == None :
                        return None
                
                try:
                        ret = buff.decode(coding)
                except:
                        ret = None
                
                return ret
                
        def read_bytes(self,  size):
                buff =  self.__read(size)       
                
                if buff == None :
                        return None
                
                return bytearray(buff)
        
        def read_int(self):
                bytes =  self.read_bytes(4)       
                
                if bytes == None :
                        return None
                        
                return  bytes[0] + (bytes[1] << 8) + (bytes[2] << 16) + (bytes[3] << 24) 

#-----------------------------------------------------#

class XQFLoader(object):
	def __init__(self):	
			pass
	
	def init_decrypt_key(self, buff_str):
		
                keys = XQFKey()
		
		key_buff =bytearray(buff_str)
		
                # Pascal code here from XQFRW.pas
                # KeyMask   : dTByte;                         // 加密掩码
                # ProductId : dTDWord;                        // 产品号(厂商的产品号)
                # KeyOrA    : dTByte;
                # KeyOrB    : dTByte;
                # KeyOrC    : dTByte;
                # KeyOrD    : dTByte;
                # KeysSum   : dTByte;                         // 加密的钥匙和
                # KeyXY     : dTByte;                         // 棋子布局位置钥匙       
                # KeyXYf    : dTByte;                         // 棋谱起点钥匙
                # KeyXYt    : dTByte;                         // 棋谱终点钥匙
                
                HEAD_KeyMask, HEAD_ProductId, \
                HEAD_KeyOrA, HEAD_KeyOrB, HEAD_KeyOrC, HEAD_KeyOrD, \
                HEAD_KeysSum, HEAD_KeyXY, HEAD_KeyXYf, HEAD_KeyXYt = struct.unpack("<BIBBBBBBBB", buff_str)
                
                """ 
                #以下是密码计算公式
                bKey       := XQFHead.KeyXY;
                KeyXY      := (((((bKey*bKey)*3+9)*3+8)*2+1)*3+8) * bKey;
                bKey       := XQFHead.KeyXYf;
                KeyXYf     := (((((bKey*bKey)*3+9)*3+8)*2+1)*3+8) * KeyXY;
                bKey       := XQFHead.KeyXYt;
                KeyXYt     := (((((bKey*bKey)*3+9)*3+8)*2+1)*3+8) * KeyXYf;
                wKey       := (XQFHead.KeysSum) * 256 + XQFHead.KeyXY;
                KeyRMKSize := (wKey mod 32000) + 767;
                """
                
                #pascal code
                #bKey       := XQFHead.KeyXY;
                #KeyXY      := (((((bKey*bKey)*3+9)*3+8)*2+1)*3+8) * bKey;
                bKey = HEAD_KeyXY
                #棋子32个位置加密因子
                keys.KeyXY = ((((((bKey*bKey)*3+9)*3+8)*2+1)*3+8) * bKey) & 0xFF
                
                #棋谱加密因子(起点)
                #pascal code
                #bKey       := XQFHead.KeyXYf;
                #KeyXYf     := (((((bKey*bKey)*3+9)*3+8)*2+1)*3+8) * KeyXY;
                bKey = HEAD_KeyXYf
                keys.KeyXYf  = ((((((bKey*bKey)*3+9)*3+8)*2+1)*3+8) * keys.KeyXY) & 0xFF
                
                #棋谱加密因子(终点)
                #pascal code 
                #bKey       := XQFHead.KeyXYt;
                #KeyXYt     := (((((bKey*bKey)*3+9)*3+8)*2+1)*3+8) * KeyXYf;
                bKey  = HEAD_KeyXYt
                keys.KeyXYt  = ((((((bKey*bKey)*3+9)*3+8)*2+1)*3+8) * keys.KeyXYf) & 0xFF
                
                #注解大小加密因子
                #pascal code 
                #wKey       := (XQFHead.KeysSum) * 256 + XQFHead.KeyXY;
                #KeyRMKSize := (wKey mod 32000) + 767;
                wKey = HEAD_KeysSum * 256 + HEAD_KeyXY
                keys.KeyRMKSize = ((wKey % 32000) + 767)  & 0xFFFF
                
                B1 = (HEAD_KeysSum & HEAD_KeyMask) | HEAD_KeyOrA
                B2 = (HEAD_KeyXY  & HEAD_KeyMask) | HEAD_KeyOrB
                B3 = (HEAD_KeyXYf  & HEAD_KeyMask) | HEAD_KeyOrC
                B4 = (HEAD_KeyXYt  & HEAD_KeyMask) | HEAD_KeyOrD
            
                keys.FKeyBytes = (B1, B2, B3, B4)
                keys.F32Keys = bytearray("[(C) Copyright Mr. Dong Shiwei.]")
                for i in range(len(keys.F32Keys)):
                        keys.F32Keys[i] &= keys.FKeyBytes[ i % 4]         
                
		return keys
		
	def init_chess_board(self,  man_str, version, keys = None):
		
		tmpMan =bytearray([0 for x in range(32)])
		man_buff =bytearray(man_str)
		
		if keys == None:
			for i in range(32) :
				tmpMan[i] = man_buff[i]
			return tmpMan
			
		for i in range(32) :
			if version >= 12:
                                tmpMan[(keys.KeyXY + i + 1) & 0x1F] =  man_buff[i]
                        else :
                                  tmpMan[i] =  man_buff[i]
                                  
		for i in range(32) :
			tmpMan[i] = (tmpMan[i] - keys.KeyXY) & 0xFF
			if (tmpMan[i] > 89) :
				tmpMan[i] = 0xFF
     
		return tmpMan
	
	def decode_buff(self, keys, buff) : 
		
                nPos = 0x400
                de_buff =bytearray(buff)
                
                for i in range(len(buff)) :
                        KeyByte = keys.F32Keys[(nPos + i) % 32]
			de_buff[i] = (de_buff[i] - KeyByte) & 0xFF
		
                return str(de_buff)
	
        def read_step_0(self, step_buff,  version,  read_comment,  keys):
                
                ucStep = step_buff.read_bytes(4)
                        
                if ucStep == None :
			return None
                        
		comment_len = 0
                
                if version <= 0x0A:
                        #低版本在走子数据后紧跟着注释长度，长度为0则没有注释
                        comment_len = step_buff.read_int()
                        
                else: # version == 0x12:
                        #高版本通过flag来标记有没有注释，有则紧跟着注释长度和注释字段
                        ucStep[2] &= 0xE0
                        if (ucStep[2] & 0x20) : #有注释
                                comment_len = step_buff.read_int() - keys.KeyRMKSize
                
                move_str = ''
                
                if  (comment_len > 0) :
                        comments = step_buff.read_str(comment_len)
                        #print comments
                        if read_comment :
                                comments = comments.strip()
                                comments.replace("{", u"（")
                                comments.replace("}", u"）")
                                move_str += ' { ' + comments + " }"  
                                
                return move_str
        	
	def read_steps(self, step_buff, version,  chess_board, read_comment, read_branch, step_no, keys, parent_node = None):
                
                board_bak = copy.deepcopy(chess_board)
                
                ucStep = step_buff.read_bytes(4)
                        
                if ucStep == None :
			return None
                        
		comment_len = 0
                has_next = False
                has_var_step = False
                
                if version <= 0x0A:
                        #低版本在走子数据后紧跟着注释长度，长度为0则没有注释
                        if (ucStep[2] & 0xF0) :
                               has_next = True
                        if (ucStep[2] & 0xF) :
                               has_var_step = True #有变着
                        comment_len = step_buff.read_int()
                        
                        ucStep[0] = (ucStep[0] - 0x18) & 0xFF;
                        ucStep[1] = (ucStep[1] - 0x20) & 0xFF;
                        
                else : #if version == 0x12:
                        #高版本通过flag来标记有没有注释，有则紧跟着注释长度和注释字段
                        ucStep[2] &= 0xE0
                        if (ucStep[2] & 0x80) :  #有后续
                                has_next = True
                        if (ucStep[2] & 0x40) :  #有变招
                                has_var_step = True
                        if (ucStep[2] & 0x20) : #有注释
                                comment_len = step_buff.read_int() - keys.KeyRMKSize
                                 
                        ucStep[0] = (ucStep[0] - 0x18 - keys.KeyXYf) & 0xFF
                        ucStep[1] = (ucStep[1] - 0x20 - keys.KeyXYt) & 0xFF
                       
                move_from = decode_pos(ucStep[0])
                move_to = decode_pos(ucStep[1])
                
                if comment_len > 0 :
                        comments = step_buff.read_str(comment_len)
                else:
                        comments = None
                        
                if chess_board.can_make_move(move_from, move_to, color_limit = False) :
                        chess_board.make_step_move(move_from, move_to, color_limit = False)
                        #chess_board.turn_side()
                        move_str = move_to_str(move_from, move_to)
                else :
                        print "bad move at", step_no
                        return  parent_node + " " + "BAD_MOVE"
                        
                step_node = parent_node + " " + move_str
                
                if read_comment and (comments > 0) :
                        comments = comments.strip()
                        comments.replace("{", u"（")
                        comments.replace("}", u"）")
                        step_node += ' {' + comments.strip() + "} "
                
                if has_next :
                        var_index = len(step_node)
                        next_node = self.read_steps(step_buff, version,  chess_board, read_comment, read_branch, step_no + 1, keys, step_node)    
                        step_node = next_node
                else  :
                        next_node = None
                
                if  has_var_step :
                        new_node = self.read_steps(step_buff, version,  board_bak,  read_comment, read_branch, step_no + 1, keys,  "")
                        if read_branch :
                                if next_node :
                                        step_node = step_node[ :var_index] +  " (" + new_node.strip() + ") "  + step_node[var_index:]
                                else :
                                        step_node = step_node +  " (" + new_node.strip() + ")"
                
                return step_node
                
	def load(self, full_file_name, read_comment = True, read_branch = True):

		with open(full_file_name, "rb") as f:
			contents = f.read()
		
		magic, version,  crypt_keys, ucBoard,\
		ucUn2, ucRes,\
		ucUn3, ucType,\
		ucUn4, ucTitleLen,szTitle,\
		ucUn5, ucMatchNameLen,szMatchName,\
		ucDateLen, szDate,\
		ucAddrLen, szAddr,\
		ucRedPlayerNameLen, szRedPlayerName,\
		ucBlackPlayerNameLen,szBlackPlayerName,\
		ucTimeRuleLen,szTimeRule,\
		ucRedTimeLen,szRedTime,\
		ucBlackTime,szBlackTime, \
		ucUn6,\
		ucCommenerNameLen,szCommenerName,ucAuthorNameLen,szAuthorName,\
		ucUn7 = struct.unpack("<2sB13s32s3sB12sB15sB63s64sB63sB15sB15sB15sB15sB63sB15sB15s32sB15sB15s528s",  contents[:0x400])
		
		if magic != "XQ":
			return None
		
                book = {}
                book["source"] = "XQF"
                book["version"] = version
                book["book_type"] =  ucType + 1
                book["result"] = ucRes
                
                try :
                        book["players"] = (szRedPlayerName[:ucRedPlayerNameLen].decode("GB18030"),szBlackPlayerName[ucBlackPlayerNameLen].decode("GB18030"))
                except : 
                        book["players"] = ('','')
                try :
                        book["title"] = szTitle[:ucTitleLen].decode("GB18030")
                except:
                        book["title"] = ''
                try :
                        book["match"] = szMatchName[:ucMatchNameLen].decode("GB18030")
                except :
                        book["match"] = ''
                try :        
                        book["narrator"] = szCommenerName[ucCommenerNameLen].decode("GB18030")
                except:
                        book["narrator"] = ''
                try :        
                        book["author"] = szAuthorName[:ucAuthorNameLen].decode("GB18030")
                except:
                        book["author"] = ''
                
                path, file_name=os.path.split(full_file_name)
                
                if book["result"] == 0 :
                        if (u"先胜" in file_name) and (u"先和" not in file_name) and (u"先负" not in file_name) :
                                book["result"] = 1
                        elif (u"先负" in file_name) and (u"先和" not in file_name) and (u"先胜" not in file_name) :
                                book["result"] = 2
                        elif (u"先和" in file_name) and (u"先负" not in file_name) and (u"先胜" not in file_name) :
                                book["result"] = 3
                
                if book["result"] == 0 :        
                        if (u"胜" in file_name) and (u"负" not in file_name) :
                                book["result"] = 1
                        elif (u"负" in file_name) and (u"胜" not in file_name) :
                                book["result"] = 2
                        elif (u"和" in file_name) and (u"负" not in file_name) and (u"胜" not in file_name) :
                                book["result"] = 3
                                
                if  (version <= 0x0A) :
                        keys = None
                        chess_mans = self.init_chess_board(ucBoard, version)
                        step_base_buff =XQFBookBuff(contents[0x400:]) 
                if  (version == 0x0B) :
                        keys = self.init_decrypt_key(crypt_keys)
                        chess_mans = self.init_chess_board(ucBoard, version, keys)
                        step_base_buff = XQFBookBuff(self.decode_buff(keys, contents[0x400:]))
                else  :
                        keys = self.init_decrypt_key(crypt_keys)
                        chess_mans = self.init_chess_board(ucBoard, version, keys)	
                        step_base_buff = XQFBookBuff(self.decode_buff(keys, contents[0x400:])) 
		
                chess_board = Chessboard()
                
                chessman_kinds = \
                        (
                                'R',  'N',  'B',  'A', 'K', 'A',  'B',  'N', 'R' , \
                                'C', 'C', \
                                'P','P','P','P','P'  
                        )
                
                for side in range(2):
                        for man_index in range(16):
                                man_pos = chess_mans[side * 16 + man_index]
                                if man_pos == 0xFF:
                                        continue
                                pos = decode_pos(man_pos)  
                                fen_ch = chr(ord(chessman_kinds[man_index]) +side * 32)
                                chess_board.create_chessman(get_kind(fen_ch), side, pos)
                                
                chess_board.move_side = RED
                book['fen_str'] = chess_board.get_fen()
                moves_str = self.read_step_0(step_base_buff,  version,  read_comment, keys)
                moves_str = self.read_steps(step_base_buff,  version,  chess_board,  read_comment, read_branch, 1, keys,  moves_str)
		book["moves"] = moves_str  #branch_split(moves_str) if moves_str else []
		
                return book
                
#-----------------------------------------------------#
if __name__ == '__main__':

		loader = XQFLoader()
		book = loader.load(u"D:\\05_棋谱\\- 黑龙江赵国荣 (和) 广东许银川 (1998.12.10于深圳).xqf")
		dump_info(book)
                moves = book["moves"]       
                mirror = mirror_moves(moves)
                print moves
                print mirror