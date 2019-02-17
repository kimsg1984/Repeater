#!/usr/bin/env python3

"""
개념탑개 어학기: Rocust(메뚜기)

[아이콘1]
<div>Icons made by <a href="https://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" 			    title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" 			    title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>


[아이콘2]
---
Metrize Icons
by Alessio Atzeni

http://alessioatzeni.com/metrize-icons/
https://twitter.com/Bluxart
http://dribbble.com/Bluxart
---

Collection of 300 Metro-Style Icons for designers and developers.

The icon set are available in:

PSD (Single Shape Layer)
SVG (Single Icon 512 x 512)
EPS
PDF
AI

In the next release add the PNG Version.

The set also include Metrize Fonts Icons for use in your web projects with @font-face.
Include a simple guide how to use the icons fonts, the necessary scripts for compatibility with IE7.

Thanks Icomoon App for create/editing the font. ( http://icomoon.io/ )

Enjoy Metrize Icons.
I hope you like them and can be useful in your future projects.

Alessio.
---

USAGE LICENSE:

You are free to use Metrize Icons (the "Icon Set") or any part thereof (the "Icons") in any personal, open-source or commercial work without obligation of payment (monetary or otherwise) or attribution.

Do not sell, sub-license, rent, transfer, host, redistribute the Icon Set. (either in existing or modified form).

The rights to each "Social Icons" are either trademarked or copyrighted by the respective company.

Attribution is optional but it is always appreciated.

Intellectual property rights are not transferred with the download of the icons.

---

ALL ICONS LICENSED ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED. ALESSIO ATZENI IS NOT LIABLE FOR ANY DAMAGES ARISING OUT OF ANY DEFECTS IN THIS MATERIAL. 

YOU AGREE TO HOLD THE ALESSIO ATZENI HARMLESS FOR ANY RESULT THAT MAY OCCUR DURING THE COURSE OF USING, OR INABILITY TO USE THESE LICENSED ICONS. 

IN NO EVENT SHALL WE BE LIABLE FOR ANY DAMAGES INCLUDING, BUT NOT LIMITED TO, DIRECT, INDIRECT, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES OR OTHER LOSSES ARISING OUT OF THE USE OF OR INABILITY TO USE THIS PRODUCTS.

---
--------------------

 pyrcc5 resources.qrc > ./resources_rc.py # 이걸 해야 리소스 읽어올 수 있다


#upLeft {
	background-color: transparent;
	border-image: url(:play.png);
	background: none;
	border: none;
	background-repeat: none;
}

./qmake /Users/sungyokim/untitled4/untitled4.pro -spec macx-g++ CONFIG+=debug CONFIG+=x86_64 CONFIG+=qml_debug

export PATH="/usr/local/opt/qt/bin:$PATH"



"""

# built-in module
import enum
import logging
import os
import platform
import re
import sys
import time
# data양식 하나 짜서 만들어야지??

# music player
import vlc

# PyQt
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from IPython import embed
import ui.resources_rc

audio_file_filter='AUDIO (*.mp3 *.wav *.ogg *.wma)'
btn_stylesheet_play = '''#btn_play {{
	background-color: transparent;
	border-image: url(:/{});
	background: none;
	border: none;
	background-repeat: none;
	}}'''

def get_btn_stylesheet(play=True):
	if play:
		png_file = 'play.png'
	else:
		png_file = 'pause.png'
	return btn_stylesheet_play.format(png_file)

def value_equlizer(value, place_value=2):
	"""
	make equel the value of place
	"""
	value = str(value)
	length = len(value)
	if length < place_value:
		value = '0' * (place_value - length) + value
	if place_value < length:
		value = value[:place_value]
	return value


def time_former(time_str):
	if not time_str:
		time_str = 0
	seconds, milliseconds = time_str // 1000, time_str % 1000
	# milliseconds = value_equlizer(milliseconds)
	milliseconds = str(milliseconds)
	result = time.strftime('%H:%M:%S', time.gmtime(seconds))
	return result


