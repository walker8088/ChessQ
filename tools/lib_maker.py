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

import sys, os
import shutil

from cchess import *


def load_board(root_path):
    games = []
    files = os.listdir(root_path)
    for file in files:
        game_info = {}
        ext = os.path.splitext(file)[1].lower()
        if ext != '.xqf':
            continue
        file_name = os.path.join(root_path, file)
        
        game = read_from_xqf(file_name)
        if game.init_board.move_side == BLACK:
            game.swap()
            game.flip()
            game.mirror()
            print(file)
            print(game.dump_chinese_moves())
        game_info['name'] = file[:-4]
        game_info['result'] = game.info["result"]
        game_info['fen'] = game.init_board.to_fen()
        game_info['moves'] = game.dump_iccs_moves()
        
        max_len = 0
        for move in game.dump_moves():
            if len(move) > max_len:
                max_len = len(move)
        game_info['len'] = max_len
        #print(game_info)
        games.append(game_info)

    #games.sort(key=lambda x: x['len'])
    return games


#collection_name = '象棋残局杀势.eglib'
#collection_dir = '..\\gamebooks\\象棋残局杀势'

collection_name = '车马专集.eglib'
collection_dir = '..\\gamebooks\\车马专集'

with open(collection_name, 'wb') as f:
    for game in load_board(collection_dir):
        #if u"红胜" not in game['name']:
        #        continue
        #if "1-0" not in game['result']:
        #    continue

        moves = game['moves']
        moves.sort(key=lambda x: len(x))
        for move in moves:
            f.write(f"{game['name']}|{game['fen']}|{','.join(move)}\n".encode('utf-8'))
