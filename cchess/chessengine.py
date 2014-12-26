# -*- coding: utf-8 -*-

#most code from http://chinesechess.googlecode.com

import time

#-----------------------------------------------------#
class Chess(object):
    def __init__(self,chess_value):
        self.chess_value = chess_value
        
#-----------------------------------------------------#
        
class Board():
    def __init__(self):
        self.TOP = 3
        self.BUTTOM = 12
        self.LEFT = 3
        self.RIGHT = 11
        self.chessList = [];
        self.init_status =  bytearray([0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0, 20, 19, 18, 17, 16, 17, 18, 19, 20,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0, 21,  0,  0,  0,  0,  0, 21,  0,  0,  0,  0,  0,
                             0,  0,  0, 22,  0, 22,  0, 22,  0, 22,  0, 22,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0, 14,  0, 14,  0, 14,  0, 14,  0, 14,  0,  0,  0,  0,
                             0,  0,  0,  0, 13,  0,  0,  0,  0,  0, 13,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0, 12, 11, 10,  9,  8,  9, 10, 11, 12,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  00])
        self.inBoard = bytearray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                        0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                        0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                        0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                        0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                        0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                        0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                        0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                        0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                        0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.inFort = bytearray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.BiShopDelta = (-30,30,-34,34)
        self.AdvisorDelta = (-17, -15, 15, 17)
        self.KingDelta =  (-1,1,-16,16)
        self.KnightDeltaPin = {-31:-16,-33:-16,-18:-1,14:-1,31:16,33:16,18:1,-14:1}
        self.KnightDeltaCheckedPin = {-31:-15,-33:-17,-18:-17,14:15,31:15,33:17,18:17,-14:-15}
        self.__creatChessObjs()   
    def __creatChessObjs(self):       
        for i in range(8):
            self.chessList.append(0)   
        for i in range(8,15):
            chessObj = Chess(i)
            self.chessList.append(chessObj) 
        self.chessList.append(0)         
        for i in range(16,23):
            chessObj = Chess(i)
            self.chessList.append(chessObj) 
    def getChessItem(self,chessValue):
        if(chessValue > 0)and (chessValue < 23) and (chessValue != 15):
            return self.chessList[chessValue]
        else:
            return None 
    def getBishopPin(self,src,dest):
        return (src+dest)/2
    def getKnightPin(self,src,dest):
        return self.KnightDeltaPin.get(dest-src)+src 
    def getKnightCheckedPin(self,src,dest):
        return self.KnightDeltaCheckedPin.get(dest-src)+src  
    def isSameHalf(self,src,dest):
        return ((src ^ dest) & 0x80) == 0; 
    def isSameRow(self,src,dest):
        return ((src ^ dest)& 0xF0) == 0;
    def isSameColum(self,src,dest):
        return ((src ^ dest)& 0x0F) == 0;
    def isCrossRiver(self,dest,player):
        if(player == 0):
            if dest & 0x80 == 0:
                return True
        elif(player == 1):
            if dest & 0x80 == 0x80:
                return True
        return False
        
#-----------------------------------------------------#
 
