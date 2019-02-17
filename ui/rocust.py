#!/usr/bin/env python3

"""
개념탑개 어학기: Rocust(메뚜기)


<div>Icons made by <a href="https://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" 			    title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" 			    title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>


"""

import os
import re
import sys

import logging
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from IPython import embed
import resources_rc

class Rocust(QDialog):
	def __init__(self, parent=None):
		super(Rocust, self).__init__(parent)
		self.menu_bar = QMenuBar(self)
		self.ui = uic.loadUi("mainwindow.ui", resource_suffix='resources_rc')
		print(dir(self.ui))
		self.ui.show()
		
	


class QApp(QApplication):
	def __init__(self, argv):
		super(Rocust, self).__init__(argv)
	
	def exec(self):
		pass

def execute_app(argv, console=False):
	app = QApplication(argv)
	rocust = Rocust()
	if console:
		embed()
	return app.exec_()

def main(argv):
	# if len(argv) == 1: argv.append('-h')
	## Parser Setting ##
	usage = u"Usage: %prog [options]"
	parser = __import__('optparse').OptionParser(usage)

	## Parser Option ##
	parser.add_option('-d', '--debug', dest='debug', action='store_true', help=u'debugging mode')
	parser.add_option('-c', '--console', dest='console', action='store_true', help=u'concole mode')

	## command logic  ##
	(opt, argv) = parser.parse_args(argv)
	if opt.debug:
	    log_level = logging.DEBUG
	else:
	    log_level = logging.INFO

	logging.basicConfig(format = '%(asctime)s [%(filename)s:%(lineno)s|%(levelname)s] %(funcName)s(): \t %(message)s', level = log_level)
	log = logging.getLogger('root')

	sys.exit(execute_app(argv, opt.console))
	
if __name__ == '__main__':
	main(__import__('sys').argv)
