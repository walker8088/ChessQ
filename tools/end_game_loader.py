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

books = []
for root, dirs, files in os.walk(u"..\\chessbooks\\适情雅趣\\"):
        for file in files :
                file_name = os.path.join(root, file)
                name, ext = os.path.splitext(file)
                
                if ext.lower() not in [".xqf"] :
                        print "PASSED ", file_name
                        continue
                #print root[2:].decode("GB18030").encode("utf-8"),  name.decode("GB18030").encode("utf-8")        
                loader = XQFLoader()
		book = loader.load(file_name)
		if book:
                        #dump_info(book)
                        books.append((name, book["fen_str"]))
                        
                else :
                        print  "ERROR", file_name.encode("utf-8")        
                
with open(u"..\\chessbooks\\适情雅趣.epd", "wb") as f:
        for line in books :
                f.write(line[0].encode("utf-8").strip() + " "+ line[1] + "\r\n")
                