class BoardPhase():
    def __init__(self,board):
        self.board_status = bytearray(board.init_status) 
        #self.board_status.extend(board.init_status)
        self.player = 0

    def movePiece(self,board,srcPos,desPos):
        print self.player,srcPos,desPos
        value = self.board_status[srcPos]
        self.board_status[srcPos] = 0
        dest_value =  self.board_status[desPos]
        self.board_status[desPos] = value
        if self.isChecked(board):
            self.board_status[srcPos] = self.board_status[desPos]
            self.board_status[desPos] = dest_value
            return 0
        else:
            self.changeSide()
            return srcPos + desPos*256
    def changeSide(self):
        self.player  =  1 -  self.player
    def setSide(self,side):
        self.player =  side
    def getSide(self):
        return self.player
    def isSelfchess(self,chess_value):
        if((chess_value & 8)!= 0) and (self.getSide() == 0):
            return True
        if((chess_value & 16)!= 0) and (self.getSide() == 1):
            return True
        return False
    def isLegalMove(self,chess_value,board,src,dest):
        if self.isSelfchess(chess_value):
            if chess_value == 18 or chess_value == 10: #Bishop
                delta =  dest - src
                if board.inBoard[dest]== 1 and not self.isSelfchess(self.board_status[dest]) and board.isSameHalf(src,dest) and delta in board.BiShopDelta and self.board_status[board.getBishopPin(src,dest)]==0:                    
                    return True 
                return False
            if chess_value == 9 or chess_value == 17: #Advisor
                delta =  dest - src
                if board.inFort[dest] == 1 and not self.isSelfchess(self.board_status[dest]) and delta in board.AdvisorDelta:
                    return True
                return False
            if chess_value == 8 or chess_value == 16: #King
                delta =  dest - src
                if board.inFort[dest] == 1 and not self.isSelfchess(self.board_status[dest]) and delta in board.KingDelta:
                    return True
                return False
            if chess_value == 19 or chess_value == 11: #Knight
                delta =  dest - src
                if board.inBoard[dest] == 1 and not self.isSelfchess(self.board_status[dest]) and delta in board.KnightDeltaPin.keys() and self.board_status[board.getKnightPin(src,dest)]==0:
                    return True
                return False
            if chess_value == 20 or chess_value == 12: #Rook
                pin = 0
                if board.inBoard[dest] != 1 or  self.isSelfchess(self.board_status[dest]): #out side the board or the dest square has a self-side chess
                    return False
                delta =  dest - src
                if board.isSameRow(src,dest):
                    if delta < 0:
                        delta = -1
                    else:
                        delta = 1
                elif board.isSameColum(src,dest):
                    if delta < 0:
                        delta = -16
                    else:
                        delta = 16
                else:
                    return False
                pin =  src + delta
                while(pin != dest and self.board_status[pin] == 0):
                    pin = pin +delta
                if(pin == dest):
                    return True               
                return False
            if chess_value == 21 or chess_value == 13: #Cannon
                pin = 0
                if board.inBoard[dest] != 1: #out side the board
                    return False
                delta =  dest - src
                if board.isSameRow(src,dest):
                    if delta < 0:
                        delta = -1
                    else:
                        delta = 1
                elif board.isSameColum(src,dest):
                    if delta < 0:
                        delta = -16
                    else:
                        delta = 16
                else:
                    return False
                pin =  src + delta
                while(pin != dest and self.board_status[pin] == 0):
                    pin = pin +delta
                if pin == dest: 
                    if self.board_status[pin] == 0:
                        return True
                    else:
                        return False 
                else:
                    if self.board_status[dest] != 0 and not self.isSelfchess(self.board_status[dest]) :
                        pin = pin + delta
                        while(pin != dest and self.board_status[pin] == 0):
                            pin = pin + delta
                        if pin == dest:
                            return True
                        else:
                            return False                   
                return False
            if chess_value == 22 or chess_value == 14: #Pawn
                delta =  dest - src
                if self.isSelfchess(self.board_status[dest]) :
                    return False
                if board.inBoard[dest] == 1:
                    if board.isCrossRiver(dest,self.getSide()) and (delta == -1 or delta == 1):
                        return True
                    else:
                        if self.getSide() == 0 and delta == -16:
                            return True
                        if self.getSide() == 1 and delta == 16:
                            return True
                        return False
                else:  
                    return False                       
        return False
    def isChecked(self,board):
        for src in range(256):
            chess_value = self.board_status[src]
            if (chess_value == 8 or chess_value == 16) and  self.isSelfchess(chess_value):  #find out the self side King
                #Judge if king is checked by Pawn
                if self.getSide()== 0: #if self is Red side
                    for delta in (-1,1,-16):
                        chess_value = self.board_status[src+delta]
                        if chess_value == 22: #enemy Pawn
                            #print "checked by Pawn"
                            return True
                else:  #if self is Black side
                    for delta in (-1,1,16):  #enemy Pawn
                        chess_value = self.board_status[src+delta]
                        if chess_value == 14:
                            #print "checked by Pawn"
                            return True
                #Judge if king is checked by Knight
                for delta in  board.KnightDeltaPin.keys():
                    dest = src + delta
                    chess_value = self.board_status[dest]
                    if (chess_value == 19 or chess_value == 11) and not self.isSelfchess(chess_value) and boardPhase.board_status[board.getKnightCheckedPin(src,dest)] == 0: #enemy knight and no pin
                        #print "checked by Knight"
                        return True 
                #Judge if king is checked by Rook or King
                for delta in board.KingDelta:
                    dest = src + delta
                    while(board.inBoard[dest]==1):
                        chess_value = self.board_status[dest]
                        if(chess_value != 0):
                            if(chess_value == 20 or chess_value == 12 or chess_value == 16 or chess_value == 8) and not self.isSelfchess(chess_value): #enemy Rook or king
                                #print "checked by Rook or king"
                                return True
                            else:
                                break
                        else:
                            dest = dest +delta

                #Judge if king is checked by Canon
                for delta in board.KingDelta:
                    dest = src + delta
                    while(board.inBoard[dest]==1):
                        chess_value = self.board_status[dest]
                        if(chess_value != 0):
                            break                                     
                        else:
                            dest =  dest + delta 
                    dest =  dest + delta
                    while(board.inBoard[dest]==1):
                        chess_value = self.board_status[dest]
                        if(chess_value != 0):
                            if(chess_value == 21 or chess_value == 13) and not self.isSelfchess(chess_value): #enemy Canon
                                #print "chessvalue %d, side %d checked by Canon" %(chess_value,self.getSide())
                                return True
                            else:
                                break
                        else:
                            dest = dest +delta                      
                return False
        return False
    def isDead(self,chessEngine,board):
        moves = []
        movecount = chessEngine.GenerateMoves(self,board,moves)
        if(movecount != 0):
            for move in moves:
                dest_chess_value = chessEngine.move_piece(self,move)
                if not self.isChecked(board):
                    chessEngine.undo_move_piece(self,move,dest_chess_value)
                    return False
                else:
                    chessEngine.undo_move_piece(self,move,dest_chess_value)   
            return True
        return False
        
