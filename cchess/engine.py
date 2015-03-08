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

import sys,time

from subprocess import PIPE, Popen
from threading import Thread
from Queue import Queue, Empty

from pubsub import pub

from common import *

#-----------------------------------------------------#

#Engine status   
(BOOTING, READY, WAITING, INFO_MOVE, MOVE, DEAD, UNKNOWN, BOARD_RESET) = range(8)
    
ON_POSIX = 'posix' in sys.builtin_module_names

#-----------------------------------------------------#

class UcciEngine(Thread):
    def __init__(self, name = ''):
        super(UcciEngine, self).__init__()
        
        self.engine_name = name
        
        self.daemon  = True
        self.running = False
        
        self.engine_status = None
        self.ids = []
        self.options = []
        
        self.last_fen_str = None
        self.move_queue = Queue()
        self.move_info_queue = Queue()
        
        pub.subscribe(self.on_game_inited, "game_inited")
        pub.subscribe(self.on_game_started, "game_started")
        pub.subscribe(self.on_game_step_moved, "game_reshow")
        pub.subscribe(self.on_game_step_moved, "game_step_moved")
        pub.subscribe(self.on_game_step_moved_undo, "game_step_moved_undo")
        
        self.search_depth = 8
    
    def on_game_inited(self, move_log) :
        self.init_fen = move_log.fen_after_move
        self.last_fen_str = move_log.fen_after_move
        self.send_cmd("setoption newgame")
        
    def on_game_started(self, move_side) :
        self.move_side = move_side
        self.go_from(self.init_fen)
       
    def on_game_step_moved(self, move_log) :
        self.move_side = move_log.next_move_side()
        self.last_fen_str = move_log.fen_after_move
        self.go_from(move_log.fen_for_engine())
    
    def on_game_step_moved_undo(self, steps, move_log, next_move_side) :
        self.move_side = next_move_side
        self.last_fen_str = move_log.fen_after_move
        self.go_from(move_log.fen_for_engine())

    def run(self) :
        
        self.running = True
        
        while self.running :
            output = self.pout.readline().strip()
            self.engine_out_queque.put(output)
            
    def handle_msg_once(self) :
        try:  
            output = self.engine_out_queque.get_nowait()
        except Empty:
            return 
    
        if output in ['bye','']: #stop pipe
            self.pipe.terminate()
            return False
            
        self.__handle_engine_out_line(output)
        
        return True
    
    def load(self, engine_path):
    
        self.engine_name = engine_path
        
        try:
            self.pipe = Popen(self.engine_name, stdin=PIPE, stdout=PIPE)#, close_fds=ON_POSIX)
        except OSError:
            return False
            
        time.sleep(0.5)
        
        (self.pin, self.pout) = (self.pipe.stdin,self.pipe.stdout)
        
        self.engine_out_queque = Queue()
        
        self.enging_status = BOOTING
        self.send_cmd("ucci")
        
        self.start()
        
        while self.enging_status ==  BOOTING :
            self.handle_msg_once()
            
        return True
        
    def quit(self):
        
        self.send_cmd("quit")
        
        time.sleep(0.2)
            
    def go_from(self, fen_for_engine):
        
        while True:
            try:  
                output = self.engine_out_queque.get_nowait()
            except Empty:
                break 
                
        cmds = 'position fen ' + fen_for_engine
       
        self.send_cmd(cmds)
        
        #if ban_move :
        #        self.send_cmd('banmoves ' + ban_move)
        
        self.send_cmd('go depth ' + str(self.search_depth))
        
    def send_cmd(self, cmd_str) :
        
        #print ">>>", cmd_str
        
        try :
            self.pin.write(cmd_str + "\n")
            self.pin.flush()
    
        except IOError as e :
            print "error in send cmd", e
                
    def __handle_engine_out_line(self, output) :
                
        #print "<<<", output
        
        outputs_list = output.split()
        resp_id = outputs_list[0]
        
        if self.enging_status == BOOTING:
            if resp_id == "id" :
                    self.ids.append(output)
            elif resp_id == "option" :
                    self.options.append(output)
            if resp_id == "ucciok" :
                    self.enging_status = READY
    
        elif self.enging_status == READY:
            
            if resp_id == 'nobestmove':         
                pub.sendMessage("side_dead", dead_side = self.move_side)
                
            elif resp_id == 'bestmove':
                if outputs_list[1].lower() == 'null':
                    pub.sendMessage("side_dead", dead_side = self.move_side)
                    
                else :  
                    move_str = output[9:13]
                    poss = str_to_move(move_str)
                    pub.sendMessage("engine_best_move",  from_engine = self, from_pos = poss[0] , to_pos = poss[1])
                    
            elif resp_id == 'info':
                #info depth 6 score 4 pv b0c2 b9c7 c3c4 h9i7 c2d4 h7e7
                if outputs_list[1] == "depth":
                    move_info = {}    
                    info_list = output[5:].split()
                    
                    if len(info_list) < 5:
                        return
                        
                    move_info["fen_str"] = self.last_fen_str
                    move_info[info_list[0]] =  info_list[1] #depth 6
                    move_info[info_list[2]] =  info_list[3] #score 4
                    
                    move_steps = []
                    for step_str in info_list[5:] :
                        move= str_to_move(step_str)
                        move_steps.append(move)    
                    move_info["moves"] = move_steps    
                    
                    pub.sendMessage("engine_move_info",  move_info  =move_info)
                                        
#-----------------------------------------------------#

if __name__ == '__main__':
    engine = UcciEngine()
    engine.load("..\\engine\\harmless\\harmless")
    time.sleep(1)
    engine.start_game()
    engine.quit()
    time.sleep(1)
    #print engine.ids
    #print engine.options       
        