class PlayStatus(enum.Enum):
	PLAY = 'Play'
	STOP = 'STOP'
	NO_FILE = 'NO_FILE'


class Platform(enum.Enum):
	MS_WINDOWS = 'MS_WINDOWS'
	LINUX = 'LINUX'
	MAC_OS = 'MAC_OS'


class VlcPlayer():
	def __init__(self):
		self.instance = vlc.Instance()
		self.mediaplayer = self.instance.media_player_new()
		self.media = None
		self.is_paused = False
		self.title = ''
		self.platform = None
		self.goback_position_value = None

	def initialize_payer(self):
		self.goback_position_value = None

	def check_platform(self):
		if platform.system() == 'Darwin': # for MacOS
			self.platform = Platform.MAC_OS
		elif platform.system() == 'Windows':
			self.platform = Platform.MS_WINDOWS
		elif platform == 'Linux':
			self.platform = Platform.LINUX
		else:
			self.platform = Platform.LINUX # etc

	def set_file(self, file_name):
		self.media = self.instance.media_new(file_name)

		# Put the media in the media player
		self.mediaplayer.set_media(self.media)

		# Parse the metadata of the file
		self.media.parse()
		self.title = self.media.get_meta(0)

	def play_pause(self):
		if self.mediaplayer.is_playing():
			self.mediaplayer.pause()
			return PlayStatus.STOP
		else:
			result = self.mediaplayer.play()
			if result == -1: # no file
				return PlayStatus.NO_FILE
			else:
				return PlayStatus.PLAY

	def stop(self):
		self.mediaplayer.stop()
		self.set_rate(1)

	def move(self, second, reposit_rate = True): # backward, forward
		if reposit_rate:
			self.set_rate(1)

		atom = 500 # 블록 최소단위 0.5

		current_time = int(self.mediaplayer.get_time() / atom) * atom 
		
		if self.mediaplayer.is_playing():
			self.mediaplayer.pause()
			pos = current_time + (second * 1000)
			self.mediaplayer.set_time(pos)
			self.mediaplayer.play()

	def get_total_play_time(self):
		return time_former(self.media.get_duration())

	def get_current_play_time(self):
		current_time = self.mediaplayer.get_time()
		if current_time == -1:
			current_time = 0
		return time_former(current_time)

	def get_position(self):
		return self.mediaplayer.get_position()

	def set_rate(self, rate):
		if rate < 0.1 or 2.0 < rate:
			raise IOError('invalid rate: "{}" from 0.1 to 2.0'.format(rate))
		self.mediaplayer.set_rate(rate)

	def set_goback_position(self):
		position = self.mediaplayer.get_time()
		self.goback_position_value = position
		return time_former(position)

	def goback_position(self, pos=None):
		"""
		포지션 변경 메소드
		- 파라미터 할당시 파라미터가 우선
		- 없을 시 인스턴스 프로퍼티 호출

		"""
		if pos != None :
			self.mediaplayer.set_time(pos)
		elif self.goback_position_value:
			self.mediaplayer.set_time(self.goback_position_value)


