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


import time

from pubsub import pub

from common import *
from engine import *

#-----------------------------------------------------#

class ChessTable(object):
    def __init__(self, parent, board) :
        self.parent =  parent
        self.board = board
        self.players = [None,None]
        self.history = []

        self.running = False
    
    def set_players(self, players):
        self.players = players
        
        self.players[RED].side = RED
        self.players[BLACK].side = BLACK
        
    def new_game(self, fen_str = None) :
    
        self.board.init_board(fen_str)
        
        self.history = []
        self.last_non_killed_fen = self.board.get_fen()         
        self.last_non_killed_moves = []
        
        move_log = MoveLogItem(fen_after_move =  self.board.get_fen(), last_non_killed_fen = self.last_non_killed_fen,  last_non_killed_moves = self.last_non_killed_moves)
        self.history.append(move_log)
        
    def start_game(self):
        
        self.running = True     
        
        self.players[RED].start_game()
        self.players[BLACK].start_game()
        
        self.players[self.board.move_side].ready_to_move()
        
    def stop_game(self):
        
        self.running = False    
        self.players[RED].stop_game()
        self.players[BLACK].stop_game()
    
    def undo_move(self):
        
        #需要返回前两步才对   
        if len(self.history) > 1:
            self.history.pop()
        
        if len(self.history) > 1:
            self.history.pop()
            
        print len(self.history)
        
        move_log = self.history[-1]
        
        self.board.init_board(move_log.fen_after_move)
        
        self.last_non_killed_fen = move_log.last_non_killed_fen         
        self.last_non_killed_moves = move_log.last_non_killed_moves[:]
        
        print  "undo to", self.last_non_killed_fen, self.last_non_killed_moves
        
        self.players[self.board.move_side].ready_to_move()    
                
    def handle_player_msg(self) :
        
        if not self.running:    
            return
            
        move_result = self.players[self.board.move_side].get_next_move() 
        
        if not move_result:
            return
        
        (result, move_event) = move_result
        
        if result == MOVE :
            p_from, p_to = move_event
            #print "chesstable got next move",  p_from, p_to
            
            if not self.board.can_make_move(p_from, p_to) :
                print "chesstable move check error", p_from, p_to
                return
            
            fen_str = self.board.get_fen() 
            move_str_zh = self.board.std_move_to_chinese_move(p_from, p_to) 
            move_log = self.board.make_log_step_move(p_from, p_to) 
            
            self.board.turn_side()
            
            move_log.fen_after_move =  self.board.get_fen()
            move_log.move_str_zh = move_str_zh
            
            if  move_log.killed_man :
                self.last_non_killed_fen = self.board.get_fen()         
                self.last_non_killed_moves = []
            else :
                self.last_non_killed_moves.append(move_log.move_str)
                
            move_log.last_non_killed_fen = self.last_non_killed_fen
            move_log.last_non_killed_moves = self.last_non_killed_moves[:]
            move_log.step_no = len(self.history) + 1
            #print  "move_log", self.last_non_killed_fen,self.last_non_killed_moves
            self.history.append(move_log)
            
            #self.parent.notify_move_from_table(move_log)
            pub.sendMessage('step_move', move_log = move_log)
            
            self.players[self.board.move_side].ready_to_move()
        
        elif result == DEAD:
            self.over = True
            self.over_side = self.board.move_side
            
            self.parent.on_game_over(self.over_side)
        
