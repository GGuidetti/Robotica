from pyfirmata import Arduino, util
import time

board = Arduino ('/dev/ttyACM0')

class engine_t:
	def __init__ (self, pin_dir0, pin_dir1, pin_speed, max_speed):
		self.pin_dir0 = pin_dir0
		self.pin_dir1 = pin_dir1
		self.pin_speed = pin_speed
		self.max_speed = max_speed
		self.dir0 = 0
		self.dir1 = 0
		self.speed = 0.0
		
		self.board_pin_speed = board.get_pin(str('d:'+str(pin_speed)+':p'))

		self.set_dir(0, 0)
		self.set_speed(0.0)
		

	def set_dir (self, dir0, dir1):
		self.dir0 = dir0
		self.dir1 = dir1
		board.digital[self.pin_dir0].write(dir0)
		board.digital[self.pin_dir1].write(dir1)


	def set_speed (self, speed):
		self.speed = speed*self.max_speed
		self.board_pin_speed.write(self.speed)

class ir_sensor_t:
	def __init__ (self, pin):
		self.pin = pin
		self.board_pin = board.get_pin(str('a:'+str(pin)+':i'))

	def read (self):
		return self.board_pin.read()

def panic (msg):
	eng_left.set_speed(0.0)
	eng_right.set_speed(0.0)
	while True:
		print("panic: ", msg)

def line_follow():
	state = "STRAIGHT"
	while True:
		left = sensor_left.read()
		right = sensor_right.read()

		error = right - left
		direction = error
		
		threshold_detect_curve = 0.2
		threshold_detect_full_curve = 0.45
		
		if state == "STRAIGHT":
			if error > threshold_detect_curve: # iniciando curva a esquerda
				state = "LEFT"
			elif error < (-1.0*threshold_detect_curve): # iniciando curva a direita
				state = "RIGHT"
		elif state == "LEFT":
			if error > threshold_detect_full_curve: # curva acentuada a esquerda
				state = "FULL_LEFT"
			elif error < (-1.0*threshold_detect_full_curve): # panic
				panic("LEFT -> FULL_RIGHT")
			elif error > (-1.0*threshold_detect_curve) and error < threshold_detect_curve: # encontrando linha reta
				state = "STRAIGHT"
		elif state == "RIGHT":
			if error > threshold_detect_full_curve: # panic
				panic("RIGHT -> FULL_LEFT")
			elif error < (-1.0*threshold_detect_full_curve): # curva acentuada a direita
				state = "FULL_RIGHT"
			elif error > (-1.0*threshold_detect_curve) and error < threshold_detect_curve: # encontrando linha reta
				state = "STRAIGHT"
		elif state == "FULL_LEFT":
			error = (right + left) / 2
			direction = 1.0
			if error < threshold_detect_full_curve: # curva acentuada a esquerda
				state = "LEFT"
			elif error < (-1.0*threshold_detect_full_curve): # panic
				panic("FULL_LEFT -> FULL_RIGHT")
		elif state == "FULL_RIGHT":
			error = (right + left) / (-2)
			direction = -1.0
			if error > threshold_detect_full_curve: # panic
				panic("FULL_RIGHT -> FULL_LEFT")
			elif error > (-1.0*threshold_detect_full_curve): # curva acentuada a direita
				state = "RIGHT"
		
		print ("estado:", state, "esquerda:", left, "direita:", right , "error:", error)

		if direction < 0.0:  # robot is pending to the left
			direction = direction * -1.0

			# we first set the left engine to full speed
			eng_left.set_speed(1.0)

			#then, we reduce the speed of the right engine proportionally to the error
			eng_right.set_speed(1.0 - direction)
		else: # robot is pending to the right
			# we first set the right engine to full speed
			eng_right.set_speed(1.0)

			#then, we reduce the speed of the left engine proportionally to the error
			eng_left.set_speed(1.0 - direction)

iterator = util.Iterator(board)
iterator.start()

#eng_left = engine_t(2, 4, 3, 0.563)
#eng_right = engine_t(10, 12, 11, 0.7)
eng_left = engine_t(2, 4, 3, 0.863)
eng_right = engine_t(10, 12, 11, 1.0)

eng_left.set_dir(1, 0)
eng_right.set_dir(0, 1)

eng_left.set_speed(0.0)
eng_right.set_speed(0.0)

sensor_left = ir_sensor_t(1)
sensor_right = ir_sensor_t(2)
#sensor_right = ir_sensor_t(3)

inicio = time.time()
tempo = 0	
while ((tempo) < 4):
	tempo = time.time()-inicio

line_follow()