class Rocust(QMainWindow):
	def __init__(self, log, parent=None):
		super(Rocust, self).__init__(parent)
		# set property #
		self.app_name = 'Rocust'
		self.file_name = ''
		self.volume = 0
		self.total_time = ''
		self.speed = 1.0
		self.repeat_time_value = 0

		# load mainWindow
		self.ui = uic.loadUi("ui/mainwindow.ui", self, resource_suffix='resources_rc')
		self.vlc = VlcPlayer()
		self.set_window_title()
		# property alias
		self.ui_spinbox_speed = self.ui.spinbox_speed
		self.ui_lbl_check_point = self.ui.lbl_check_point
		self.ui_lbl_play_time = self.ui.lbl_play_time
		self.ui_btn_play = self.ui.btn_play
		self.ui_sldr_position = self.ui.sldr_position
		self.ui_sldr_volum = self.ui.sldr_volum
		self.ui.show()
		self.log = log
		#timer for realtime update
		self.timer = QTimer(self)
		self.timer.setInterval(100)
		self.timer.timeout.connect(self.realtime_update)

	def set_window_title(self, title=None):
		if title:
			self.ui.setWindowTitle('[{}] - {}'.format(self.app_name, title))
		else:
			self.ui.setWindowTitle('[{}]'.format(self.app_name))

	def initialize_player(self):
		pass

	def update_play_time(self):

		# self.log.debug('self.vlc.get_current_play_time():' + self.vlc.get_current_play_time())
		time_str = self.vlc.get_current_play_time() + '/' + self.total_time
		self.ui_lbl_play_time.setText(time_str)

	def realtime_update(self):
		"""update for ui and else"""
		media_pos = int(self.vlc.mediaplayer.get_position() * 1000)
		self.ui_sldr_position.setValue(media_pos)
		self.update_play_time()

		if not self.vlc.mediaplayer.is_playing():
			self.stop()
			self.go_to_first()
			self.update_play_time()

	def go_to_first(self):
		self.vlc.goback_position(0)

	def start(self):
		self.timer.start()
		self.ui_btn_play.setStyleSheet(get_btn_stylesheet(False))

	@pyqtSlot()
	def open_file(self):
		self.log.debug('open_file')
		dialog_txt = "Choose Media File"
		filename = QFileDialog.getOpenFileName(self.ui, dialog_txt, os.path.expanduser('~'), filter=audio_file_filter)
		if not filename:
			return

		self.file_name = filename[0]
		self.log.debug(self.file_name)
		self.vlc.set_file(self.file_name)
		self.total_time = self.vlc.get_total_play_time()
		self.update_play_time()
		self.set_window_title(self.vlc.title)

	@pyqtSlot()
	def play_pause(self):
		status = self.vlc.play_pause()
		self.log.debug(str(status))
		if status == PlayStatus.PLAY:
			self.start()
		else:
			self.stop()

	@pyqtSlot()
	def stop(self):
		self.timer.stop()
		self.ui_btn_play.setStyleSheet(get_btn_stylesheet(True))

	@pyqtSlot()
	def set_position(self):
		self.timer.stop()
		# pos = self.sldr_position.value()
		self.vlc.mediaplayer.set_position(self.sldr_position.value() / 1000.0)
		# self.timer.start()

	@pyqtSlot()
	def stop_timer(self):
		self.log.debug('stop_timer')
		self.vlc.mediaplayer.set_position(self.sldr_position.value() / 1000.0)
		self.timer.stop()

	@pyqtSlot()
	def start_timer(self):	
		self.log.debug('start_timer')
		self.timer.start()

	@pyqtSlot()
	def backward_s(self):
		self.log.debug('backward_s')
		self.vlc.move(-1, reposit_rate=False)

	@pyqtSlot()
	def backward_m(self):
		self.log.debug('backward_m')
		self.vlc.move(-3)

	@pyqtSlot()
	def backward_l(self):
		self.log.debug('backward_s')
		self.vlc.move(-5)

	@pyqtSlot()
	def forward_m(self):
		self.log.debug('forward_m')
		self.vlc.move(3)

	@pyqtSlot()
	def forward_l(self):
		self.log.debug('forward_l')
		self.vlc.move(5)

	@pyqtSlot()
	def speed_up(self):
		pass

	@pyqtSlot()
	def speed_down(self):
		pass

	@pyqtSlot()
	def check_point(self):
		self.log.debug('check_point')
		point_time = self.vlc.set_goback_position()
		if point_time:
			self.ui_lbl_check_point.setText(point_time)

	@pyqtSlot()
	def go_back_to_point(self):
		self.log.debug('goback_to_point')
		self.vlc.goback_position()

	@pyqtSlot()
	def volume_up(self):
		pass

	@pyqtSlot()
	def volume_down(self):
		pass


def execute_app(argv, log, console=False):
	app = QApplication(argv)
	rocust = Rocust(log)
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

	sys.exit(execute_app(argv, log, opt.console))
	
if __name__ == '__main__':
	main(__import__('sys').argv)
