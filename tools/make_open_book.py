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

open_errors = []
result_errors = []
all_moves = {}
repeats = []
good_moves = []

for root, dirs, files in os.walk(u"D:\\05_棋谱\\0_对局整理\\"):
        for file in files :
                file_name = os.path.join(root, file)
                name, ext = os.path.splitext(file)
                
                if ext.lower() not in [".xqf"] :
                        print "PASSED ", file_name
                        continue
                        
                loader = XQFLoader()
		book = loader.load(file_name, True, False)
		if book:
                        if book["fen_str"]  != "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1" :
                                print "ERROR ", file_name,book["fen_str"]
                                open_errors.append("fen error " + file_name)
                                continue
                        
                        if  book["result"] == 0 :
                                print "****** RESULT ERROR ******", file_name
                                result_errors.append(file_name)
                                continue
                        
                        moves  = book["moves"]
                        if not moves :
                                print "ERROR ", file_name
                                open_errors.append("no moves " + file_name)
                                continue
                                
                        moves = moves.strip()        
                        
                        if moves[0] in ['a','b','c','d'] :
                                moves = mirror_moves(moves)
                        
                        if len(moves) <  250 and ( 1 <= book["result"] <= 2) and ((u'超时' in moves) or (u'步时' in moves) or (u'断线' in moves)):
                                print "MOVE TO SHORT", file_name
                                open_errors.append(file_name)
                                open_errors.append(moves)
                                
                                continue
                        
                        if  (u'超时' in moves[-20:]) or (u'步时' in moves[-20:]) or (u'断线' in moves[-20:]):
                                print u"超时", file_name
                                open_errors.append(file_name)
                                open_errors.append(moves)
                                
                                continue
                                
                        if  moves not in all_moves:
                                good_moves.append(moves + " " + str(book["result"]))
                                all_moves[moves] = file_name
                        else :
                                repeats.append(file_name + ":" + all_moves[moves])
                                
                                try:
                                        os.remove(file_name) 
                                except OSError, e:  ## if failed, report it back to the user ##
                                        print ("Error: %s - %s." % (e.filename,e.strerror))        
                                
                        
                        #dump_info(book)        
                else :
                        print  "ERROR", file_name 
                        open_errors.append(file_name) 
                        
        #if len(open_errors) > 5:
        #        break

good_moves.sort()
with open("open_book.txt", "wb") as f:        
        for it in good_moves :
                f.write(it.encode('utf-8') + "\r\n")
        
with open("error.open.txt", "wb") as f:        
        f.write("******************open error*********************\r\n")
        for it in open_errors :
                f.write(it.encode('utf-8') + "\r\n")
        
        f.write("*******************result error*********************\r\n")
        for it in result_errors :
                f.write(it.encode('utf-8') + "\r\n")
        
        f.write("*******************repeated*********************\r\n")
        for it in repeats :
                f.write(it.encode('utf-8') + "\r\n")
                        