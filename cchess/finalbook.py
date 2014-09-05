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

class FinalBook(object):
    def __init__(self, epd_file):
        self.books = []
        self.load_from_epd(epd_file)
        self.index = 0
            
    def load_from_epd(self, epd_file):
        with open(epd_file) as f:
            lines = f.readlines()
        for line in lines:
            items = line.strip().split(";")
            self.books.append((items[1].decode("utf-8"), items[0]))
        
    def  curr_book(self):
        return self.books[self.index]
    
    def next_book(self):
        self.index += 1
        return self.books[self.index]
    