#-----------------------------------------------------#
        
class ChessEngine():
    def __init__(self):
        self.vRed = 0
        self.vBlack = 0
        self.PawnValue = bytearray([0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  9,  9,  9, 11, 13, 11,  9,  9,  9,  0,  0,  0,  0,
                          0,  0,  0, 19, 24, 34, 42, 44, 42, 34, 24, 19,  0,  0,  0,  0,
                          0,  0,  0, 19, 24, 32, 37, 37, 37, 32, 24, 19,  0,  0,  0,  0,
                          0,  0,  0, 19, 23, 27, 29, 30, 29, 27, 23, 19,  0,  0,  0,  0,
                          0,  0,  0, 14, 18, 20, 27, 29, 27, 20, 18, 14,  0,  0,  0,  0,
                          0,  0,  0,  7,  0, 13,  0, 16,  0, 13,  0,  7,  0,  0,  0,  0,
                          0,  0,  0,  7,  0,  7,  0, 15,  0,  7,  0,  7,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0])
        self.KingValue = bytearray([0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  1,  1,  1,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  2,  2,  2,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0, 11, 15, 11,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0])
        self.AdvisorValue = bytearray([0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0, 20,  0, 20,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0, 23,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0, 20,  0, 20,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0])
        self.BishopValue = bytearray([ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0, 20,  0,  0,  0, 20,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0, 18,  0,  0,  0, 23,  0,  0,  0, 18,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0, 20,  0,  0,  0, 20,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0])
        self.KnightValue = bytearray([0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0, 90, 90, 90, 96, 90, 96, 90, 90, 90,  0,  0,  0,  0,
                          0,  0,  0, 90, 96,103, 97, 94, 97,103, 96, 90,  0,  0,  0,  0,
                          0,  0,  0, 92, 98, 99,103, 99,103, 99, 98, 92,  0,  0,  0,  0,
                          0,  0,  0, 93,108,100,107,100,107,100,108, 93,  0,  0,  0,  0,
                          0,  0,  0, 90,100, 99,103,104,103, 99,100, 90,  0,  0,  0,  0,
                          0,  0,  0, 90, 98,101,102,103,102,101, 98, 90,  0,  0,  0,  0,
                          0,  0,  0, 92, 94, 98, 95, 98, 95, 98, 94, 92,  0,  0,  0,  0,
                          0,  0,  0, 93, 92, 94, 95, 92, 95, 94, 92, 93,  0,  0,  0,  0,
                          0,  0,  0, 85, 90, 92, 93, 78, 93, 92, 90, 85,  0,  0,  0,  0,
                          0,  0,  0, 88, 85, 90, 88, 90, 88, 90, 85, 88,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0])
        self.RookValue = bytearray([0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,206,208,207,213,214,213,207,208,206,  0,  0,  0,  0,
                          0,  0,  0,206,212,209,216,233,216,209,212,206,  0,  0,  0,  0,
                          0,  0,  0,206,208,207,214,216,214,207,208,206,  0,  0,  0,  0,
                          0,  0,  0,206,213,213,216,216,216,213,213,206,  0,  0,  0,  0,
                          0,  0,  0,208,211,211,214,215,214,211,211,208,  0,  0,  0,  0,
                          0,  0,  0,208,212,212,214,215,214,212,212,208,  0,  0,  0,  0,
                          0,  0,  0,204,209,204,212,214,212,204,209,204,  0,  0,  0,  0,
                          0,  0,  0,198,208,204,212,212,212,204,208,198,  0,  0,  0,  0,
                          0,  0,  0,200,208,206,212,200,212,206,208,200,  0,  0,  0,  0,
                          0,  0,  0,194,206,204,212,200,212,204,206,194,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0])
        self.CannonValue = bytearray([0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                            0,  0,  0,100,100, 96, 91, 90, 91, 96,100,100,  0,  0,  0,  0,
                            0,  0,  0, 98, 98, 96, 92, 89, 92, 96, 98, 98,  0,  0,  0,  0,
                            0,  0,  0, 97, 97, 96, 91, 92, 91, 96, 97, 97,  0,  0,  0,  0,
                            0,  0,  0, 96, 99, 99, 98,100, 98, 99, 99, 96,  0,  0,  0,  0,
                            0,  0,  0, 96, 96, 96, 96,100, 96, 96, 96, 96,  0,  0,  0,  0,
                            0,  0,  0, 95, 96, 99, 96,100, 96, 99, 96, 95,  0,  0,  0,  0,
                            0,  0,  0, 96, 96, 96, 96, 96, 96, 96, 96, 96,  0,  0,  0,  0,
                            0,  0,  0, 97, 96,100, 99,101, 99,100, 96, 97,  0,  0,  0,  0,
                            0,  0,  0, 96, 97, 98, 98, 98, 98, 98, 97, 96,  0,  0,  0,  0,
                            0,  0,  0, 96, 96, 97, 99, 99, 99, 97, 96, 96,  0,  0,  0,  0,
                            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0])
        self.ChessValueTable = {0:self.KingValue,1:self.AdvisorValue,2:self.BishopValue,3:self.KnightValue,
                                4:self.RookValue,5:self.CannonValue,6:self.PawnValue}
        self.HistoryTable=[0]*65536
        self.distance = 0
        self.computerMove = 0
        self.MATE_VALUE = 10000
        self.DEPTH_LIMIT = 32
        self.TIME_LIMIT = 1
        self.WIN_VALUE =  self.MATE_VALUE - 100
        return
    def __MOV(self,src,dest):
        return src+dest*256
    def GenerateMoves(self,boardPhase,board,movs):
        moveCount = 0
        for src in range(256):
            chess_value = boardPhase.board_status[src]
            if(boardPhase.isSelfchess(chess_value)):
                if chess_value == 18 or chess_value == 10: #Bishop
                    for delta in board.BiShopDelta:
                        dest = src+delta
                        if boardPhase.isLegalMove(chess_value,board,src,dest):
                            movs.append(self.__MOV(src,dest))
                            moveCount = moveCount + 1
                            #print "Bishop %d move: src %d, dest %d" %(chess_value,src,dest)
                elif chess_value == 9 or chess_value == 17: #Advisor
                    for delta in board.AdvisorDelta:
                        dest = src+delta
                        if boardPhase.isLegalMove(chess_value,board,src,dest):
                            movs.append(self.__MOV(src,dest))
                            moveCount = moveCount + 1
                            #print "Advisor %d move: src %d, dest %d" %(chess_value,src,dest)                    
                elif chess_value == 8 or chess_value == 16: #King
                    for delta in board.KingDelta:
                        dest = src+delta
                        if boardPhase.isLegalMove(chess_value,board,src,dest):
                            movs.append(self.__MOV(src,dest))
                            moveCount = moveCount + 1  
                            #print "King %d move: src %d, dest %d" %(chess_value,src,dest)                 
                elif chess_value == 19 or chess_value == 11: #Knight
                    for delta in board.KnightDeltaPin.keys():
                        dest = src+delta
                        if boardPhase.isLegalMove(chess_value,board,src,dest):
                            movs.append(self.__MOV(src,dest))
                            moveCount = moveCount + 1
                            #print "Knight %d move: src %d, dest %d" %(chess_value,src,dest)                               
                elif chess_value == 20 or chess_value == 12: #Rook
                    for delta in board.KingDelta:
                        dest = src+delta
                        while(board.inBoard[dest]==1):
                            if boardPhase.isLegalMove(chess_value,board,src,dest):
                                movs.append(self.__MOV(src,dest))
                                moveCount = moveCount + 1
                                #print "Rook %d move: src %d, dest %d" %(chess_value,src,dest)   
                            dest = dest + delta
                elif chess_value == 21 or chess_value == 13: #Cannon
                    for delta in board.KingDelta:
                        dest = src+delta
                        while(board.inBoard[dest]==1):
                            if boardPhase.isLegalMove(chess_value,board,src,dest):
                                movs.append(self.__MOV(src,dest))
                                moveCount = moveCount + 1
                                #print "Cannon %d move: src %d, dest %d" %(chess_value,src,dest)   
                            dest = dest + delta                    
                elif chess_value == 22 or chess_value == 14: #Pawn
                    for delta in board.KingDelta:
                        dest = src+delta
                        if boardPhase.isLegalMove(chess_value,board,src,dest):
                            movs.append(self.__MOV(src,dest))
                            moveCount = moveCount + 1 
                            #print "Pawn %d move: src %d, dest %d" %(chess_value,src,dest)                           
        return moveCount
    def __mirrorSquare(self,index):
        return 254 - index
    def __addPiece(self,index,boardPhase,chess_value):
        boardPhase.board_status[index] =  chess_value
        if chess_value < 16:
            self.vRed = self.vRed + self.ChessValueTable[chess_value - 8][index]
        else:
            self.vBlack = self.vBlack + self.ChessValueTable[chess_value - 16][self.__mirrorSquare(index)]
    def __delPiece(self,index,boardPhase,chess_value):
        boardPhase.board_status[index] =  0
        if chess_value < 16:
            self.vRed = self.vRed - self.ChessValueTable[chess_value - 8][index]
        else:
            self.vBlack = self.vBlack - self.ChessValueTable[chess_value - 16][self.__mirrorSquare(index)]   
                 
    def move_piece(self,boardPhase,move):
        src = move%256
        dest = move/256
        dest_chess_value = boardPhase.board_status[dest]
        if dest_chess_value != 0:
            self.__delPiece(dest, boardPhase, boardPhase.board_status[dest])
        self.__addPiece(dest,boardPhase,boardPhase.board_status[src]) #move the piece to new place
        self.__delPiece(src, boardPhase, boardPhase.board_status[src]) # delete the piece in the original place
        return dest_chess_value     #return the dest piece for undo move. even it has no piece in dest, it will still return 0
    
    def undo_move_piece(self,boardPhase,move,dest_chess_value):
        src = move%256
        dest = move/256
        temp = boardPhase.board_status[dest]
        self.__delPiece(dest, boardPhase, temp)
        self.__addPiece(src,boardPhase,temp)
        if dest_chess_value != 0:
            self.__addPiece(dest, boardPhase, dest_chess_value)
            
    def makeMove(self,boardPhase,board,move):
        temp = boardPhase.board_status[move%256]
        dest_chess_value = self.move_piece(boardPhase, move)
        if boardPhase.isChecked(board):
            self.undo_move_piece(boardPhase, move, dest_chess_value)
            return (False,0)
        boardPhase.changeSide()
        self.distance =  self.distance + 1
        #print "Move chess %d, from %d to %d" %(temp,move%256,move/256)
        return (True,dest_chess_value)
        
    def undoMakeMove(self,boardPhase,move,dest_chess_value):
        self.undo_move_piece(boardPhase, move,dest_chess_value)
        self.distance =  self.distance - 1
        boardPhase.changeSide()
                           
    def __alpha_beta_search(self,depth,boardPhase,board,alpha,beta):
        best_move = 0
        best_value = alpha
        isMated =  True
        if(depth <= 0):
            return self.__evaluate(boardPhase)
        movs = []
        movecount = self.GenerateMoves(boardPhase,board,movs)
        if movecount != 0:
            movs.sort(cmp=lambda x,y:cmp(self.HistoryTable[x],self.HistoryTable[y]),reverse=True)
            for move in movs:
                result = self.makeMove(boardPhase,board,move)
                if result[0] == True:
                    isMated = False
                    val = -self.__alpha_beta_search(depth - 1,boardPhase,board,-beta,-alpha)
                    self.undoMakeMove(boardPhase, move, result[1])
                    if val > beta:
                        best_value = val
                        best_move = move
                        break
                    if val >alpha:
                        alpha = val
                        best_value = val
                        best_move = move
            if isMated == True:
                return self.distance - self.MATE_VALUE
            if best_move != 0:
                self.HistoryTable[best_move] += depth * depth;
                if self.distance == 0:
                    self.computerMove = best_move
            return best_value
    def __evaluate(self,boardPhase):
        if boardPhase.getSide == 0:           
            return self.vRed - self.vBlack + 3
        else:
            return self.vBlack - self.vRed + 3
    def __mainSearch(self,boardPhase,board):
        start_time = time.time()
        #for i in range(self.DEPTH_LIMIT):
        #for i in range(self.DEPTH_LIMIT):
        value = self.__alpha_beta_search(4,boardPhase,board,-self.MATE_VALUE, self.MATE_VALUE)
        #if value > self.WIN_VALUE or value < -self.WIN_VALUE:
            #break
        print time.time() - start_time
        
    def getBestMove(self,boardPhase,board):
        self.__mainSearch(boardPhase,board)
        return self.computerMove
        
