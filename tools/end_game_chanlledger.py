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

sys.path.append("..\\")

from cchess import *

#-----------------------------------------------------#
def load_from_qcb(qcb_file):
        with open(qcb_file) as f:
            lines = f.readlines()
        
        books = []
        
        for line in lines:
            if line.startswith("**") :
                continue
            items = line.strip()
            books.append(items)
        
        return books
        
def  chanlledge_end_game(book_fen, engine) :
        print "doing", book_fen
        board  = Chessboard()
        board.init_board(book_fen)
        engine.start_game()
        
        moves = []
        last_moves = []
        last_fen = board.get_fen()
        
        running = True
        ok = False
        
        while running : 
   
                if len(last_moves) == 0:
                    move_history = None
                    engine_fen =  last_fen 
                else :
                    move_history = ' '.join(last_moves)
                    engine_fen =  last_fen + " moves " + move_history 
                
                engine.go_from(engine_fen, last_fen)
                
                waiting = True
                while waiting : 
                        if len(moves) > 100:
                                running = False
                                engine.stop_game()
                                print
                                break        
                        if engine.move_queue.qsize() == 0:
                                time.sleep(0.05)
                                continue
                        
                        msg = engine.move_queue.get_nowait()
                        
                        if msg  == None :
                                continue       
                                
                        elif msg[0] == MOVE :
                                move_from, move_to = msg[1]
                                if board.can_make_move(move_from, move_to):
                                        
                                        if board.at_pos(move_to[0], move_to[1]) != None :
                                                killed_man = True
                                        else :
                                                killed_man = False
                                        
                                        print board.std_move_to_chinese_move(move_from, move_to),
                                        
                                        board.make_step_move(move_from, move_to)
                                        board.turn_side()
                                        
                                        if killed_man :
                                                last_moves = []
                                                last_fen = board.get_fen()
                                        else :
                                                last_moves.append(move_to_str(move_from, move_to))
                                        
                                        moves.append(move_to_str(move_from, move_to))
                                        
                                        
                                        break 
                                else :
                                        print "error on move", msg 
                                        running = False
                                        break
                                        
                        elif msg[0] == DEAD :
                                if board.move_side is BLACK:
                                        print u"挑战成功"
                                        ok = True
                                else :
                                        print u"挑战失败"
                                running = False
                                break
                #end while waiting                 
        #end while running
        if ok :
                return moves
        else :
                return None
                
#-----------------------------------------------------#
if __name__ == '__main__':
    
    books = load_from_qcb(u"end_games.qcb")
    
    engine = UcciEngine()
    engine.load("..\\engines\\eleeye\\eleeye")
    time.sleep(1)
    
    ok_games = []
    bad_games = []
    for book in books[:]  :
        items = book.split()
        book_fen = " ".join(items[0:2])
        moves = chanlledge_end_game(book_fen, engine)
        if moves :
                end_game_str = "%02d  %s %s moves %s" % ( (len(moves)+1)/2, items[0], items[1], ' '.join(moves))
                ok_games.append(end_game_str)
                print  end_game_str      
        else :
                bad_games.append(book)
                
    engine.quit()
    
    ok_games.sort() 
    #print ok_games
    
    with open(u"end_games_good.qcb", "wb") as f:
        for line in bad_games :
                f.write(line + "\n")
    
        for line in ok_games :
                f.write(line + "\n")
                