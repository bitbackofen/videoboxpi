import os.path
from pyomxplayer import OMXPlayer
from logbook import Logger

class VideoPlayer:
	"""docstring for VideoPlayer"""

	def __init__(self, video_file, video_options = ""):
		self.log = Logger('VideoPlayer')
		self.video_file = video_file
		self.video_options = video_options
		self.video_status = false
		self.command_queue = Queue()
		self.log.debug('VideoPlayer created with file: '+self.video_file+' and options '+self.video_options)

	def init_omxplayer():
		if not os.path.isfile(self.video_file):
			self.log.error('file does not exist: '+self.video_file)
			return
		self.omx_player = OMXPlayer(self.video_file, self.video_options)

	def play():
		if not self.video_status:
			self.omx_player.toggle_pause()
			self.video_status = true

	def stop():
		if self.video_status:
			self.omx_player.toggle_pause()
			self.omx_player.previous_chapter()
			self.video_status = false

	def restart():
		self.stop()
		self.start()

	def process_command(command):
		command_function={
			'PLAY' : self.play,
			'STOP' : self.stop,
			'RESTART' : self.restart
		}
		command_function[command]()

	def process_queue():
		command = self.command_queue.get()
		self.process_command(command)
		self.command_queue.task_done()

	def get_command_queue():
		return self.command_queue

	def run():
		self.init_omxplayer()
		while true:
			self.process_queue()

		