from .Block import Block
from . import *


class Ball(Block):
	def __init__(self, path, x_pos, y_pos, speed_x, speed_y, paddles):
		super().__init__(path, x_pos, y_pos)
		self.speed_x = speed_x * random.choice((-1, 1))
		self.speed_y = speed_y * random.choice((-1, 1))
		self.paddles = paddles
		self.active = False
		self.score_time = 0

	def update(self):
		if self.active:
			self.rect.x += self.speed_x
			self.rect.y += self.speed_y
			self.collisions()
		else:
			self.restart_counter()

	def collisions(self):
		if self.rect.top <= 0 or self.rect.bottom >= screen_height:
			pygame.mixer.Sound.play(plob_sound)
			self.speed_y *= -1

		if pygame.sprite.spritecollide(self, self.paddles, False):
			pygame.mixer.Sound.play(plob_sound)
			collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
			if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
				self.speed_x *= -1
			if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
				self.speed_x *= -1
			if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
				self.rect.top = collision_paddle.bottom
				self.speed_y *= -1
			if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
				self.rect.bottom = collision_paddle.top
				self.speed_y *= -1

	def reset_ball(self):
		self.active = False
		self.speed_x *= random.choice((-1, 1))
		self.speed_y *= random.choice((-1, 1))
		self.score_time = pygame.time.get_ticks()
		self.rect.center = (screen_width / 2, screen_height / 2)
		pygame.mixer.Sound.play(score_sound)

	def restart_counter(self):
		current_time = pygame.time.get_ticks()
		countdown_number = 3

		if current_time - self.score_time <= 700:
			countdown_number = "ready"
		if 700 < current_time - self.score_time <= 1400:
			countdown_number = "set"
		if 1400 < current_time - self.score_time <= 2100:
			countdown_number = "go!!"
		if current_time - self.score_time >= 2100:
			self.active = True

		time_counter = basic_font.render(str(countdown_number), True, accent_color)
		time_counter_rect = time_counter.get_rect(center=(screen_width / 2, screen_height / 2 + 50))
		pygame.draw.rect(screen, bg_color, time_counter_rect)
		screen.blit(time_counter, time_counter_rect)