#-----------------------------------------------------#
chess_man_kind_dict = \
{
        "k" : 8, 
        "a" : 9,
        "b" : 10,
        "n" : 11,
        "r" : 12,
        "c" : 13,
        "p" : 14       
}

def  get_chessman_kind(ch) :
        
        lower_ch = ch.lower()
        
        if lower_ch in chess_man_kind_dict :
                val = chess_man_kind_dict[lower_ch]
                if lower_ch == ch :  #大小写检测
                         val = val +  8                
                return val
        else :
                return None
                
 
#-----------------------------------------------------#

class ChessEngineInterface(object) :
        
        def __init__(self) :
        
                self.board = Board()
                self.boardPhase = BoardPhase(self.board)               
                self.engine =  ChessEngine()
                
        def from_fen(self, fen_str) :
                init_status =  bytearray([0 for x in range(16 * 16)])

                self.fen_str = fen_str
                
                if fen_str == '':
                        return

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
                    elif (ch >= 'A' and ch <= 'Z') or (ch >= 'a' and ch <= 'z') :
                        if x <= 8:
                            chess_man_val = get_chessman_kind(ch)
                            init_status[ (y+3)  * 16 + (x+3) ] = chess_man_val
                            x += 1
                
                self.board.init_status = init_status
                self.boardPhase = BoardPhase(self.board)   
                
                if fen_str[i+1] == 'b':
                     self.boardPhase.player = 1
                else:
                     self.boardPhase.player = 0
                
                '''
                for y in range(16):
                       for x in range(16):
                                print self.boardPhase.board_status [y * 16 + x], " ", 
                       print        
                '''
                
        def get_best_move(self) : 
                if self.boardPhase.isDead(self.engine, self.board):
                        print "Win!"
                        return None
                else:
                        mov = self.engine.getBestMove(self.boardPhase, self.board)
                        
                        v_from = mov % 256
                        v_to =  mov / 256
                        
                        mov_from = ((v_from % 16) - 3,  (v_from / 16) - 3)  
                        mov_to = ((v_to % 16) - 3,  (v_to / 16) - 3)
                        
                        return (mov_from, mov_to)
    
#-----------------------------------------------------#

if __name__ == '__main__':
    inf = ChessEngineInterface()
    fen_str = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C2C4/9/RNBAKABNR b - - 0 1'
    #fen_str = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1'
    inf.from_fen(fen_str)
    print inf.get_best_move()
    