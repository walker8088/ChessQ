import os
import time
from pathlib import Path

from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#-----------------------------------------------------#
class ThreadRunner(QThread):
    def __init__(self, runner):
        super(QThread, self).__init__()
        self.runner = runner
    
    def run(self):
        self.runner.run()

#-----------------------------------------------------#
class GameKeeper():
    def __init__(self, file):

        self.file = os.path.splitext(file)[0]
        self.games = []
        self.games_done = []
        self.file_eglib = self.file + '.eglib'
        self.file_eplib = self.file + '.eplib'
        self.index = -1
        
    def load(self):

        with open(self.file_eglib, 'rb') as f:
            lines = f.readlines()

        for line in lines:
            it = line.strip().decode('utf-8')
            if it.startswith('#') or  it== '':
                continue
            its = it.split('|')
            if len(its) == 3:
                self.games.append((its[0], its[1], its[2]))
            else:
                self.games.append((its[0], its[1], None))
            
        self.games_done = bytearray(b'0' * len(self.games))

        if os.path.isfile(self.file + '.eplib'):
            with open(self.file_eplib, 'rb') as f:
                done_array = bytearray(open(self.file_eplib, 'rb').read())
            for i, it in enumerate(done_array):
                if i >= len(self.games):
                    break
                if it == ord('1'):
                    self.games_done[i] = it
        self.next_new() 
        self.save_done()
    
    def all(self):
        return zip(self.games, self.games_done)
        
    def curr_game(self):
        if self.index >= 0:
            return self.games[self.index]
        else:
            return None
            
    def curr_game_done(self):
        self.games_done[self.index] = ord('1')
        self.save_done()

    def save_done(self):
        open(self.file_eplib, 'wb').write(bytes(self.games_done))
    
    def next_new(self):
        for i in range(self.index+1, len(self.games)):
            if self.games_done[i] == ord('0'):
                self.index = i
                return self.index
        self.index = 0
        return self.index 
    
    def prev_new(self):
        for i in range(self.index-1, -1, -1):
            if self.games_done[i] == ord('0'):
                self.index = i
                return self.index
        self.index = 0
        return self.index 
    
    def next_game(self):
        self.index = self.index + 1
        if self.index >= len(self.games):
            self.index = len(self.games) - 1
        return self.index
    
    def prev_game(self):
        self.index = self.index - 1
        if self.index <= 0:
            self.index = 0
        return self.index

#-----------------------------------------------------#
class TimerMessageBox(QMessageBox):
    def __init__(self, text, timeout=2):
        super().__init__()
        self.setWindowTitle("ChessQ")
        self.time_to_wait = timeout
        self.setText(text)
        self.setStandardButtons(QMessageBox.NoButton)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.changeContent)
        self.timer.start()

    def changeContent(self):
        self.time_to_wait -= 1
        if self.time_to_wait <= 0:
            self.close()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()

