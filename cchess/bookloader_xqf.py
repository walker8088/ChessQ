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

import struct

from common import *
from chessboard import *
from chesstree import *

#-----------------------------------------------------#

def xqf_pos_2_board_pos(man_pos) :
        return   ( int(man_pos / 10), 9 - (man_pos % 10) )
        
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
                
        def read_str(self, size, coding = "GBK"):
                buff =  self.__read(size)       
                
                if buff == None :
                        return None
                
                return buff.decode(coding)
        
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
                
                """
                SetKeyBytes(
                        (XQFHead.KeysSum and XQFHead.KeyMask) or XQFHead.KeyOrA,
                        (XQFHead.KeyXY   and XQFHead.KeyMask) or XQFHead.KeyOrB,
                        (XQFHead.KeyXYf  and XQFHead.KeyMask) or XQFHead.KeyOrC,
                        (XQFHead.KeyXYt  and XQFHead.KeyMask) or XQFHead.KeyOrD);
                """
                
                B1 = (HEAD_KeysSum & HEAD_KeyMask) | HEAD_KeyOrA
                B2 = (HEAD_KeyXY  & HEAD_KeyMask) | HEAD_KeyOrB
                B3 = (HEAD_KeyXYf  & HEAD_KeyMask) | HEAD_KeyOrC
                B4 = (HEAD_KeyXYt  & HEAD_KeyMask) | HEAD_KeyOrD
            
                keys.FKeyBytes = (B1, B2, B3, B4)
                keys.F32Keys = bytearray("[(C) Copyright Mr. Dong Shiwei.]")
                for i in range(len(keys.F32Keys)):
                        keys.F32Keys[i] &= keys.FKeyBytes[ i % 4]         
                
		return keys
		
	def init_chess_board(self,  man_str, keys = None):
		
		tmpMan =bytearray([0 for x in range(32)])
		man_buff =bytearray(man_str)
		
		if keys == None:
			for i in range(32) :
				tmpMan[i] = man_buff[i]
			return tmpMan
			
		for i in range(32) :
			ucTmp = man_buff[i]
			nTmp = (keys.KeyXY + i + 1) & 0x8000001F 
			tmpMan[nTmp] = ucTmp

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
		
	def read_steps(self, step_buff, version,  chess_board, keys, parent_node = None):

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
                        
                elif version == 0x12:
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
                        
                        #print "here", ucStep[0],ucStep[1]
                       
                move_from = xqf_pos_2_board_pos(ucStep[0])
                move_to = xqf_pos_2_board_pos(ucStep[1])
                
                if comment_len > 0 :
                        comments = step_buff.read_str(comment_len)
                else:
                        comments = None
                        
                #print "move", move_from, move_to
                fen_before_move = chess_board.get_fen()
                
                if parent_node == None :
                        step_node = LabelNode(u"==开始==", fen_before_move, comments)
                else :         
                        if chess_board.can_make_move(move_from, move_to):
                                move_str = chess_board.std_move_to_chinese_move(move_from, move_to)
                                chess_board.make_step_move(move_from, move_to)
                                chess_board.turn_side()
                                fen_after_move = chess_board.get_fen()
                                step_node = StepNode(move_str, fen_before_move,  fen_after_move, (move_from, move_to), comments)
                        else :
                                print "error on move"
                                return None
                 
                if has_next :
                        new_node = self.read_steps(step_buff, version,  chess_board, keys, step_node)         
                        if new_node :
                                step_node.add_child(new_node)
                
                elif  has_var_step :
                        new_node = self.read_steps(step_buff, version,  chess_board, keys, step_node)
                        if new_node :
                                step_node.add_child(new_node)
                        
                        #new_node = self.read_steps(step_buff, version,  chess_board, keys, step_node)
                        #step_node.add_child(new_node)
                
                return step_node
                
	def load(self, file_name):

		with open(file_name, "rb") as f:
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
                book["title"] = szTitle.decode("GBK")
                book["match"] = szTitle.decode("GBK")
                book["players"] = (szRedPlayerName.decode("GBK"),szBlackPlayerName.decode("GBK"))
                book["result"] = ucRes
                book["narrator"] = szCommenerName.decode("GBK")
                book["author"] = szAuthorName.decode("GBK")
                
                if  (version <= 0x0A) :
                        keys = None
                        chess_mans = self.init_chess_board(ucBoard)
                        step_base_buff =XQFBookBuff(contents[0x400:]) 
                elif (version == 0x12) :
                        keys = self.init_decrypt_key(crypt_keys)
                        chess_mans = self.init_chess_board(ucBoard, keys)	
                        step_base_buff = XQFBookBuff(self.decode_buff(keys, contents[0x400:])) 
		else :
                        raise Exception("version erorr")
		
                chess_board = Chessboard()
                chess_board.move_side = RED
                
                chessman_pos_kinds = \
                        (
                                ROOK,  KNIGHT,  BISHOP,  ADVISOR, KING, ADVISOR,  BISHOP,  KNIGHT, ROOK , \
                                CANNON, CANNON, \
                                PAWN,  PAWN, PAWN,  PAWN, PAWN
                        )
                        
                for side in range(2):
                        for man_index in range(16):
                                man_pos = chess_mans[side * 16 + man_index]
                                if man_pos == 0xFF:
                                        continue
                                pos = xqf_pos_2_board_pos(man_pos)       
                                chess_board.create_chessman(chessman_pos_kinds[man_index], side, pos ) 
                 
                step_node = self.read_steps(step_base_buff,  version,  chess_board,  keys)
		book["steps"] = step_node
		
                return book
                
#-----------------------------------------------------#

if __name__ == '__main__':
		loader = XQFLoader()
		book = loader.load("test\\test.xqf")
		dump_info(book)
                dump_steps(book["steps"])       
                