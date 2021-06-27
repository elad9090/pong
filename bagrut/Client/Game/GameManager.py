from time import sleep
from . import *
from .Player import Player
from .Ball import Ball
import sys
import socket
import threading
from .score import score as Score

class GameManager:
	def __init__(self):
		player = self.player = Player('Paddle.png', screen_width - 20, screen_height / 2, 10)
		opponent = self.opponent = Player('Paddle.png', 20, screen_height / 2, 15, is_comp=True)

		paddle_group = pygame.sprite.Group()
		paddle_group.add(player)
		paddle_group.add(opponent)
		ball = self.ball = Ball('Ball.png', screen_width / 2, screen_height / 2, 4, 4, paddle_group)
		ball_sprite = pygame.sprite.GroupSingle()
		ball_sprite.add(ball)

		self.ball_group = ball_sprite
		self.paddle_group = paddle_group

		self.on_quit = []

		self.fps = 60
	def add_on_quit_listener(self, c):
		if not callable(c):
			raise Exception(f'{c.__name__} IS NOT CALLABLE!')
		self.on_quit.append(c)

	def pause(self):
		pause = True
		basic_font = pygame.font.Font('freesansbold.ttf', 40)
		pause_text = basic_font.render("press any key to continue", True, (200, 150, 255))
		pause_rect = pause_text.get_rect(center=(screen_width / 2, ((screen_height / 2) - 100)))
		screen.blit(pause_text, pause_rect)
		pygame.display.flip()
		while pause:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key != pygame.K_UP and event.key != pygame.K_DOWN:
						pause = False
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

	def p1Level(self):
		global fps
		intro = True
		easy = pygame.image.load("easy_mode.jpg").convert()
		easy_rect = easy.get_rect(center=(screen_width / 2, screen_height / 4))
		medium = pygame.image.load("normal_mode.jpg").convert()
		medium_rect = medium.get_rect(center=(screen_width / 2, 2 * (screen_height / 4)))
		hard = pygame.image.load("hard_mode.jpg").convert()
		hard_rect = hard.get_rect(center=(screen_width / 2, 3 * (screen_height / 4)))
		while intro:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					click = True
					while click:
						if pygame.Rect.collidepoint(easy_rect, pygame.mouse.get_pos()):
							self.opponent.speed = 5
							click = False
							self.fps = 60
						if pygame.Rect.collidepoint(medium_rect, pygame.mouse.get_pos()):
							self.opponent.speed = 10
							click = False
							self.fps = 120
						if pygame.Rect.collidepoint(hard_rect, pygame.mouse.get_pos()):
							self.opponent.speed = 15
							self.player.speed = 10
							click = False
							self.fps = 200
					intro = False
			screen.fill((25, 35, 50))
			screen.blit(easy, easy_rect)
			screen.blit(medium, medium_rect)
			screen.blit(hard, hard_rect)
			pygame.display.flip()
			clock.tick(120)

	def run_game(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					for c in self.on_quit:
						c()
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						self.player.movement -= self.player.speed
					if event.key == pygame.K_DOWN:
						self.player.movement += self.player.speed
					if event.key == pygame.K_p:
						self.pause()
						# print(player.rect.y)
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_UP:
						self.player.movement += self.player.speed
					if event.key == pygame.K_DOWN:
						self.player.movement -= self.player.speed

			screen.fill(bg_color)
			pygame.draw.rect(screen, accent_color, middle_strip)

			# Drawing the game objects
			self.paddle_group.draw(screen)
			self.ball_group.draw(screen)

			# Updating the game objects
			self.paddle_group.update(self.ball_group)
			self.ball_group.update()
			self.reset_ball()
			self.draw_score()

			# Rendering
			pygame.display.flip()
			clock.tick(self.fps)

	def reset_ball(self):
		if self.ball_group.sprite.rect.right >= screen_width:
			self.opponent.score += 1
			self.ball_group.sprite.reset_ball()
		if self.ball_group.sprite.rect.left <= 0:
			self.player.score += 1
			self.ball_group.sprite.reset_ball()
		if self.player.score == 7 or self.opponent.score == 7:
			win = True
			if self.player.score == 7:
				text= "wow you are Amazing"
			else:
				text = "you lose"
			win_text = basic_font.render(str(text), True, (200, 150, 255))
			win_rect = win_text.get_rect(center=(screen_width / 2, ((screen_height / 2) - 100)))
			Score(self.fps, self.opponent.score, self.player.score).mainloop()
			while win:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_SPACE:
							win = False
							self.player.score = 0
							self.opponent.score = 0
							self.p1Level()
				next_text = basic_font.render("press spacebar for a new game", True, (200, 150, 255))
				next_rect = win_text.get_rect(center=(((screen_width / 2)-120), ((screen_height / 2) + 100)))
				screen.blit(win_text, win_rect)
				screen.blit(next_text, next_rect)
				pygame.display.flip()



	def draw_score(self):
		player_score = basic_font.render(str(self.player.score), True, accent_color)
		opponent_score = basic_font.render(str(self.opponent.score), True, accent_color)

		player_score_rect = player_score.get_rect(midleft=(screen_width / 2 + 40, screen_height / 2))
		opponent_score_rect = opponent_score.get_rect(midright=(screen_width / 2 - 40, screen_height / 2))

		screen.blit(player_score, player_score_rect)
		screen.blit(opponent_score, opponent_score_rect)



class GameManagerMP(GameManager):
	def print(self, *args, **kwargs):
		print('RECIEVED DATA --->>\t\t', *args, **kwargs)

	def __init__(self, address):
		super().__init__()

		sck = self.sck = socket.socket()
		self.opponent.is_comp(False)

		self.player.speed = self.opponent.speed = 10

		sck.connect(address)
		sck.send(b'connected')

		def sck_rcv_worker():
			side = sck.recv(2)
			self.print(side)
			if side == b'p1':
				self.player.rect.x = screen_width - 20
				self.opponent.rect.x = 20
			elif side == b'p2':
				self.player.rect.x = 20
				self.opponent.rect.x = screen_width - 20

			# sck.send(b'redy')

			while True:
				data = sck.recv(64).decode()
				while data[0] == '<':
					data = data[1:]
				p1, p2, ball, stp, winner = data.split(';')
				stp = int(stp)
				winner = None if winner == 'null' else winner
				if winner:
					print(str(side))
					if winner == str(side):
						text= "you win"
					else:
						text="you lose"
					win_text = basic_font.render(str(text), True, (200, 150, 255))
					win_rect = win_text.get_rect(center=(screen_width / 2, ((screen_height / 2) - 100)))
					win =True
					while win:
						for event in pygame.event.get():
							if event.type == pygame.QUIT:
								pygame.quit()
								sys.exit()
						screen.blit(win_text, win_rect)
						pygame.display.flip()
				#print(self.player.rect)

				if p1 == 'null':
					p1 = '400,False,0'
				if p2 == 'null':
					p2 = '400,False,0'

				p1 = p1.split(',')
				p2 = p2.split(',')
				ball = ball.split(',')

				if side == b'p1':
					self.player.score = p1[2]
					self.opponent.score = p2[2]
					self.opponent.y = int(p2[0])
				elif side == b'p2':
					self.opponent.score = p1[2]
					self.player.score = p2[2]
					self.opponent.y = int(p1[0])

				self.ball.x = int(ball[0])
				self.ball.y = int(ball[1])

				if stp == 1:
					pygame.mixer.Sound.play(plob_sound)
				elif stp == 2:
					pygame.mixer.Sound.play(score_sound)

		def sck_snd_worker():
			while True:
				d = self.player.pickle().encode()
				d = b'<' * (9 - len(d)) + d
				self.sck.send(d)
				sleep(0.02)
				

		threading.Thread(target=sck_rcv_worker).start()
		threading.Thread(target=sck_snd_worker).start()

		self.add_on_quit_listener(lambda: self.sck.close())

	def run_game(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					for c in self.on_quit:
						c()
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						self.player.movement -= self.player.speed
					if event.key == pygame.K_DOWN:
						self.player.movement += self.player.speed
						# print(player.rect.y)
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_UP:
						self.player.movement += self.player.speed
					if event.key == pygame.K_DOWN:
						self.player.movement -= self.player.speed

			screen.fill(bg_color)
			pygame.draw.rect(screen, accent_color, middle_strip)

			self.paddle_group.update()

			# Drawing the game objects
			self.paddle_group.draw(screen)
			self.ball_group.draw(screen)

			# Updating the game objects
			self.reset_ball()
			self.draw_score()

			# Rendering
			pygame.display.flip()
			clock.tick(self.fps)


	def reset_ball(self):
		pass

	def draw_score(self):
		player_score = basic_font.render(str(self.player.score), True, accent_color)
		opponent_score = basic_font.render(str(self.opponent.score), True, accent_color)

		some_var = 40 if self.player.rect.x == screen_width - 20 else -40

		player_score_rect = player_score.get_rect(midleft=(screen_width / 2 + some_var, screen_height / 2))
		opponent_score_rect = opponent_score.get_rect(midright=(screen_width / 2 - some_var, screen_height / 2))

		if self.player.score == 7 or self.opponent.score == 7:
			win = True
			if self.player.score == 7:
				text = "wow you are Amazing"
			else:
				text = "you lose"
			win_text = basic_font.render(str(text), True, (200, 150, 255))
			win_rect = win_text.get_rect(center=(screen_width / 2, ((screen_height / 2) - 100)))
			while win:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_SPACE:
							win = False
							self.player.score = 0
							self.opponent.score = 0
				next_text = basic_font.render("press spacebar for a new game", True, (200, 150, 255))
				next_rect = win_text.get_rect(center=(((screen_width / 2) - 120), ((screen_height / 2) + 100)))
				screen.blit(win_text, win_rect)
				screen.blit(next_text, next_rect)
				pygame.display.flip()

		screen.blit(player_score, player_score_rect)
		screen.blit(opponent_score, opponent_score_rect)