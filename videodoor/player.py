from pyomxplayer import OMXPlayer

class VideoPlayer:
	"""docstring for VideoPlayer"""

	def __init__(self, video_file, video_options = ""):
		self.video_file = video_file
		self.video_options = video_options
		self.video_status = false
		self.command_queue = Queue()

	def init_omxplayer():
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

	def process_command(command):
		command_function={
			'PLAY' : play,
			'STOP' : stop
		}

	def process_queue():
		command = self.command_queue.get()

	def run():
		self.init_omxplayer()
		while true:
			self.process_queue()

		