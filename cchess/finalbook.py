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

#-----------------------------------------------------#
class EndGameItem(object) :
        def __init__(self, level, name, fen,  moves) :
                self.level = level
                self.name = name
                self.fen = fen
                self.moves = moves
                self.done = False
                
#-----------------------------------------------------#

class FinalBook(object):
    def __init__(self):
        self.books = []
        self.index = -1
            
    def load_from_qcb(self, qcb_file):
        self.books = []
        with open(qcb_file) as f:
            lines = f.readlines()
        for line in lines:
            items = line.strip().decode("utf-8").split(" ")
            fen = " ".join(items[2:4])
            moves = " ".join(items[4:])
            it = EndGameItem(int(items[0]), items[1], fen, items[5])
            self.books.append(it)
        self.index = 0
    
    def load_from_qcd(self, qcd_file):
        self.books = []
        with open(qcd_file) as f:
            lines = f.readlines()
         
        index = 1   
        for line in lines:
            items = line.strip().decode("utf-8").split(" ")
            fen = " ".join(items[1:4])
            moves = " ".join(items[4:])
            name = u"第 %d 局" % index 
            it = EndGameItem(int(items[0]),  name, fen, moves)
            self.books.append(it)
            index += 1
        self.index = 30
         
    def  curr_book(self):
        return self.books[self.index]
    
    def next_book(self):
        self.index += 1
        return self.books[self.index]
    
