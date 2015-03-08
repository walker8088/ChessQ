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

file_errors =[]
books = []
files = []
files = [u'D:\\05_棋谱\\0_残局整理\\竹香斋\\野马操田.XQF']
#files = [u'D:\\05_棋谱\\0_残局整理\\隐秀斋象戏谱\\作茧自缚.XQF']
'''
with open("error_file.txt", "rb") as f:
        lines = f.readlines()
        for line in lines :
                files.append(line.strip().decode("utf-8"))
'''                
#try:
for root, dirs, files in os.walk(u"D:\\05_棋谱\\0_残局整理\\适情雅趣550局\\先胜局"):
        for file in files :
                file_name = os.path.join(root, file)
                name, ext = os.path.splitext(file)
                names = name.split()
                name = "_".join(names)
                if ext.lower() not in [".xqf"] :
                        print "PASSED ", file_name
                        continue
                print "processing",  file_name
                loader = XQFLoader()
		book = loader.load(file_name, read_comment = False, read_branch = True)
                if book and book["moves"]:
                        '''
                        try :
                               dump_info(book)
                        except :
                                pass
                        '''        
                        fens = " ".join(book["fen_str"].split()[:2])
                        move_str = book["moves"]
                        moves = branch_split(move_str)[0]               
                        move_len = "%02d" % ((len(moves.split()) +1) // 2)         
                        #chinese_move_str = moves_to_chinese_moves( book["fen_str"], move_str)
                        book_str = " ".join([move_len, name, fens, moves])
                        #book_str = name  + ' ' + fens
                        books.append(book_str)
                        
#except Exception as e:
#        import traceback
#        traceback.print_exc()
        #print  "error", e

#print file_errors
                
#with open("error_file.txt", "wb") as f:
#        for line in file_errors :
#                f.write(line.encode("utf-8").strip() + '\n')

books.sort()
                
with open(u"适情雅趣.qcb", "wb") as f:
        for line in books :
                f.write(line.encode("utf-8").strip() + '\n')   
        