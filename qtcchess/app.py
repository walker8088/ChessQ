#!/usr/bin/env python
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

import sys, yaml

from PyQt5 import *
from PyQt5.QtWidgets import QApplication

from .QtCChessMain import *

#-----------------------------------------------------#
class QChessApp(QApplication):
    def __init__(self):
        super().__init__([])
        
        self.config = None
        
        self.mainWin = MainWindow(self)
        self.mainWin.show()
        
    def loadConfig(self):
        with open(APP_CONFIG_FILE) as f:
            try:
                self.config = yaml.load(f, Loader=yaml.FullLoader)
            except Exception as e:
                QMessageBox.warning(self, APP_NAME,
                                    APP_CONFIG_FILE + " 配置文件错误：" + str(e))
                self.config = None
                return
 
        

#-----------------------------------------------------#
def run():
    app = QChessApp()
    sys.exit(app.exec_())
    